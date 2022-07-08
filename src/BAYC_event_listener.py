import json

from web3 import Web3
from web3.middleware import geth_poa_middleware

from src.constants import MAIN_IPC

w3 = Web3(Web3.IPCProvider(MAIN_IPC))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('web3 connection: ' + str(w3.isConnected()))

BAYC_address = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
with open('./abi/bayc.json', 'r') as f:
    data = json.load(f)
    abi = json.dumps(data)

contract = w3.eth.contract(address=BAYC_address, abi=abi)
event_filter = contract.events.Transfer.createFilter(fromBlock='latest')


def handle_event(e):
    tx_receipt = w3.eth.waitForTransactionReceipt(e['transactionHash'])
    rich_logs = contract.events.Transfer().processReceipt(tx_receipt)
    print(rich_logs[0])


while True:
    for new_event in event_filter.get_new_entries():
        handle_event(new_event)
