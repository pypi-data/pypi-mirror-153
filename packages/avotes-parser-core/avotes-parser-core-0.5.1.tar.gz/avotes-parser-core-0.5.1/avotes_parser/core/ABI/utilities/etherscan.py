"""
Getting contracts ABI through Etherscan API.
"""
import json
import logging
import time
from functools import lru_cache, partial
from typing import Dict, Tuple

import brownie
import requests

from .exceptions import ABIEtherscanNetworkError, ABIEtherscanStatusCode
from ..storage import ABI_T

# ============================================================================
# ===================== Constants ============================================
# ============================================================================

DEFAULT_NET = 'mainnet'
NET_URL_MAP = {
    'mainnet': 'https://api.etherscan.io',
    'goerli': 'https://api-goerli.etherscan.io',
    'kovan': 'https://api-kovan.etherscan.io',
    'rinkebay': 'https://api-rinkeby.etherscan.io',
    'ropsten': 'https://api-ropsten.etherscan.io'
}
SUCCESS = '1'
MINIMUM_RETRIES = 1
CACHE_SIZE = 128


# ============================================================================
# ================================ Utilities =================================
# ============================================================================


@lru_cache(maxsize=CACHE_SIZE)
def _send_query(
        module: str, action: str, api_key: str, address: str,
        retries: int, specific_net: str
) -> str:
    """
    Send query to Etherscan API.

    :param module: str, part of Etherscan API.
    :param action: str, concrete function from API.
    :param api_key: str, API credentials.
    :param address: str, address of target contract.
    :param retries: int, number of retry in case of unsuccessful api call.
    :param specific_net: str, name of target net.
    :return: str, encoded json description of abi.
    :exception ABIEtherscanNetworkError in case of error at network layer.
    :exception ABIEtherscanStatusCode in case of error in api calls.
    """
    retries = max(MINIMUM_RETRIES, retries)

    if specific_net not in NET_URL_MAP:
        raise KeyError(f'Unexpected name of net. '
                       f'Should be one of: '
                       f'{str(NET_URL_MAP.keys())}')

    url = NET_URL_MAP[specific_net]
    parameters = '&'.join([
        f'{name}={value}'
        for name, value in zip(
            ['module', 'action', 'address', 'apikey'],
            [module, action, address, api_key]
        )
    ])
    query = f'{url}/api?{parameters}'

    data = {}
    initial_wait = 0
    increase_wait = 1
    for ind in range(retries):
        logging.debug(
            f'Send query to Etherscan API; retry: {ind + 1}/{retries}; '
            f'sleep for {initial_wait} seconds.'
        )
        time.sleep(initial_wait)

        response = requests.get(query, headers={'User-Agent': ''})
        try:
            response.raise_for_status()
        except requests.HTTPError as err:
            raise ABIEtherscanNetworkError(str(err)) from err

        data = response.json()

        if data['status'] == SUCCESS:
            return data['result']

        initial_wait += increase_wait
        increase_wait *= 2

    raise ABIEtherscanStatusCode(
        status_code=str(data.get('status', -1)),
        message=data.get('message', 'unknown'),
        result=data.get('result', '')
    )


"""Alias for calling getabi functionality."""
_get_contract_abi = partial(_send_query, 'contract', 'getabi')


def get_abi(
        api_key: str, address: str, specific_net: str,
        retries: int = 5
) -> ABI_T:
    """
    Get ABI of target contract by calling to Etherscan API.

    :param api_key: str, API credentials.
    :param address: str, address of target contract.
    :param retries: int, number of retry in case of unsuccessful api call.
    :param specific_net: str, name of target net.
    :return: List[Dict[str, Any]], abi description.
    :exception ABIEtherscanNetworkError in case of error at network layer.
    :exception ABIEtherscanStatusCode in case of error in api calls.
    """
    return json.loads(_get_contract_abi(
        api_key, address, retries, specific_net
    ))


@lru_cache(maxsize=CACHE_SIZE)
def _punched_proxy() -> Dict[Tuple[str, str], str]:
    return dict()


def get_implementation_address(
        proxy_address: str, proxy_abi: ABI_T, specific_net: str
) -> str:
    """Get address from behind proxy."""
    storage = _punched_proxy()
    key = (proxy_address, specific_net)

    if key not in storage:
        if not brownie.network.is_connected():
            # WEB3_INFURA_PROJECT_ID should be set in environment.
            logging.debug(
                f'Connect to {specific_net}.'
            )
            brownie.network.connect(specific_net)

        logging.debug(
            f'Get address of implementation from {proxy_address} '
            f'in {specific_net}.'
        )
        storage[key] = brownie.Contract.from_abi(
            f'ProxyAt{proxy_address}', proxy_address, proxy_abi
        ).implementation()

    return storage[key]
