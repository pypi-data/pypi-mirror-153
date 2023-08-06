from .params import get_profile


def validate_resource(resource: str):
    try:
        get_profile(resource)
        return True
    except KeyError:
        return False


def validate_bool_str(bool_str: str):
    return bool_str.lower() in {"true", "false"}
