from sym.cli.saml_clients.saml_client import SAMLClient

from .cache import CachingEc2Client
from .client import Ec2Client


def get_ec2_client(client: SAMLClient) -> Ec2Client:
    return CachingEc2Client(client)
