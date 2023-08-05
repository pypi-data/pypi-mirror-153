"""
Parsing payload of aragon votes.
"""
import json
from dataclasses import dataclass, field, asdict
from typing import Tuple, List

from .pretty_printed import PrettyPrinted
from .spec import (
    LENGTH_SPEC_ID, LENGTH_ADDRESS,
    LENGTH_METHOD_ID, HEX_PREFIX,
    DEFAULT_SPEC_ID, LENGTH_DATA_LEN,
    add_hex_prefix, PRETTY_PRINT_NEXT_LEVEL_OFFSET
)


# ============================================================================
# =========================== Parsing stage exceptions =======================
# ============================================================================

class ParseStructureError(TypeError):
    """
    The base type for exceptions at parsing stage.
    """

    pass


class ParseMismatchLength(ParseStructureError):
    """
    Mismatching between expected and received data lengths
    """

    def __init__(self, field_name: str, received: int, expected: int):
        """Get error info and forward formatted message to super"""
        message = f'Length of {field_name} should be: {expected}; ' \
                  f'received: {received}.'
        super().__init__(message)


# ============================================================================
# =========================== Parsing stage structures =======================
# ============================================================================


@dataclass
class EncodedCall(PrettyPrinted):
    """
    Contains fields of the single call from script body.
    """

    # 20 bytes
    address: str
    # 4 bytes
    call_data_length: int
    # 4 bytes
    method_id: str
    # (call_data_length - 4) bytes
    encoded_call_data: str

    def pretty_print(self, *_, **kwargs) -> str:
        """Get human-readable form."""
        offset_size = kwargs.pop('offset', 0)
        offset = PrettyPrinted.get_tabular(offset_size)

        return (
            f'{offset}Encoded function call\n'
            f'{offset}Address: {self.address}\n'
            f'{offset}Call data length: {self.call_data_length}\n'
            f'{offset}Signature: {self.method_id}\n'
            f'{offset}Encoded call data: {self.call_data_length}'
        )

    def __post_init__(self):
        """Check length constraints and perform normalized to hex."""
        if len(self.address) != LENGTH_ADDRESS:
            raise ParseMismatchLength(
                'address', len(self.address), LENGTH_ADDRESS
            )

        if len(self.method_id) != LENGTH_METHOD_ID:
            raise ParseMismatchLength(
                'method id', len(self.method_id), LENGTH_METHOD_ID
            )

        call_data_length_without_method_id = (
                self.call_data_length * 2 - len(self.method_id)  # noqa
        )
        if len(self.encoded_call_data) != call_data_length_without_method_id:
            raise ParseMismatchLength(
                'encoded call data',
                len(self.encoded_call_data),
                call_data_length_without_method_id
            )

        self.address = add_hex_prefix(self.address)
        self.method_id = add_hex_prefix(self.method_id)
        self.encoded_call_data = add_hex_prefix(self.encoded_call_data)

    def __repr__(self) -> str:
        """Get human-readable representation."""
        return self.pretty_print(offset=0)


@dataclass
class EVMScript(PrettyPrinted):
    """
    Contains data of the whole EVM script.
    """

    # Script executor id
    spec_id: str = field(default=DEFAULT_SPEC_ID)
    # Calls data
    calls: List[EncodedCall] = field(default_factory=list)

    def pretty_print(self, *_, **kwargs) -> str:
        """Get human-readable form."""
        offset_size = kwargs.pop('offset', 0)
        offset = PrettyPrinted.get_tabular(offset_size)

        header = (
            f'{offset}EVM script\n'
            f'{offset}Script executor ID: {self.spec_id}'
        )

        calls = '\n'.join((
            call.pretty_print(
                offset=offset_size + PRETTY_PRINT_NEXT_LEVEL_OFFSET,
                **kwargs
            ) if isinstance(call, PrettyPrinted) else repr(call)
            for call in self.calls
        ))
        calls = (
            f'{offset}Calls:\n'
            f'{calls}'
        )

        return (
            f'{header}\n'
            f'{calls}'
        )

    def __post_init__(self):
        """Check length constraints and perform normalized to hex."""
        if len(self.spec_id) != LENGTH_SPEC_ID:
            raise ParseMismatchLength(
                'spec id', len(self.spec_id), LENGTH_SPEC_ID
            )

        self.spec_id = add_hex_prefix(self.spec_id)

    def __repr__(self) -> str:
        """Get human-readable representation."""
        return self.pretty_print(offset=0)

    def to_json(self) -> str:
        """Encode structure into json format."""
        return json.dumps(asdict(self))


# ============================================================================
# =========================== Parsing stage actions ==========================
# ============================================================================

def _parse_single_call(
        encoded_script: str, index: int
) -> Tuple[int, EncodedCall]:
    """Parse one call segment and shift index."""
    address = encoded_script[index: index + LENGTH_ADDRESS]
    index += LENGTH_ADDRESS

    data_length = int(encoded_script[index:index + LENGTH_DATA_LEN], 16)
    index += LENGTH_DATA_LEN

    method_id = encoded_script[index: index + LENGTH_METHOD_ID]
    index += LENGTH_METHOD_ID

    offset = data_length * 2 - LENGTH_METHOD_ID
    call_data = encoded_script[index: index + offset]
    index += offset

    return index, EncodedCall(
        address, data_length, method_id, call_data
    )


def parse_script(encoded_script: str) -> EVMScript:
    """
    Parse encoded EVM script.

    :param encoded_script: str, encoded EVM script.
    :return: parsed script as instance of EVMScript object.
    """
    if encoded_script.startswith(HEX_PREFIX):
        encoded_script = encoded_script[len(HEX_PREFIX):]
    spec_id = encoded_script[:LENGTH_SPEC_ID]

    calls_data = []
    i = LENGTH_SPEC_ID
    while i < len(encoded_script):
        i, one_call = _parse_single_call(encoded_script, i)
        calls_data.append(one_call)

    return EVMScript(
        spec_id, calls_data
    )
