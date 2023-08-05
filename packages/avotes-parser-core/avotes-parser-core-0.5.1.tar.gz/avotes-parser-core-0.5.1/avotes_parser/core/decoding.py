"""
Decoding payload of aragon votes.
"""
from dataclasses import dataclass
from typing import (
    Union, Tuple,
    List, Any,
    Dict, Optional
)

import web3

from .ABI.storage import (
    CachedStorage, ABI, ABIKey
)
from .pretty_printed import PrettyPrinted
from .spec import HEX_PREFIX, PRETTY_PRINT_NEXT_LEVEL_OFFSET


# ============================================================================
# ======================= Decoding stage structures ==========================
# ============================================================================


@dataclass
class FuncInput(PrettyPrinted):
    """
    Single function input
    """

    name: str
    type: str
    value: Any

    def __post_init__(self):
        """Conversion from raw bytes to string for bytes values."""
        if callable(getattr(self.value, 'hex', None)):
            self.value = self.value.hex()

    def pretty_print(self, *_, **kwargs) -> str:
        """Get human-readable representation."""
        offset_size = kwargs.pop('offset', 0)
        offset = PrettyPrinted.get_tabular(offset_size)

        if isinstance(self.value, list):
            value_repr = []
            for entry in self.value:
                if isinstance(entry, PrettyPrinted):
                    entry_repr = entry.pretty_print(
                        offset=offset_size + PRETTY_PRINT_NEXT_LEVEL_OFFSET,
                        **kwargs
                    )
                    value_repr.append(entry_repr)

                else:
                    value_repr.append(str(entry))

            value_repr = '\n'.join(value_repr)
            value_repr = f'[\n{value_repr}\n]'
        else:
            value_repr = str(self.value)

        return f'{offset}{self.name}: {self.type} = {value_repr}'

    def __repr__(self) -> str:
        """Get human-readable representation."""
        return self.pretty_print(offset=0)


@dataclass
class Call(PrettyPrinted):
    """
    Single function call
    """

    contract_address: str
    function_signature: str
    function_name: str
    inputs: List[FuncInput]
    properties: Dict[str, Any]
    outputs: Optional[List[Any]]

    def pretty_print(self, *_, **kwargs) -> str:
        """Get human-readable representation."""
        offset_size = kwargs.pop('offset', 0)
        offset = PrettyPrinted.get_tabular(offset_size)

        header = (
            f'{offset}Function call\n'
            f'{offset}Contract: {self.contract_address}\n'
            f'{offset}Signature: {self.function_signature}\n'
            f'{offset}Name: {self.function_name}'
        )

        inputs = '\n'.join((inp.pretty_print(
            offset=offset_size, **kwargs
        ) if isinstance(
            inp, PrettyPrinted
        ) else repr(inp) for inp in self.inputs))
        inputs = (
            f'{offset}Inputs:\n'
            f'{inputs}'
        )

        return (
            f'{header}\n'
            f'{inputs}'
        )

    def __repr__(self) -> str:
        """Get human-readable representation."""
        return self.pretty_print(offset=0)


# ============================================================================
# ======================= Decoding stage actions =============================
# ============================================================================

_CacheT = CachedStorage[Union[ABIKey, Tuple[ABIKey, ABIKey]], ABI]


def decode_function_call(
        contract_address: str, function_signature: str,
        call_data: str, abi_storage: _CacheT
) -> Optional[Call]:
    """
    Decode function call.

    :param contract_address: str, contract address.
    :param function_signature: str, the first fourth bytes
                                    of function signature
    :param call_data: str, encoded call data.
    :param abi_storage: CachedStorage, storage of contracts ABI.
    :return: Call, decoded description of function calling.
    """
    key = ABIKey(contract_address, function_signature)

    abi = abi_storage[key]
    function_description = abi.func_storage.get(function_signature, None)

    if function_description is None:
        return function_description

    address = web3.Web3.toChecksumAddress(contract_address)
    contract = web3.Web3().eth.contract(
        address=address, abi=abi.raw
    )

    inputs_spec = function_description['inputs']

    if call_data.startswith(HEX_PREFIX):
        call_data = call_data[len(HEX_PREFIX):]

    _, decoded_inputs = contract.decode_function_input(
        f'{function_signature}{call_data}'
    )

    inputs = [
        FuncInput(
            inp['name'],
            inp['type'],
            decoded_inputs[inp['name']]
        )
        for inp in inputs_spec
    ]

    properties = {
        'constant': function_description.get(
            'constant', 'unknown'
        ),
        'payable': function_description.get(
            'payable', 'unknown'
        ),
        'stateMutability': function_description.get(
            'stateMutability', 'unknown'
        ),
        'type': function_description.get(
            'type', 'unknown'
        )
    }

    return Call(
        contract_address, function_signature,
        function_description.get('name', 'unknown'), inputs,
        properties, function_description['outputs']
    )
