from subprocess import CalledProcessError

from sym.cli.helpers.ec2.factory import get_ec2_client
from sym.cli.helpers.ssh import (
    ensure_public_key_on_instance,
    gen_local_ssh_config,
    maybe_gen_ssh_key,
    ssh_key_and_config,
)
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from .model import CheckContext, CheckResult, SymCheck, failure, success


class GenSshConfigCheck(SymCheck):
    def check(self, ctx: CheckContext) -> CheckResult:
        client = SAMLClientFactory.create_saml_client(ctx.resource, ctx.options)
        ssh_config = gen_local_ssh_config(client)
        msg = f"Successfully created local SSH config"
        msg += "\nUsing config: " + str(ssh_config.path)
        msg += "\n" + ssh_config.read()
        return success(msg)


class GenSshKeyCheck(SymCheck):
    def check(self, ctx: CheckContext) -> CheckResult:
        client = SAMLClientFactory.create_saml_client(ctx.resource, ctx.options)
        maybe_gen_ssh_key(client)
        ssh_key, _ = ssh_key_and_config(client)
        msg = "Local SSH keys generated"
        msg += "\nPrivate key: " + str(ssh_key.path)
        pub_key_path = str(ssh_key.path) + ".pub"
        msg += "\nPublic key: " + pub_key_path
        with open(pub_key_path) as f:
            msg += "\n" + f.read()
        return success(msg)


class EnsureSshKeyAuthorizedCheck(SymCheck):
    def __init__(self, instance: str):
        self.instance = instance

    def check(self, ctx: CheckContext) -> CheckResult:
        try:
            client = SAMLClientFactory.create_saml_client(ctx.resource, ctx.options)
            running_instance = get_ec2_client(client).load_instance_by_alias(
                self.instance
            )
            ensure_public_key_on_instance(client, running_instance.instance_id, 22)
            msg = f"Successfully ensured SSH key authorized on instance: {self.instance}"
            if self.instance != running_instance.instance_id:
                msg += f" [{running_instance.instance_id}]"
            return success(msg)
        except CalledProcessError as e:
            msg = f"Error checking SSH on instance {self.instance}: {e}"
            return failure(msg)
