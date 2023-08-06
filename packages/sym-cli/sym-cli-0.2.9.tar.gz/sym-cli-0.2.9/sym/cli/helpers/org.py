from typing import Optional

from sym.cli.helpers.params import PARAMS as PARAMS_BY_ORG

_ORGS_BY_DOMAIN = dict(map(lambda kv: (kv[1]["domain"], kv[0]), PARAMS_BY_ORG.items()))


def infer_org_from_email(email: str) -> Optional[str]:
    return _ORGS_BY_DOMAIN.get(email.split("@")[-1])
