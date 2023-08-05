"""
Parsing and decoding aragon votes.

Prepare human-readable representation of the last N votes
for a aragon application with a specific address in a target net.
"""
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

from brownie.utils import color

from avotes_parser.core.ABI import get_cached_etherscan_api
from avotes_parser.core.ABI.utilities.etherscan import (
    DEFAULT_NET, NET_URL_MAP
)
from .utilities import (
    logging_settings, read_key, get_aragon_voting,
    parse_voting, set_infura_project_id
)

DEFAULT_ARAGON_ADDRESS = '0x2e59A20f205bB85a89C53f1936454680651E618e'
DEFAULT_N = 10
DEFAULT_WORKERS_NUM = DEFAULT_N


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        add_help=True,
        description=__doc__,
        prog='avotes-parser',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--apitoken',
                        required=True,
                        type=str,
                        help='Etherscan API key as string or '
                             'a path to txt file with it.')
    parser.add_argument('--infura',
                        type=str,
                        required=True,
                        help='Infura project ID.')

    parser.add_argument('-n',
                        type=int,
                        default=DEFAULT_N,
                        help='Parse last N votes.')
    parser.add_argument('--aragon-voting-address',
                        type=str,
                        default=DEFAULT_ARAGON_ADDRESS,
                        help='Address of aragon voting contract.')
    parser.add_argument('--net',
                        type=str,
                        default=DEFAULT_NET,
                        help='Net name is case-insensitive.',
                        choices=NET_URL_MAP.keys())
    parser.add_argument('--retries',
                        type=int,
                        default=5,
                        help='Number of retries of calling Etherscan API.')
    parser.add_argument('--num-workers',
                        default=DEFAULT_WORKERS_NUM,
                        type=int,
                        help='Number of asynchronous parsing tasks.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Show debug messages')

    return parser.parse_args()


def main():
    """Parse and decode aragon votes."""
    args = parse_args()

    logging_settings(args.debug)
    token = read_key(args.apitoken)
    set_infura_project_id(args.infura)
    logging.debug(f'API key: {token}')

    aragon_voting = get_aragon_voting(
        args.net, args.aragon_voting_address,
        token, args.retries
    )

    last_vote_number = aragon_voting.votesLength()

    abi_storage = get_cached_etherscan_api(
        token, args.net
    )

    _parse_voting = partial(parse_voting, aragon_voting, abi_storage)
    number_offset = last_vote_number - args.n
    with ThreadPoolExecutor(args.num_workers) as executor:
        parsed_votes = {
            executor.submit(
                _parse_voting,
                vote_number + number_offset
            ): vote_number
            for vote_number in range(
                0, args.n
            )
        }
        results = [None] * len(parsed_votes)
        for future in as_completed(parsed_votes):
            number = parsed_votes[future]
            results[number] = future.result()

    for num, parsed_vote in enumerate(results):
        number = num + number_offset
        total = len(parsed_vote)
        print(f'Voting #{number}.')
        for ind, call in enumerate(parsed_vote):
            print(f'Point {ind + 1}/{total}.')
            print(color.highlight(repr(call)))
        print('------------------------------------------------\n\n')


if __name__ == '__main__':
    main()
