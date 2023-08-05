"""
Exceptions on ABI extraction.
"""


# ============================================================================
# =========================== ABI exceptions =================================
# ============================================================================


class ABIResolvingError(IOError):
    """
    The base type for exceptions ot ABI getting.
    """

    pass


class ABIEtherscanNetworkError(ABIResolvingError):
    """
    Exception while calling Etherscan API.
    """

    pass


class ABIEtherscanStatusCode(ABIResolvingError):
    """
    Etherscan API return failure status code.
    """

    def __init__(self, status_code: str, message: str, result: str):
        """Get error info and forward formatted message to super"""
        msg = f'Code: {status_code}. ' \
              f'Message: {message}. ' \
              f'Result: {result}.'
        super().__init__(msg)


class ABILocalNotFound(ABIResolvingError):
    """
    File with ABI definition was not found.
    """

    def __init__(self, target_file: str):
        """Prepare and forward error message."""
        msg = f'Local ABI definition was not found: {target_file}.'
        super().__init__(msg)
