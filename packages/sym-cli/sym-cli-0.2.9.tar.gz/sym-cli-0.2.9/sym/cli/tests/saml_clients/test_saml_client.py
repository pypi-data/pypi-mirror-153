import pytest

from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients.saml_client import SAMLClient

TEST_RESOURCE = "foobar"


class BasicTestClient(SAMLClient):
    def _ensure_config(self, profile: "Profile") -> "ConfigParser":
        pass

    def is_setup(self) -> bool:
        return True

    def _exec(self, *args: str, **opts: str) -> None:
        pass


class TestSAMLClient:
    """SAMLClient abstract class testing suite. Uses the BasicSAMLClient class
    to test the base methods.

    To run the tests you may, from the runtime/sym-cli project folder:
    - Run the entire test suite:
        python -m pytest sym/cli/tests/saml_clients/test_saml_client.py

    - Run a single test method:
        python -m pytest sym/cli/tests/saml_clients/test_saml_client.py::TestSAMLClient::test_missing_arn_errors
    """

    def test_testing_client_not_included_in_sorted_subclasses(self):
        subclasses = SAMLClient.sorted_subclasses()
        assert subclasses
        assert BasicTestClient not in subclasses

    def test_missing_arn_errors(self):
        with pytest.raises(ValueError) as exception_info:
            client = BasicTestClient(resource=TEST_RESOURCE, options=GlobalOptions())
            client.resource_from_arn(None)

        assert exception_info.match("missing ARN")
