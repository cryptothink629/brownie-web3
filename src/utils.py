import json
from json.decoder import JSONDecodeError
import requests
from solcx import compile_files

from src.web3_client import w3
from src.log import logger

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
    try:
        abi_json = json.loads(response_json['result'])
    except JSONDecodeError as e:
        logger.error(e, exc_info=True)
        logger.error('response json: {}'.format(response_json))
        raise JSONDecodeError
    abi = json.dumps(abi_json, indent=4, sort_keys=True)
    return abi


def export_private_key(keystore_file, password):
    with open(keystore_file) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, password)
    return private_key


def send_eth(acc1, key, acc2, value):
    nonce = w3.eth.getTransactionCount(acc1)

    # build a transaction in a dictionary
    tx = {
        'nonce': nonce,
        'to': acc2,
        'value': w3.toWei(value, 'ether')
    }

    # sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, key)

    # send transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
