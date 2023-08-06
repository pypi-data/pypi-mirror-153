from platon_typing import (
    Address,
)
from platon_utils import (
    keccak,
)


def public_key_to_address(public_key_bytes: bytes) -> Address:
    return keccak(public_key_bytes)[-20:]
