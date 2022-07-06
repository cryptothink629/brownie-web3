import os

from solcx import compile_files
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider(os.environ.get('GETH_HOST')))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('web3 connection: ' + str(w3.isConnected()))

address = '0xfBeEe3B5FD04e080BEAEabd73F4D59039d753251'

file_path = '../contracts/Number.sol'
compiled_sol = compile_files([file_path], output_values=['abi', 'bin'])
contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface['abi']
bytecode = contract_interface['bin']

contract = w3.eth.contract(address=address, abi=abi)
event_filter = contract.events.Add.createFilter(fromBlock='latest')


def handle_event(e):
    tx_receipt = w3.eth.waitForTransactionReceipt(e['transactionHash'])
    rich_logs = contract.events.Add().processReceipt(tx_receipt)
    print(rich_logs[0])


while True:
    for new_event in event_filter.get_new_entries():
        handle_event(new_event)
