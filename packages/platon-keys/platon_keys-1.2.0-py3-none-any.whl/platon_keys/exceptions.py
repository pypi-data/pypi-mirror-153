# This exposes the platon-utils exception for backwards compatibility,
# for any library that catches platon_keys.exceptions.ValidationError
from platon_utils import ValidationError  # noqa: F401


class BadSignature(Exception):
    pass
