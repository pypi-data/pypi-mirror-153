from typing import Type

import pytest

from sym.cli.errors import SAMLClientNotFound
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.saml_clients.chooser import SAMLClientName, choose_saml_client
from sym.cli.saml_clients.saml2aws import Saml2Aws
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.mark.parametrize(
    argnames=("saml_client_name", "make_saml2aws", "expected"),
    argvalues=[
        ("auto", True, Saml2Aws),
        ("aws-profile", False, AwsProfile),
        ("aws-profile", True, AwsProfile),
        ("aws-okta", False, AwsOkta),
        ("aws-okta", True, AwsOkta),
        ("saml2aws", False, Saml2Aws),
        ("saml2aws", True, Saml2Aws),
    ],
)
def test_chooser_selects_available_saml_client(
    sandbox: Sandbox,
    saml_client_name: SAMLClientName,
    make_saml2aws: bool,
    expected: Type[SAMLClient],
) -> None:
    if make_saml2aws:
        sandbox.create_file("bin/saml2aws", 0o755)
    with sandbox.push_exec_path():
        assert choose_saml_client(saml_client_name) == expected


def test_chooser_auto_no_client_installed_raises_exception(sandbox: Sandbox):
    with pytest.raises(SAMLClientNotFound):
        with sandbox.push_exec_path():
            choose_saml_client("auto")
