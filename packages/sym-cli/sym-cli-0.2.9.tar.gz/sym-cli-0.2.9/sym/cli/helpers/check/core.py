from sym.shared.cli.helpers.os import has_command

from sym.cli.errors import SAMLClientNotFound
from sym.cli.helpers.config import Config
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from .model import CheckContext, CheckResult, SymCheck, failure, success

# TODO: these error messages are quite terrible, and should
# be replaced with the existing ones in errors.py and decorators.py.


class LoginCheck(SymCheck):
    def check(self, _: CheckContext) -> CheckResult:
        if Config.is_logged_in():
            return success(f"Logged in as: {Config.get_email()} ({Config.get_org()})")
        else:
            return failure(f"Not logged in!")


class DependenciesCheck(SymCheck):
    def __init__(self, binary: str):
        self.binary = binary

    def check(self, _: CheckContext) -> CheckResult:
        if has_command(self.binary):
            return success(f"Found on path: {self.binary}")
        else:
            return failure(f"Could not find binary on path: {self.binary}")


class ResourceCheck(SymCheck):
    def check(self, ctx: CheckContext) -> CheckResult:
        try:
            client = SAMLClientFactory.create_saml_client(ctx.resource, ctx.options)
            msg = f"Created client with {client.binary} for resource {ctx.resource}"
            msg += "\nUsing config: " + str(client.config_file.path)
            msg += "\n" + client.config_file.read()

            return success(msg)
        except SAMLClientNotFound as e:
            return failure(
                f"Unable to create client: {ctx.options.saml_client_type} not found"
            )
