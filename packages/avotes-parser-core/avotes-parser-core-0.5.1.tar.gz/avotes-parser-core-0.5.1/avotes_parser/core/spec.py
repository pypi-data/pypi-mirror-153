"""
Data specific constants.
"""

# All lengths in numbers of symbols (number of bytes * 2)
CHARS_PER_BYTE = 2
LENGTH_SPEC_ID = 4 * CHARS_PER_BYTE
LENGTH_ADDRESS = 20 * CHARS_PER_BYTE
LENGTH_DATA_LEN = 4 * CHARS_PER_BYTE
LENGTH_METHOD_ID = 4 * CHARS_PER_BYTE

DEFAULT_SPEC_ID = '1'.zfill(LENGTH_SPEC_ID)
HEX_PREFIX = '0x'


def add_hex_prefix(data: str) -> str:
    """Add HEX_PREFIX to the start of a string data."""
    return f'{HEX_PREFIX}{data}'


PRETTY_PRINT_NEXT_LEVEL_OFFSET = 4
