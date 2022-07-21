import json

import requests
from solcx import compile_files

ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='


def get_abi_from_source(file_path):
    file_name = file_path.split('/')[-1]
    class_name = file_name.split('.')[0]
    compiled_sols = compile_files([file_path], output_values=['abi', 'bin'])
    for contract_id, contract_interface in compiled_sols.items():
        cla_name = contract_id.split(':')[-1]
        if class_name == cla_name:
            print('compiling contract: ' + contract_id)
            abi = contract_interface['abi']
            bytecode = contract_interface['bin']
            return abi, bytecode


def get_abi_from_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        abi = json.dumps(data)
    return abi


def fetch_abi_from_address(address):
    response = requests.get('%s%s' % (ABI_ENDPOINT, address))
    response_json = response.json()
    abi_json = json.loads(response_json['result'])
    abi = json.dumps(abi_json, indent=4, sort_keys=True)
    return abi
