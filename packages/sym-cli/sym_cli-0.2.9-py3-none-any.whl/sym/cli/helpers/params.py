from typing import Dict, List, NamedTuple, Optional, Tuple, TypedDict

import validators

from ..errors import CliError, InvalidResource, MissingResource
from .config import Config


class Profile(NamedTuple):
    display_name: str
    region: str
    arn: str
    aws_saml_url: Optional[str] = None
    ansible_bucket: Optional[str] = None
    aliases: List[str] = []


class OrgParams(TypedDict, total=False):
    resource_env_var: Optional[str]
    users: Dict[str, str]
    domain: str
    aws_saml_url: str
    aws_okta_params: Dict[str, str]
    saml2aws_params: Dict[str, str]
    profiles: Dict[str, Profile]


# For legacy reasons, we need to maintain multiple org slugs for LD.
# This allows us to put the config in one place.
LaunchDarklyParams: OrgParams = {
    "resource_env_var": "ENVIRONMENT",
    "users": {"ssh": "ubuntu", "ansible": "ansible"},
    "domain": "launchdarkly.com",
    "aws_saml_url": (
        "https://launchdarkly.okta.com/home/amazon_aws/0oaj4aow7gPk26Fy6356/272"
    ),
    "aws_okta_params": {
        "mfa_provider": "OKTA",
        "mfa_factor_type": "auto",
        "assume_role_ttl": "1h",
        "session_ttl": "30m",
    },
    "saml2aws_params": {"mfa": "Auto", "aws_session_duration": "1800"},
    "profiles": {
        "production": Profile(
            display_name="Production",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-production",
            aliases=["prod"],
        ),
        "staging": Profile(
            display_name="Staging",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-staging",
        ),
        "dr": Profile(
            display_name="DR",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-dr",
            ansible_bucket="launchdarkly-sym-ansible-dr",
            aliases=["production_dr"],
        ),
        "dev": Profile(
            display_name="Dev",
            region="us-east-1",
            arn="arn:aws:iam::506919356135:role/ops/SSHAdmin-development",
            ansible_bucket="launchdarkly-sym-ansible-dev",
            aliases=["development"],
        ),
        "shared-services": Profile(
            display_name="Shared Services",
            region="us-east-1",
            arn="arn:aws:iam::061661829416:role/ops/SSHAdmin-shared-services",
            ansible_bucket="launchdarkly-sym-ansible-shared-services",
            aliases=["shared_services"],
        ),
        "catamorphic": Profile(
            display_name="Catamorphic",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-catamorphic",
            ansible_bucket="launchdarkly-sym-ansible-catamorphic",
        ),
        "catamorphic-dr": Profile(
            display_name="Catamorphic DR",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-catamorphic_dr",
            ansible_bucket="launchdarkly-sym-ansible-catamorphic-dr",
            aliases=["catamorphic_dr"],
        ),
        "intuit-production": Profile(
            display_name="Intuit: Production",
            region="us-west-2",
            arn="arn:aws:iam::527291094460:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-intuit-production",
            aliases=["production-intuit", "intuit_production", "intuit_production_use2"],
        ),
        "intuit-dr": Profile(
            display_name="Intuit: DR",
            region="us-east-2",
            arn="arn:aws:iam::527291094460:role/ops/SSHAdmin-intuit-dr",
            ansible_bucket="launchdarkly-sym-ansible-intuit-dr",
            aliases=["intuit_dr"],
        ),
        "intuit-staging": Profile(
            display_name="Intuit: Staging",
            region="us-west-2",
            arn="arn:aws:iam::527291094460:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-intuit-staging",
            aliases=["staging-intuit", "intuit_staging", "intuit_staging_use2"],
        ),
        "production_apac": Profile(
            display_name="Production: APAC",
            region="ap-southeast-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-production",
        ),
        "production_euw1": Profile(
            display_name="Production: EU West 1",
            region="eu-west-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-production",
        ),
        "staging_apac": Profile(
            display_name="Staging: APAC",
            region="ap-southeast-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-staging",
        ),
        "staging_euw1": Profile(
            display_name="Staging: EU West 1",
            region="eu-west-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-staging",
        ),
        "sdk": Profile(
            display_name="SDK",
            region="us-east-1",
            arn="arn:aws:iam::223148043183:role/ops/SSHAdmin-sdk",
            ansible_bucket="launchdarkly-sym-ansible-sdk",
            aliases=["sdk"],
        ),
    },
}

PARAMS: Dict[str, OrgParams] = {
    "launch-darkly": LaunchDarklyParams,
    "launchdarkly": LaunchDarklyParams,
    "sym": {
        "resource_env_var": "ENVIRONMENT",
        "users": {"ssh": "ubuntu", "ansible": "ubuntu"},
        "domain": "symops.io",
        "aws_saml_url": (
            "https://dev-291131.okta.com/home/amazon_aws/0oaqlmsn7GMVgAyBK4x6/272"
        ),
        "aws_okta_params": {
            "mfa_provider": "OKTA",
            "assume_role_ttl": "1h",
            "session_ttl": "30m",
        },
        "saml2aws_params": {"mfa": "Auto", "aws_session_duration": "1800"},
        "profiles": {
            "test": Profile(
                display_name="Test",
                region="us-east-1",
                arn="arn:aws:iam::838419636750:role/SSMTestRole",
                aliases=["this_is_an_alias"],
            ),
            "test_euw1": Profile(
                display_name="Test: EU West 1",
                region="eu-west-1",
                arn="arn:aws:iam::838419636750:role/SSMTestRole",
            ),
            "test-custom": Profile(
                display_name="TestCustom",
                region="us-east-1",
                arn="arn:aws:iam::838419636750:role/SSMTestRoleCustomBucket",
                ansible_bucket="sym-ansible-dev",
                aliases=["test_custom", "test_custom2"],
            ),
        },
    },
    "healthy-health": {
        "resource_env_var": "ENVIRONMENT",
        "users": {"ssh": "ubuntu"},
        "domain": "healthy-health.co",
        "aws_saml_url": (
            "https://healthy-health.okta.com/home/amazon_aws/0oagrj7yFaVtJoI2N5d5/272"
        ),
        "aws_okta_params": {
            "mfa_provider": "OKTA",
            "assume_role_ttl": "1h",
            "session_ttl": "30m",
        },
        "saml2aws_params": {"mfa": "Auto", "aws_session_duration": "1800"},
        "profiles": {
            "prod": Profile(
                display_name="Prod",
                region="us-east-1",
                arn="arn:aws:iam::223440862848:role/ssm-healthy-health-user-prod",
            ),
        },
    },
}


def get_org_params() -> OrgParams:
    return PARAMS[Config.get_org()]


def get_aws_saml_url(resource: str) -> str:
    org_params = get_org_params()
    profile = get_profile(resource)
    return profile.aws_saml_url or org_params["aws_saml_url"]


def get_aws_okta_params() -> Dict[str, str]:
    return get_org_params()["aws_okta_params"]


def get_saml2aws_params() -> Dict[str, str]:
    return get_org_params()["saml2aws_params"]


def get_profiles() -> Dict[str, Profile]:
    return get_org_params()["profiles"]


def get_domain() -> str:
    return get_org_params()["domain"]


def get_ssh_user() -> str:
    return get_org_params()["users"]["ssh"]


def get_ansible_user() -> str:
    return get_org_params()["users"]["ansible"]


def get_resource_env_vars() -> Optional[str]:
    try:
        return ("SYM_RESOURCE", get_org_params()["resource_env_var"])
    except KeyError:
        return "SYM_RESOURCE"


def get_profile_and_name(resource: str) -> Tuple[str, Profile]:
    if not resource:
        raise MissingResource(list(get_profiles().keys()))
    try:
        return next(
            (name, profile)
            for name, profile in get_profiles().items()
            if resource == name or resource in profile.aliases
        )
    except StopIteration:
        raise InvalidResource(resource, list(get_profiles().keys()))


def get_profile(resource: str) -> Profile:
    return get_profile_and_name(resource)[1]


def set_login_fields(org: str, email: str):
    if org not in PARAMS:
        raise CliError(f"Invalid org: {org}")

    config = Config.instance()
    config["org"] = org

    if not validators.email(email):
        raise CliError(f"Invalid email: {email}")

    if (domain := email.split("@")[-1]) != get_domain():
        raise CliError(f"Invalid domain: {domain}")

    config["email"] = email
