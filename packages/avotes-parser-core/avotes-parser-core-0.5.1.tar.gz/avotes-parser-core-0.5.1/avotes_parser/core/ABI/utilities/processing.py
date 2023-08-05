"""
Decoding functions callings to human-readable format.
"""
from typing import Dict, List, Any

from sha3 import keccak_256

from ..storage import (
    ABI_T, FuncStorage
)


# ============================================================================
# ========================= Utilities ========================================
# ============================================================================

def _get_encoded_signature(func_name: str, input_types: List[str]) -> str:
    """
    Encode signature of function according to the ABI specification.

    :param func_name: str, function name
    :param input_types: List[str], list with inputs types for function.
    :return: str, first fours bytes of encoded function.

    The result of encoding is:

    keccak256('func_name(input_type1,input_type2,...)')
    """
    input_types = ','.join(input_types)
    signature = f'{func_name}({input_types})'
    keccak = keccak_256()
    keccak.update(signature.encode('ascii'))
    return f'0x{keccak.hexdigest()[:8]}'


def _gather_types(inputs: List[Dict[str, Any]]) -> List[str]:
    """
    Parse input json ABI description for function input types.

    :param inputs: List[Dict[str, Any]], 'inputs' entry of a json description.
    :return: List[str], gathered types.
    """

    def __extract_type(entity: Dict[str, Any]) -> str:
        if 'components' in entity:
            t = ','.join(_gather_types(
                entity['components']
            ))
            return f'({t})'

        return entity.get('type', 'unknown')

    return [
        __extract_type(inp)
        for inp in inputs
    ]


def index_function_description(
        contract_abi: ABI_T
) -> FuncStorage:
    """Create mapping from function signatures to function descriptions."""

    def __is_function(entity: Dict[str, Any]) -> bool:
        t = entity.get('type', 'unknown')
        if t == 'function' or t == 'receive':
            return True

        return False

    return {
        _get_encoded_signature(
            entry.get('name', 'unknown'),
            _gather_types(entry.get('inputs', []))
        ): entry
        for entry
        in filter(
            __is_function, contract_abi
        )
    }
