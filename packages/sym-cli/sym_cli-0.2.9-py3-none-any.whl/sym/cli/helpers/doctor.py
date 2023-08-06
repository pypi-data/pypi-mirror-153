import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, cast

import click
from sym.shared.cli.helpers.os import has_command

from sym.cli.helpers.ansible import create_ssh_bin
from sym.cli.helpers.boto import put_file
from sym.cli.helpers.config import Config, SymConfigFile
from sym.cli.helpers.params import get_ssh_user
from sym.cli.helpers.ssh import ssh_key_and_config
from sym.cli.saml_clients.saml_client import SAMLClient

BUCKET = "sym-doctor-prod-us-east-1"

BINARIES = [
    "aws",
    "ssh",
    "session-manager-plugin",
    "sym",
    "python",
    "python3",
    "pip",
    "pip3",
    "aws-okta",
    "saml2aws",
    "ansible",
]

PIP_PACKAGES = [
    "ansible",
    "boto",
    "boto3",
    "six",  # just here for a sanity check
]

REMOTE_LOG_DIRS = ["/var/log/amazon/ssm"]

TEST_PLAYBOOK = """
---
- name: Ping
  hosts: all
  become: true

  tasks:
    - ping:
"""

INSTANCE_PATTERN = re.compile(
    r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|i-[a-f0-9]+)\s+:\sok="
)


def self_update():
    click.echo("Checking for updates...")
    version = self_update_pipx()
    if version is None:
        click.secho(
            "Failed to determine current version! It appears that sym is not a pipx-managed binary",
            fg="red",
        )
    else:
        old_version, new_version = version
        if old_version != new_version:
            click.secho(f"Updating to {new_version}!", fg="yellow")
            return subprocess.run([*sys.argv, "--did-update"])
        else:
            click.secho(f"{old_version} is the latest version!", fg="green")


def self_update_pipx() -> Optional[Tuple[str, str]]:
    if not has_command("pipx"):
        return None
    if not check_pipx_package_provides_binary("sym-cli", "sym"):
        return None
    version = get_version("sym")
    try:
        run_and_log_args(["pipx", "upgrade", "sym-cli"], check=True)
    except subprocess.CalledProcessError:
        return None
    return (cast(str, version), cast(str, get_version("sym")))


def check_saml_client(client, path: Path):
    message = f"client: {client.__class__.__name__}\nis_setup:{client.is_setup()}"
    click.secho(message, fg="blue")
    path.write_text(message)


def write_host_info(path: Path):
    path.write_text(run_and_log_args(["uname", "-a"]).stdout)


def get_version(binary) -> Optional[str]:
    if not has_command(binary):
        return None
    for command in ("--version", "-V", "version"):
        result = subprocess.run([binary, command], capture_output=True, text=True)
        if not result.returncode and (output := (result.stdout or result.stderr).strip()):
            return output


def check_pipx_package_provides_binary(package: str, binary: str):
    if path := get_first_binary(binary):
        return os.path.join("pipx", "venvs", package, "bin", binary) in str(
            Path(path).expanduser().resolve()
        )
    else:
        return False


def get_version_pip(package):
    pip_binary = get_first_binary("pip", "pip3")
    packages = json.loads(run([pip_binary, "list", "--format", "json"]).stdout)
    return next((x for x in packages if x["name"] == package), {}).get("version")


def get_versions():
    versions = {}
    for binary in BINARIES:
        versions[binary] = get_version(binary)
        click.secho(f"Found {binary} with version {versions[binary]}", fg="blue")
    return versions


def get_versions_pip():
    pip_versions = {}
    for pip_package in PIP_PACKAGES:
        pip_versions[pip_package] = get_version_pip(pip_package)
        click.secho(
            f"Found Pip package {pip_package} with version {pip_versions[pip_package]}",
            fg="blue",
        )
    return pip_versions


def write_versions(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(f"{k}\t\t{v}" for k, v in get_versions().items()))


def write_versions_pip(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(f"{k}\t\t{v}" for k, v in get_versions_pip().items()))


def logs_dir(temp_dir: Path) -> Path:
    return temp_dir / f"sym_logs_{datetime.now().date()}_{round(time.time())}"


def zip_logs(doctor_dir: Path) -> Path:
    zip = SymConfigFile(file_name=f"doctor/logs/{doctor_dir.name}")
    shutil.make_archive(str(zip.path), format="zip", root_dir=str(doctor_dir))
    return zip.path.with_suffix(".zip")


def deliver_logs(client: SAMLClient, output_dir: Path, zip: Path):
    output = output_dir / zip.name
    zip.link_to(output)

    try:
        put_file(
            client, BUCKET, zip, f"{Config.get_org()}/{Config.get_handle()}/{zip.name}"
        )
    except Exception as e:
        click.secho(f"Failed to upload logs: {e}", fg="red")

    return output


def run_and_log_args(args, **kwargs):
    return run(args, log=True, **kwargs)


def run(args, log=False, **kwargs):
    if log:
        click.secho(f"Running {shlex.join(args)}", fg="blue")
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


def get_first_binary(*args):
    which_lines = run(["which", *args]).stdout.splitlines()
    return which_lines[0] if which_lines else None


def get_server_logs(client, doctor_dir: Path, instance: str):
    click.secho(f"Getting server logs from {instance}", fg="blue", bold=True)

    dest_dir = doctor_dir / "server_logs"
    dest_dir.mkdir(parents=True, exist_ok=True)

    ssh_user = get_ssh_user()
    ssh_bin = str(create_ssh_bin(client))
    ssh_key, _ = ssh_key_and_config(client)

    for dir in REMOTE_LOG_DIRS:
        ssh_commands = [
            f"mkdir -p /tmp/sym{dir}",
            f"sudo cp -r {dir}/ /tmp/sym{dir}",
            f"sudo chmod -R a+rw /tmp/sym{dir}",
        ]
        run_and_log_args(
            ["sym", "ssh", client.resource, instance, "; ".join(ssh_commands)]
        )

        run_and_log_args(
            [
                "scp",
                "-r",
                "-i",
                str(ssh_key),
                "-S",
                str(ssh_bin),
                f"{ssh_user}@{instance}:/tmp/sym{dir}",
                str(dest_dir),
            ]
        )

        ssh_commands = [
            f"cd /tmp/sym",
            f"rm -r /tmp/sym{dir}",
        ]
        run_and_log_args(
            ["sym", "ssh", client.resource, instance, "; ".join(ssh_commands)]
        )


def get_versions_from_server(client, doctor_dir: Path, instance: str):
    click.secho(f"Getting server version info from {instance}", fg="blue", bold=True)
    ssh_commands = [
        f"snap list amazon-ssm-agent",
        f"ssh -V 2>&1",
    ]
    res = run_and_log_args(
        ["sym", "ssh", client.resource, instance, "; ".join(ssh_commands)]
    )
    (doctor_dir / "server_versions.txt").write_text(res.stdout)


class DoctorRunner:
    def __init__(self, client: SAMLClient, doctor_dir: Path, timeout: int):
        self.client = client
        self.doctor_dir = doctor_dir
        self.timeout = timeout

    def run_with_timeout(self, args):
        return run_and_log_args(args, timeout=self.timeout)

    def write_error_logs(self, result, name: str = None):
        name = name or result.args[0]
        (self.doctor_dir / f"{name}_error_stdout.log").write_text(result.stdout)
        (self.doctor_dir / f"{name}_error_stderr.log").write_text(result.stderr)

    def write_temp_file(self, filename: str, content: str):
        path = self.doctor_dir.parent / filename
        path.write_text(content)
        return path


class AnsibleDoctorRunner(DoctorRunner):
    def run(self, inventory: Optional[str], playbook: Optional[str]):
        if not playbook:
            playbook = str(self.write_temp_file("playbook.yml", TEST_PLAYBOOK))

        args = ["sym", "ansible-playbook", self.client.resource]
        if inventory:
            args.extend(["-i", inventory])
        args.append(playbook)

        try:
            result = self.run_with_timeout(args)
        except subprocess.TimeoutExpired:
            click.secho("ansible check timed out", fg="red")
            return

        if match := INSTANCE_PATTERN.search(result.stdout):
            get_server_logs(self.client, self.doctor_dir, match[1])
            get_versions_from_server(self.client, self.doctor_dir, match[1])
        else:
            self.write_error_logs(result, name="ansible_playbook")
            click.secho(f"Found no servers from which to retrieve logs", fg="red")
