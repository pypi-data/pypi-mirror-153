from configparser import ConfigParser
from contextlib import contextmanager
from copy import copy
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import ANY, patch

import pytest
from expects import expect, have_keys
from sym.shared.cli.tests.conftest import _env_str

from sym.cli.actions.write_creds_action import WriteCredsAction
from sym.cli.data.request_data import RequestData
from sym.cli.errors import CliError, InvalidResource, MissingResource
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.sandbox import Sandbox

TEST_PROFILE = "foobar-9000"
TEST_RESOURCE = "test"

# mapping of keys stored in .aws/credentials to internal keys
# in the case they're different, as we change some during write_creds
CRED_KEYS_MAPPING = {
    "REGION": "AWS_REGION",
    "X_SECURITY_TOKEN_EXPIRES": "AWS_CREDENTIAL_EXPIRATION",
}


class TestWriteCreds:
    """write_creds testing suite.

    Includes tests for click commands / user interaction
    and the internal module code separately.

    This class is broken into 2 distinct parts:
        1. pytest test cases
        2. pytest fixture and data creation helper methods

    To run the tests you may, from the runtime/sym-cli project folder:
    - Run the entire test suite:
        python -m pytest sym/cli/tests/commands/test_write_creds.py

    - Run a single test method:
        python -m pytest sym/cli/tests/commands/test_write_creds.py::TestWriteCreds::test_execute_write_creds
    """

    def test_execute_write_creds(self, setup, credentials_path, creds_env):
        with setup():
            global_options = GlobalOptions(saml_client_type=AwsOkta)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": str(credentials_path), "profile": TEST_PROFILE},
            )
            action = WriteCredsAction()
            action.execute(request_data)

            written_creds = self.get_credentials_from_file(credentials_path, TEST_PROFILE)
            expect(written_creds).to(have_keys(creds_env))

    def test_execute_write_creds_session_length(self, setup, credentials_path, creds_env):
        with setup():
            global_options = GlobalOptions(saml_client_type=AwsOkta, session_length=60)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": str(credentials_path), "profile": TEST_PROFILE},
            )
            action = WriteCredsAction()
            action.execute(request_data)

            written_creds = self.get_credentials_from_file(credentials_path, TEST_PROFILE)
            expect(written_creds).to(have_keys(creds_env))

    @patch("sym.cli.saml_clients.saml_client.SAMLClient.write_creds")
    def test_execute_write_creds_prefix(self, mock_write_creds, setup, credentials_path):
        with setup():
            global_options = GlobalOptions(saml_client_type=AwsOkta)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": credentials_path, "prefix": "foo"},
            )
            action = WriteCredsAction()
            action.execute(request_data)

            mock_write_creds.assert_called_once_with(
                path=credentials_path,
                profile=f"foo-{TEST_RESOURCE}",
            )

    def test_execute_write_creds_without_aws_okta_fails(self, setup, credentials_path):
        with pytest.raises(CliError, match="Unable to find aws-okta in your path!"):
            with setup(create_binary=False):
                global_options = GlobalOptions(saml_client_type=AwsOkta)

                request_data = RequestData(
                    action="write_creds",
                    resource=TEST_RESOURCE,
                    global_options=global_options,
                    params={"path": str(credentials_path), "profile": TEST_PROFILE},
                )
                action = WriteCredsAction()
                action.execute(request_data)

    @patch("sym.cli.saml_clients.saml_client.SAMLClient._ensure_session")
    def test_execute_write_creds_expiring_force_ensures_session(
        self,
        mock_ensure_session,
        setup,
        credentials_path,
        creds_env,
    ):
        creds = copy(creds_env)
        creds["AWS_OKTA_SESSION_EXPIRATION"] = str(int(datetime.now().timestamp()))

        with setup(creds=creds):
            global_options = GlobalOptions(saml_client_type=AwsOkta)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": str(credentials_path), "profile": TEST_PROFILE},
            )

            action = WriteCredsAction()
            action.execute(request_data)

            mock_ensure_session.assert_called_once_with(force=True)

            written_creds = self.get_credentials_from_file(credentials_path, TEST_PROFILE)

            # Ideally we'd like to make sure the written_creds expiration is in
            # the future, not what we set as creds["AWS_OKTA_SESSION_EXPIRATION"],
            # but since we stub the subprocess, we can't get updated creds.
            # So the real test here is _ensure_session.assert_called and this check
            # is extra.
            expect(written_creds).to(have_keys(creds))

    @patch(
        "sym.cli.saml_clients.saml_client.SAMLClient._profile_matches_caller_identity",
        return_value=False,
    )
    @patch("sym.cli.saml_clients.saml_client.SAMLClient._ensure_session")
    def test_execute_write_creds_profile_mismatch_force_ensures_session(
        self,
        mock_ensure_session,
        mock_profile_match,
        setup,
        credentials_path,
        creds_env,
    ):
        creds = creds_env.copy()
        # _profile_matches_caller_identity doesn't get called if creds are expiring
        future_datetime = datetime.now() + timedelta(minutes=30)
        creds["AWS_OKTA_SESSION_EXPIRATION"] = str(int(future_datetime.timestamp()))

        with setup(creds=creds):
            global_options = GlobalOptions(saml_client_type=AwsOkta)

            request_data = RequestData(
                action="write_creds",
                resource=TEST_RESOURCE,
                global_options=global_options,
                params={"path": str(credentials_path), "profile": TEST_PROFILE},
            )

            action = WriteCredsAction()
            action.execute(request_data)

            mock_profile_match.assert_called_once()
            mock_ensure_session.assert_called_once_with(force=True)

            written_creds = self.get_credentials_from_file(credentials_path, TEST_PROFILE)

            expect(written_creds).to(have_keys(creds))

    def test_write_creds_no_login_errors(self, command_login_tester):
        command_login_tester(["write-creds"])
        command_login_tester(["write-creds", TEST_RESOURCE])
        command_login_tester(["write-creds"], {"SYM_RESOURCE": TEST_RESOURCE})
        command_login_tester(["write-creds"], {"ENVIRONMENT": TEST_RESOURCE})

    def test_good_error_message(self, sandbox, click_setup, credentials_path):
        # NOTE: It's important to have good error messages.
        # If you break these tests, it's a genuine failure and you must fix it.

        sandbox.create_binary("bin/aws")
        sandbox.create_binary("bin/session-manager-plugin")

        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["write-creds", "--path", credentials_path],
            )
            assert "You must supply a resource" in result.output
            assert "These are the resources available to you:" in result.output
            assert result.exit_code == MissingResource.exit_code

            result = runner.invoke(
                click_command,
                ["write-creds", "--path", credentials_path, "invalid"],
            )
            assert "Invalid resource" in result.output
            assert "These are the resources available to you:" in result.output
            assert result.exit_code == InvalidResource.exit_code

    @patch.object(WriteCredsAction, "write_creds")
    def test_write_creds_command_executes_correct_action_with_params(
        self,
        mock_write_creds,
        setup,
        simple_command_tester,
        credentials_path,
        sandbox,
    ):
        with setup():
            sandbox.create_binary(f"bin/aws")
            sandbox.create_binary(f"bin/session-manager-plugin")

            result = simple_command_tester(
                [
                    "write-creds",
                    TEST_RESOURCE,
                    "--profile",
                    TEST_PROFILE,
                    "--path",
                    str(credentials_path),
                ],
            )

            assert result.exit_code == 0
            mock_write_creds.assert_called_once_with(
                TEST_RESOURCE,
                ANY,
                str(credentials_path),
                TEST_PROFILE,
                "sym",
            )

    ##############################################################################################
    # SECTION 2
    # pytest fixture and testing data preparation
    # and data creation helper methods
    #
    ##############################################################################################

    @pytest.fixture
    def credentials_path(self, sandbox: Sandbox):
        """Create `.aws/credentials` file in the sandbox environment
        and return the path.
        """

        credentials_path = sandbox.path / ".aws" / "credentials"

        try:
            credentials_path.parent.mkdir(parents=True)
            credentials_path.touch()
        except FileExistsError:
            # Allow tests to use this fixture to get the path even
            # if they've already used this fixture to create the file.
            pass

        return credentials_path

    def get_credentials_from_file(self, path: Path, profile: str) -> dict:
        """Read AWS credentials file at path and return all creds
        for the provided profile as a dict.

        Does some replacements to reverse changes we make when writing
        credentials to the file so it can be compared to internal dicts
        like the creds_env fixture easily.
        """

        config = ConfigParser(strict=False)
        with open(path) as f:
            config.read_file(f)

        creds = config.items(profile)
        creds_dict = {k.upper(): v for k, v in creds}

        for file_key_name, internal_key_name in CRED_KEYS_MAPPING.items():
            val = creds_dict.pop(file_key_name)
            creds_dict[internal_key_name] = val

        return creds_dict

    @pytest.fixture
    def setup(self, capture_command, no_click_setup, creds_env):
        @contextmanager
        def _setup(create_binary=True, creds=creds_env):
            with no_click_setup(set_client=create_binary):
                with capture_command():
                    capture_command.register_output(r"env", _env_str(creds))
                    yield

        return _setup
