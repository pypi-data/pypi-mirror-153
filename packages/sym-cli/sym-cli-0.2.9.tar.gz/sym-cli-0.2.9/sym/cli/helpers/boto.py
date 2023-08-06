import json
import re
import shlex
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from typing import Dict, Sequence

import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError, WaiterError
from sym.shared.cli.helpers.boto import make_intercept_boto_errors

from ..decorators import retry
from ..errors import AccessDenied, ExpiredCredentials, TargetNotConnected
from .config import SymConfigFile
from .params import get_ssh_user

InstanceIDPattern = re.compile("^i-[a-f0-9]+$")
RequestExpired = re.compile(r"RequestExpired|ExpiredToken")
TargetNotConnectedPattern = re.compile("TargetNotConnected")
AccessDeniedPattern = re.compile("AccessDeniedException")

intercept_boto_errors = make_intercept_boto_errors(
    {
        TargetNotConnectedPattern: TargetNotConnected,
        AccessDeniedPattern: AccessDenied,
        RequestExpired: ExpiredCredentials,
    }
)


def boto_client(saml_client, service):
    creds = saml_client.get_creds()
    return boto3.client(
        service,
        config=BotoConfig(region_name=get_region(saml_client, creds)),
        aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
        aws_session_token=creds.get("AWS_SESSION_TOKEN"),
    )


def get_region(saml_client, creds=None) -> str:
    override = saml_client.options.aws_region
    return override or (creds or saml_client.get_creds()).get("AWS_REGION")


@intercept_boto_errors
def send_ssh_key(saml_client: "SAMLClient", instance: str, ssh_key: SymConfigFile):
    saml_client.dprint("sending SSH key")

    user = get_ssh_user()
    ssm_client = boto_client(saml_client, "ssm")
    # fmt: off
    command = dedent(
        f"""
        #!/bin/bash
        mkdir -p "$(echo ~{user})/.ssh"
        echo "{ssh_key.path.with_suffix('.pub').read_text()}" >> "$(echo ~{user})/.ssh/authorized_keys"
        chown -R {user}:{user} "$(echo ~{user})/.ssh"
        """
    ).strip()
    # fmt: on

    response = ssm_client.send_command(
        InstanceIds=[instance],
        DocumentName="AWS-RunShellScript",
        Comment="SSH Key for Sym",
        Parameters={"commands": command.splitlines()},
    )

    saml_client.dprint(response)

    _wait_for_command(ssm_client, instance, response)


@retry(
    WaiterError,
    count=5,
    delay=1,
    check_ex=lambda ex: ex.last_response["Error"]["Code"] == "InvocationDoesNotExist",
)
def _wait_for_command(ssm_client, instance, response):
    waiter = ssm_client.get_waiter("command_executed")
    waiter.wait(
        InstanceId=instance,
        CommandId=response["Command"]["CommandId"],
        WaiterConfig={"Delay": 1},
    )


@intercept_boto_errors
def get_identity(saml_client) -> dict:
    sts_client = boto_client(saml_client, "sts")
    return sts_client.get_caller_identity()


@intercept_boto_errors
def _ssm_command(saml_client, ssm_client, params: Dict):
    saml_client.dprint("SSM Session: ", params=params)
    response = ssm_client.start_session(**params)
    command = [
        "session-manager-plugin",
        json.dumps(response),
        ssm_client.meta.region_name,
        "StartSession",
        "",  # This is the profile name, left empty since we're supplying credentials via environment
        json.dumps(params),
        ssm_client.meta.endpoint_url,
    ]
    return response, command


@contextmanager
def _ssm_session(saml_client, params: Dict):
    ssm_client = boto_client(saml_client, "ssm")
    response, command = _ssm_command(saml_client, ssm_client, params=params)
    try:
        yield command
    finally:
        try:
            ssm_client.terminate_session(SessionId=response["SessionId"])
        except ClientError:
            pass  # Creds expired while session was in progress, cannot terminate it


@contextmanager
def ssm_ssh_session(saml_client, instance: str, port: int):
    params = {
        "Target": instance,
        "DocumentName": "AWS-StartSSHSession",
        "Parameters": {"portNumber": [str(port)]},
    }
    with _ssm_session(saml_client, params) as command:
        yield command


@contextmanager
def ssm_interactive_command(saml_client, instance: str, user: str, cmd: Sequence[str]):
    full_cmd = f"sudo run-parts /etc/update-motd.d; sudo su -l {user}"
    if len(cmd) > 0:
        joined = shlex.join(cmd)
        full_cmd += f' -c "{joined}"'

    params = {
        "Target": instance,
        "DocumentName": "AWS-StartInteractiveCommand",
        "Parameters": {"command": [f"{full_cmd}"]},
    }
    with _ssm_session(saml_client, params) as command:
        yield command


@intercept_boto_errors
def put_file(saml_client, bucket: str, file_path: Path, object_path: str):
    s3_client = boto_client(saml_client, "s3")
    s3_client.upload_file(
        str(file_path),
        bucket,
        object_path,
        ExtraArgs={"ACL": "bucket-owner-full-control"},
    )
