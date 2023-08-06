from unittest.mock import ANY, patch

import pytest
from sym.shared.cli.helpers.config.base import ConfigBase

from sym.cli.decorators import setup_sentry


class TestSetupSentry:
    @pytest.mark.parametrize(
        argnames=("is_prod_mode", "org_name", "expected_environment"),
        argvalues=[
            (True, "sym", "development"),
            (True, "notsym", "pypi"),
            (False, "sym", "development"),
            (False, "notsym", "development"),
        ],
    )
    @patch("sym.shared.cli.decorators.sentry_init")
    def test_sentry_environment(
        self,
        mock_sentry_init,
        is_prod_mode: bool,
        org_name: str,
        expected_environment: str,
        sandbox,
    ):
        with patch("sym.shared.cli.decorators.is_prod_mode", return_value=is_prod_mode):
            with sandbox.push_xdg_config_home():
                ConfigBase.instance()["email"] = f"foo@{org_name}.com"
                setup_sentry()
                mock_sentry_init.assert_called_once_with(
                    environment=expected_environment, sample_rate=ANY
                )
