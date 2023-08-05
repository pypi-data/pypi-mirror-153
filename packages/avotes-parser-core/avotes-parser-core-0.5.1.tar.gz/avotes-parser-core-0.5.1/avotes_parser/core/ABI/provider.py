"""
Base class for ABI hierarchy.
"""
import logging
from abc import ABC, abstractmethod
from typing import Tuple

from .storage import (
    ABIKey, ABI,
    CachedStorage
)
from .utilities.etherscan import (
    get_abi, get_implementation_address, DEFAULT_NET
)
from .utilities.exceptions import (
    ABILocalNotFound, ABIEtherscanNetworkError,
    ABIEtherscanStatusCode, ABIResolvingError
)
from .utilities.local import (
    get_all_files, read_abi_from_json
)
from .utilities.processing import (
    index_function_description
)


# ============================================================================
# ============================== ABI =========================================
# ============================================================================


class ABIProvider(ABC):
    """
    Base class for ABI providers.
    """

    def __call__(self, key: ABIKey) -> ABI:
        """Return ABI for key."""
        return self.get_abi(key)

    @abstractmethod
    def get_abi(self, key: ABIKey) -> ABI:
        """Return ABI."""
        pass


class ABIProviderEtherscanAPI(ABIProvider):
    """
    Getting ABI from Etherscan API.
    """

    def __init__(self, api_key: str, net: str = DEFAULT_NET):
        """Prepare provider with concrete APi key and net."""
        self._api_key = api_key
        self._net = net

        self._retries = 3

    def get_abi(self, key: ABIKey) -> ABI:
        """
        Return ABI from Etherscan API.

        :param key: str, address of contract.
        :return: abi
        :exception ABIEtherscanNetworkError in case of error at network layer.
        :exception ABIEtherscanStatusCode in case of error in api calls.
        """
        abi = get_abi(
            self._api_key, key.ContractAddress,
            self._net, self._retries
        )

        proxy_type_code = 1
        implementation_code = 2

        status = 0
        for entry in abi:
            name = entry.get('name', 'unknown')

            if name == 'proxyType':
                status |= proxy_type_code
            elif name == 'implementation':
                status |= implementation_code

            if status == 3:
                logging.debug(
                    f'Proxy punching for {key} '
                    f'in {self._net}'
                )
                address = get_implementation_address(
                    key.ContractAddress, abi, self._net
                )
                abi = get_abi(
                    self._api_key, address,
                    self._net, self._retries
                )
                break

        return ABI(raw=abi, func_storage=index_function_description(abi))


class ABIProviderLocalDirectory(ABIProvider):
    """
    Getting ABI from local files of interfaces.
    """

    def __init__(self, interfaces_directory: str):
        """Prepare mapping from files names to paths."""
        interfaces = get_all_files(
            interfaces_directory, '*.json'
        )

        self._interfaces = {}
        for interface in interfaces.values():
            abi = read_abi_from_json(interface)
            indexed_func_descriptions = index_function_description(
                abi
            )
            for sign in indexed_func_descriptions:
                self._interfaces[sign] = ABI(
                    raw=abi,
                    func_storage=indexed_func_descriptions
                )

    def get_abi(self, key: ABIKey) -> ABI:
        """
        Return ABI from interface file.

        :param key: str, name of interface file.
        :return: abi
        :exception ABILocalNotFound in case of interface file does not
                   exist.
        """
        if key.FunctionSignature in self._interfaces:
            return self._interfaces[key.FunctionSignature]

        raise ABILocalNotFound(key.FunctionSignature)


class ABIProviderCombined(
    ABIProviderEtherscanAPI, ABIProviderLocalDirectory
):
    """
    Combined getting ABI.

    Try to get ABI from Etherscan API.
    In case of failure, read ABI from local file.
    """

    def __init__(self, api_key: str, net: str, interfaces_directory: str):
        """Prepare instances of API and local files providers."""
        ABIProviderEtherscanAPI.__init__(self, api_key, net)
        ABIProviderLocalDirectory.__init__(self, interfaces_directory)

    def get_abi(self, key: ABIKey) -> ABI:
        """
        Return ABI.

        :param key: Tuple[str, str], pair of address of contract
                                     and interface file.
        :return: abi
        :exception ABIResolvingError in case of resolving through all ways is
                   failed.
        """
        try:
            return ABIProviderEtherscanAPI.get_abi(self, key)
        except (ABIEtherscanNetworkError, ABIEtherscanStatusCode) as err:
            logging.debug(f'Fail on resolving ABI trough API: {str(err)}')

        try:
            return ABIProviderLocalDirectory.get_abi(self, key)
        except ABILocalNotFound as err:
            logging.debug(f'Fail on resolving ABI trough local directory: '
                          f'{str(err)}')

        raise ABIResolvingError()


def get_cached_etherscan_api(
        api_key: str, net: str
) -> CachedStorage[ABIKey, ABI]:
    """
    Return prepared instance of CachedStorage with API provider.

    :param api_key: str, Etherscan API token.
    :param net: str, the name of target network.
    :return: CachedStorage[ABIKey, ABI]
    """
    return CachedStorage(ABIProviderEtherscanAPI(api_key, net))


def get_cached_local_interfaces(
        interfaces_directory: str
) -> CachedStorage[ABIKey, ABI]:
    """
    Return prepared instance of CachedStorage with local files provider.

    :param interfaces_directory: str, path to directory with interfaces.
    :return: CachedStorage[ABIKey, ABI]
    """
    return CachedStorage(ABIProviderLocalDirectory(interfaces_directory))


def get_cached_combined(
        api_key: str, net: str,
        interfaces_directory: str
) -> CachedStorage[Tuple[ABIKey, ABIKey], ABI]:
    """
    Return prepared instance of CachedStorage with combined provider.

    :param api_key: str, Etherscan API token.
    :param net: str, the name of target network.
    :param interfaces_directory: str, path to directory with interfaces.
    :return: CachedStorage[ABIKey, ABI]
    """
    return CachedStorage(ABIProviderCombined(
        api_key, net, interfaces_directory
    ))
