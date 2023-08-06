from platon_hash.backends.auto import (
    AutoBackend,
)
from platon_hash.main import (
    Keccak256,
)

keccak = Keccak256(AutoBackend())
