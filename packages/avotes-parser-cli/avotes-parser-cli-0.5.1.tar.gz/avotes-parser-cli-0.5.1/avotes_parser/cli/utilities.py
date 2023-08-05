"""
Utilities and helpers of CLI tool.
"""
import logging
import os
from functools import lru_cache
from mimetypes import guess_type, types_map
from typing import Union, List

import brownie

from avotes_parser.core import (
    Call, decode_function_call, parse_script
)
from avotes_parser.core.ABI.storage import CachedStorage
from avotes_parser.core.ABI.utilities.etherscan import (
    get_implementation_address, get_abi
)
from avotes_parser.core.ABI.utilities.exceptions import (
    ABIEtherscanNetworkError, ABIEtherscanStatusCode
)
from avotes_parser.core.parsing import ParseStructureError


def set_infura_project_id(project_id: str) -> None:
    """Set WEB3_INFURA_PROJECT_ID environment variable."""
    os.environ['WEB3_INFURA_PROJECT_ID'] = project_id


def read_key(path_to: str) -> str:
    """Read Etherscan API key."""
    m_type, _ = guess_type(path_to)
    if m_type == types_map['.txt']:
        with open(path_to, 'r') as api_token_file:
            return api_token_file.read().strip()

    else:
        return path_to


def logging_settings(debug: bool) -> None:
    """Prepare logger."""
    if debug:
        level = logging.DEBUG

    else:
        level = logging.INFO

    logging.basicConfig(
        format='%(levelname)s:%(message)s', level=level
    )


@lru_cache
def get_aragon_voting(
        net: str, address: str,
        etherscan_api_key: str, retries: int,
):
    """Get aragon voting contract as object."""
    if not brownie.network.is_connected():
        brownie.network.connect(net)

    abi = get_abi(etherscan_api_key, address, net, retries)
    impl_address = get_implementation_address(
        address, abi, net
    )
    impl_abi = get_abi(etherscan_api_key, impl_address, net, retries)
    return brownie.Contract.from_abi(
        'AragonVoting', address, impl_abi
    )


def decode_evm_script(
        script: str,
        abi_storage: CachedStorage
) -> List[Union[Call, str]]:
    """
    Parse and decode EVM script.
    """
    try:
        parsed = parse_script(script)
    except ParseStructureError as err:
        return [repr(err)]

    calls = []
    for call in parsed.calls:
        try:
            decoded_call = decode_function_call(
                call.address, call.method_id,
                call.encoded_call_data, abi_storage
            )
            if decoded_call is None:
                calls.append(call)
            else:
                calls.append(decoded_call)
                for inp in decoded_call.inputs:
                    if inp.type == 'bytes' and inp.name == '_evmScript':
                        inp.value = decode_evm_script(inp.value, abi_storage)
                        break

        except (ABIEtherscanNetworkError, ABIEtherscanStatusCode) as err:
            calls.append(f'Network layer error: {repr(err)}')

    return calls


def parse_voting(
        aragon_voting, abi_storage: CachedStorage,
        vote_number: int
) -> List[Union[Call, str]]:
    """Decode aragon voting with specific number."""
    script_code = str(aragon_voting.getVote(vote_number)[-1])
    return decode_evm_script(script_code, abi_storage)
