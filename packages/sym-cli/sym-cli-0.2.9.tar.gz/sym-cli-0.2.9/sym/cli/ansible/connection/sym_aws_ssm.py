# Ignore black formatting in this file to ensure backward
# compatibility with python 2.7
# fmt: off

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
- Yasyf Mohamedali <yasyf@symops.io>
- Rick Ducott <rick@symops.io>
connection: sym_aws_ssm
short_description: Use SSM SendCommand as an Ansible Connection
description:
- Use SSM SendCommand as an Ansible Connection. Inspired heavily by community.aws.aws_ssm.
requirements:
- session-manager-plugin is on your PATH
options:
  region:
    description: The region to use for all boto commands
    vars:
    - name: ansible_aws_ssm_region
    default: 'us-east-1'
  bucket:
    description: The name of the S3 bucket used for file transfers.
    vars:
    - name: ansible_aws_ssm_bucket
  profile:
    description: The AWS profile to use
    vars:
    - name: ansible_aws_ssm_profile
      default: 'sym-ansible'
  retries:
    description: Number of attempts to connect.
    default: 3
    type: integer
    vars:
    - name: ansible_aws_ssm_retries
  ssm_timeout:
    description: SSM connection timeout (in seconds)
    default: 120
    type: integer
    vars:
    - name: ansible_aws_ssm_timeout
  host_command:
    description: Host-to-Instance command
    vars:
    - name: ansible_aws_ssm_host_cmd
"""

import json
import os
import pty
import select
import shlex
import subprocess
import time
from functools import wraps

import boto3
from ansible.errors import AnsibleConnectionFailure, AnsibleError, AnsibleFileNotFound
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.module_utils.six.moves import xrange
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display

URL_TTL = 3600
CHUNK_SIZE = 1024
MAX_DELAY = 30
START_COMMAND = "SYM_COMMAND_START"
END_COMMAND = "SYM_COMMAND_END"

display = Display()


def ssm_retry(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        retries = int(self.get_option("retries"))
        cmd = args[0]

        for attempt in xrange(retries):
            try:
                response = func(self, *args, **kwargs)
                display.vvv(response, host=self.host)
                return response
            except self._ssm_client.exceptions.TargetNotConnected as e:
                raise AnsibleConnectionFailure(
                    "Instance %s (%s) must be managed by Session Manager. Is SSM Agent installed and active?"
                    % (self.instance_id, self.host),
                    orig_exc=e,
                )
            except (AnsibleConnectionFailure, Exception) as e:
                if "RequestExpired" in str(e):
                    raise AnsibleConnectionFailure(
                        "Your AWS credentials have expired. Please refresh them and try again.",
                        orig_exc=e,
                    )

                if attempt == retries - 1:
                    raise AnsibleConnectionFailure(e)

                delay = min((2 ** attempt) - 1, MAX_DELAY)

                if isinstance(e, AnsibleConnectionFailure):
                    msg = "ssm_retry: attempt: %d, cmd (%s), pausing for %d seconds" % (
                        attempt,
                        cmd,
                        delay,
                    )
                else:
                    msg = (
                        "ssm_retry: attempt: %d, caught exception(%s) from cmd (%s), pausing for %d seconds"
                        % (attempt, e, cmd, delay)
                    )
                display.vv(msg, host=self.host)

                time.sleep(delay)
                self.close()

    return wrapped


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


class Poller:
    def __init__(self, fd):
        self.fd = fd

    @classmethod
    def create(cls, fd):
        if hasattr(select, "poll"):
            return PollPoller(fd)
        else:
            return KQueuePoller(fd)

    def poll(self, timeout):
        return self._poll(timeout=timeout)

    def _poll(self, timeout):
        raise NotImplementedError


class KQueuePoller(Poller):
    def __init__(self, fd):
        super(KQueuePoller, self).__init__(fd)
        self.kq = select.kqueue()
        self.kevts = [select.kevent(self.fd)]

    def _poll(self, timeout):
        return bool(self.kq.control(self.kevts, 1, timeout))


class PollPoller(Poller):
    def __init__(self, fd):
        super(PollPoller, self).__init__(fd)
        self.poller = select.poll()
        self.poller.register(self.fd, select.POLLIN)

    def _poll(self, timeout):
        return bool(self.poller.poll(timeout))


class Connection(ConnectionBase):
    """ AWS SSM based connections """

    transport = "sym_aws_ssm"
    allow_executable = False
    allow_extras = True
    has_pipelining = False

    _process = None
    _session_id = None

    _stdout = None
    _poll_stdout = None
    _poll_stderr = None

    _ssm_client = None
    _s3_client = None

    _terminate = False

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.host = self._play_context.remote_addr
        self.user = self._play_context.remote_user

        # In Ansible 2.5, _load_name has not yet been set,
        # so the loading resources that use `self.get_option` from
        # init fail. As a result, we set them to None here and
        # initialize them when they're needed.
        self._ssm_client = None
        self._s3_client = None

    def _connect(self):
        if not self._session_id:
            self.start_ssm_session()
        return self

    def _get_instance_meta(self):
        cmd = self.get_option("host_command").replace("$HOST", self.host)
        return json.loads(to_text(subprocess.check_output(shlex.split(cmd)).strip()))

    def _start_process(self, cmd):
        display.vvvv(u"SSM COMMAND: {0}".format(to_text(cmd)), host=self.host)

        stdout_r, stdout_w = pty.openpty()
        self._process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=stdout_w,
            stderr=subprocess.PIPE,
            close_fds=True,
            bufsize=0,
        )
        os.close(stdout_w)

        self._stdout = os.fdopen(stdout_r, "rb", 0)

        self._poll_stdout = Poller.create(self._stdout)
        self._poll_stderr = Poller.create(self._process.stderr)

    def _prepare_terminal(self):
        # Disable command echo and prompt
        self._process.stdin.write(to_bytes("stty -echo\n" + "PS1=''\n"))

    def start_ssm_session(self):
        instance_meta = self._get_instance_meta()
        self.instance_id = instance_meta["instance"]

        self._s3_client = self._get_boto_client("s3")
        self._ssm_client = self._get_boto_client("ssm", region=instance_meta["region"])

        display.vvv(
            u"ESTABLISH SSM CONNECTION TO: {0}".format(self.instance_id),
            host=self.host,
        )

        response = self._ssm_client.start_session(
            Target=self.instance_id,
            DocumentName="AWS-StartInteractiveCommand",
            Parameters={"command": ["sudo su -l {0}".format(self.user)]},
        )
        self._session_id = response["SessionId"]
        display.vvv(u"SSM CONNECTION ID: {0}".format(self._session_id), host=self.host)

        cmd = [
            "session-manager-plugin",
            json.dumps(response),
            self.get_option("region"),
            "StartSession",
            self.get_option("profile"),
            json.dumps({"Target": self.instance_id}),
            self._ssm_client.meta.endpoint_url,
        ]

        self._start_process(cmd)
        self._prepare_terminal()

    def _wrap_command(self, cmd):
        return "echo {1}; {0}; echo {2} $?\n".format(cmd, START_COMMAND, END_COMMAND)

    def _flush_stderr(self):
        stderr = ""

        while self._process.poll() is None:
            if self._poll_stderr.poll(1):
                line = self._process.stderr.readline()
                display.vvvv(u"stderr line: {0}".format(to_text(line)), host=self.host)
                stderr = stderr + line
            else:
                break

        return stderr

    def _get_returncode(self, line):
        return int(line.split(" ")[-1])

    def _process_line(self, line):
        return to_text(line).replace("\r\r\n", "\n")

    @ssm_retry
    def exec_command(self, cmd, in_data=None, sudoable=True):
        super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)

        cmd = self._wrap_command(cmd)
        display.vvv(u"EXEC send: {0}".format(to_text(cmd)), host=self.host)

        self._flush_stderr()

        for chunk in chunks(cmd, CHUNK_SIZE):
            self._process.stdin.write(to_bytes(chunk))

        started = False
        stdout = ""

        for elapsed in range(self.get_option("ssm_timeout")):
            if self._process.poll():
                break

            if elapsed == self.get_option("ssm_timeout") - 1:
                self._terminate = True
                display.vvvv(
                    u"EXEC timeout stdout: {0}".format(to_text(stdout)),
                    host=self.host,
                )
                raise AnsibleConnectionFailure(
                    "SSM exec_command timeout on host: {0}".format(self.instance_id)
                )

            if not self._poll_stdout.poll(1000):
                display.vvvv(u"EXEC elapsed: {0}".format(elapsed), host=self.host)
                continue

            line = self._process_line(self._stdout.readline())
            display.vvvv(u"EXEC stdout line: {0}".format(line), host=self.host)

            if not started and START_COMMAND in line:
                display.vvvv(u"EXEC start", host=self.host)
                started = True
                continue

            if not started:
                continue

            if END_COMMAND in line:
                returncode = self._get_returncode(line)
                display.vvvv(u"EXEC end: {0}".format(line), host=self.host)
                return (returncode, stdout, self._flush_stderr())

            stdout = stdout + line

        return (self._process.returncode, stdout, self._flush_stderr())

    def _get_boto_client(self, service, region=None):
        return boto3.Session(
            profile_name=self.get_option("profile"),
            region_name=region or self.get_option("region"),
        ).client(service)

    def _get_url(self, action, key, http_method):
        return self._s3_client.generate_presigned_url(
            action,
            Params={"Bucket": self.get_option("bucket"), "Key": key},
            ExpiresIn=URL_TTL,
            HttpMethod=http_method,
        )

    @ssm_retry
    def _file_transport_command(self, in_path, out_path, ssm_action):
        path = "{0}/{1}".format(self.instance_id, out_path)

        if ssm_action == "get":
            command = "curl --request PUT --upload-file '{0}' '{1}'".format(
                in_path, self._get_url("put_object", path, "PUT")
            )
            result = self.exec_command(command, in_data=None, sudoable=False)
            with open(to_bytes(out_path), "wb") as f:
                self._s3_client.download_fileobj(self.get_option("bucket"), path, f)
        else:
            command = "curl '{0}' -o '{1}'".format(
                self._get_url("get_object", path, "GET"), out_path
            )
            with open(to_bytes(in_path), "rb") as f:
                self._s3_client.upload_fileobj(f, self.get_option("bucket"), path)
            result = self.exec_command(command, in_data=None, sudoable=False)

        self._s3_client.delete_object(Bucket=self.get_option("bucket"), Key=path)

        (returncode, stdout, stderr) = result
        if returncode == 0:
            return (returncode, stdout, stderr)
        else:
            raise AnsibleError(
                "failed to transfer file to %s %s:\n%s\n%s"
                % (
                    to_native(in_path),
                    to_native(out_path),
                    to_native(stdout),
                    to_native(stderr),
                )
            )

    def put_file(self, in_path, out_path):
        super(Connection, self).put_file(in_path, out_path)
        display.vvv(u"PUT {0} TO {1}".format(in_path, out_path), host=self.host)
        if not os.path.exists(to_bytes(in_path)):
            raise AnsibleFileNotFound(
                "file or module does not exist: {0}".format(to_native(in_path))
            )
        return self._file_transport_command(in_path, out_path, "put")

    def fetch_file(self, in_path, out_path):
        super(Connection, self).fetch_file(in_path, out_path)
        display.vvv(u"FETCH {0} TO {1}".format(in_path, out_path), host=self.host)
        return self._file_transport_command(in_path, out_path, "get")

    def close(self):
        if not self._session_id:
            return

        display.vvv(u"CLOSE SSM: {0}".format(self.instance_id), host=self.host)

        if self._terminate:
            self._process.terminate()
        else:
            try:
                self._process.communicate(b"\nexit\n")
            except Exception as e:  # Not sure why this fails sometimes
                display.vvv(u"ERROR CLOSING SSM: {0}".format(e), host=self.host)
                self._process.terminate()

        display.vvvv(u"TERMINATE SSM: {0}".format(self._session_id), host=self.host)
        self._ssm_client.terminate_session(SessionId=self._session_id)
        self._session_id = None
