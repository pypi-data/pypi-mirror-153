from sym.cli.helpers.global_options import GlobalOptions

from ..errors import SAMLClientNotFound
from .saml_client import SAMLClient


class SAMLClientFactory:
    @classmethod
    def create_saml_client(cls, resource: str, options: GlobalOptions) -> SAMLClient:
        """Returns an initialized SAML Client, either from a cache based on the
        resource name, or by initializing a new one based on the type specified
        in the options provided.
        """
        if not options.saml_client_type:
            raise SAMLClientNotFound()

        saml_client = options.saml_clients.get(resource, None)

        if saml_client is None:
            saml_client = options.saml_client_type(resource, options=options)
            options.saml_clients[resource] = saml_client

        return saml_client

    @classmethod
    def clone(cls, client: SAMLClient, **option_overrides) -> SAMLClient:
        """Create a new SAMLClient with the same setup as the provided
        client, with option overrides from **kwargs.

        Args:
            client: SAMLClient to clone
            option_overrides: key/value pairs to override in client options
        """

        return client.clone(options=client.options.clone(**option_overrides))
