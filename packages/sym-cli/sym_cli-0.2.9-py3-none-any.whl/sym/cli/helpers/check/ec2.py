import json

from sym.cli.errors import BotoError, CliError, InstanceNotFound
from sym.cli.helpers.boto import get_identity
from sym.cli.helpers.ec2.factory import get_ec2_client
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from .model import CheckContext, CheckResult, SymCheck, failure, success


class CallerIdentityCheck(SymCheck):
    def check(self, ctx: CheckContext) -> CheckResult:
        client = SAMLClientFactory.create_saml_client(ctx.resource, ctx.options)
        try:
            identity = get_identity(client)
            pretty = json.dumps(identity, indent=4, sort_keys=True)
            return success(f"Successfully got AWS identity:\n{pretty}")
        except CliError as e:
            return failure(f"Unable to get AWS identity: {e.message}")


class DescribeRegionsCheck(SymCheck):
    def check(self, ctx: CheckContext) -> CheckResult:
        client = SAMLClientFactory.create_saml_client(ctx.resource, ctx.options)

        try:
            ctx.regions = get_ec2_client(client).get_regions()
            return success(f"Found {len(ctx.regions)} regions")
        except BotoError as e:
            return failure(f"Unable to describe regions: {e.message}")


class DescribeInstanceCheck(SymCheck):
    def __init__(self, instance: str):
        self.instance = instance

    def check(self, ctx: CheckContext) -> CheckResult:
        client = SAMLClientFactory.create_saml_client(ctx.resource, ctx.options)
        try:
            running_instance = get_ec2_client(client).load_instance_by_alias(
                self.instance
            )
            return success(
                f"Located instance {running_instance.instance_id} in region {running_instance.region}"
            )
        except InstanceNotFound as e:
            return failure(f"{e.message}")
