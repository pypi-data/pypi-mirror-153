"""
Storage with cache for results of provider calling.
"""
from typing import (
    Generic, TypeVar,
    Callable, Dict,
    Any, List
)
from collections import namedtuple

_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

_ProviderT = Callable[[_KT], _VT]
_StorageT = Dict[_KT, _VT]


class CachedStorage(Generic[_KT, _VT]):
    """
    Cache for results of provider calling.
    """

    def __init__(self, provider: _ProviderT):
        """Create empty cache."""
        self._provider = provider
        self._storage: _StorageT = {}

    def _get_from_provider(self, key: _KT) -> _VT:
        return self._provider(key)

    def __getitem__(self, key: _KT) -> _VT:
        """Get value from cache or provider."""
        if key not in self:
            self._storage[key] = self._get_from_provider(key)

        return self._storage[key]

    def __contains__(self, key: _KT) -> bool:
        """Check existence of key in cache."""
        return key in self._storage

    def __len__(self) -> int:
        """Return number of elements in cache."""
        return len(self._storage)


ABI_T = List[Dict[str, Any]]

_FunctionSignature = str
_FunctionDescription = Dict[str, Any]
FuncStorage = Dict[_FunctionSignature, _FunctionDescription]

ABIKey = namedtuple(
    'ABIKey', field_names=['ContractAddress', 'FunctionSignature'],
    rename=False
)
ABI = namedtuple(
    'ABI', field_names=['raw', 'func_storage'], rename=False
)
