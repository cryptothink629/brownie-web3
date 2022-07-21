#!/usr/bin/python
import argparse
import json

import requests

# Exports contract ABI in JSON

ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='

parser = argparse.ArgumentParser()
parser.add_argument('addr', type=str, help='Contract address')
parser.add_argument('-o', '--output', type=str, help="Path to the output JSON file", required=True)


def fetch(address):
    response = requests.get('%s%s' % (ABI_ENDPOINT, address))
    response_json = response.json()
    abi_json = json.loads(response_json['result'])
    abi = json.dumps(abi_json, indent=4, sort_keys=True)
    return abi


def __main__():
    args = parser.parse_args()
    result = fetch(args.addr)
    open(args.output, 'w').write(result)


if __name__ == '__main__':
    __main__()

#  python fetch_abi.py <contract address> -o <target JSON file>
