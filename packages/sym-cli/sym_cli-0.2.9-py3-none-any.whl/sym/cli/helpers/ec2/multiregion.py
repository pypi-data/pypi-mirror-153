from threading import Condition, Thread
from typing import Callable, Sequence

import click

from sym.cli.errors import InstanceNotFound
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from .client import Ec2Client, RunningInstance


class MultiRegionEc2Client(Ec2Client):
    """
    A multiregion Ec2 client is able to load instances by alias from any region. Like a normal Ec2
    client, it executes describe-instances on the default region for the SAML client passed to the
    constructor. If that fails, then it calls describe-regions, and searches each region for the instance.
    """

    def __init__(self, client: SAMLClient):
        super().__init__(client)

    def _first(
        self,
        ctx,
        alias: str,
        regions: Sequence[str],
        finder: Callable[[str], RunningInstance],
        timeout=5,
    ) -> RunningInstance:
        """
        Uses the provided function to search each region and returns the first result, or
        raises InstanceNotFound after the timeout is met.

        This is pulled into a helper method to allow "ctx" to be passed in as an arg without a type
        assertion, otherwise the typechecker gets confused.
        """

        results = []
        cv = Condition()

        def search_in_region(region):
            with ctx:
                try:
                    res = finder(region)
                except InstanceNotFound:
                    return
                with cv:
                    results.append(res)
                    cv.notify()

        for region in regions:
            Thread(target=search_in_region, args=(region,), daemon=True).start()

        with cv:
            if cv.wait_for(lambda: bool(results), timeout=timeout):
                return results.pop()

        raise InstanceNotFound(alias)

    def load_instance_by_alias(self, alias: str) -> RunningInstance:
        """
        The MultiRegionEc2Client.load_instance_by_alias method first attempts
        to load the instance from the default region. If that fails with an
        InstanceNotFound error, then start a multi-threaded search for the instance
        across all regions, returning the first instance that is found or raising
        an InstanceNotFound error otherwise.
        """
        try:
            return super().load_instance_by_alias(alias)
        except InstanceNotFound:
            pass

        regions = self.get_regions()

        def find_in_region(region: str) -> RunningInstance:
            new_client = SAMLClientFactory.clone(self.client, aws_region=region)
            new_ec2_client = Ec2Client(new_client)
            return new_ec2_client.load_instance_by_alias(alias)

        ctx = click.get_current_context()
        return self._first(ctx, alias, regions, find_in_region)
