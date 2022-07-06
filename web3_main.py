import os

from solcx import compile_files
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider(os.environ.get('GETH_HOST')))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('web3 connection: ' + str(w3.isConnected()))


def transfer(from_, to_, value):
    tx_hash = w3.eth.send_transaction({
        'from': from_,
        'to': to_,
        'value': value
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)

    tx = w3.eth.get_transaction(tx_hash)
    print(tx)
    return tx


def create_number_contract(abi, bytecode):
    n = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = n.constructor(1).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    return tx_receipt


def call_number(abi, address):
    g = w3.eth.contract(address=address, abi=abi)
    number = g.functions.get().call()
    print('number:' + str(number))


def set_number(abi, address):
    g = w3.eth.contract(address=address, abi=abi)
    tx_hash = g.functions.set(1).transact()
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # return tx_receipt


def deploy_contract(abi, bytecode):
    c = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = c.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)
    return tx_receipt


def main():
    ac1 = w3.eth.accounts[0]
    ac2 = w3.eth.accounts[1]

    w3.eth.default_account = w3.eth.accounts[0]

    # value = w3.toWei(0.001, 'ether')
    # transfer(ac1, ac2, value)

    file_path = './contracts/Number.sol'
    compiled_sol = compile_files([file_path], output_values=['abi', 'bin'])
    contract_id, contract_interface = compiled_sol.popitem()
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']

    # tx_receipt = deploy_contract(abi, bytecode)
    # address = tx_receipt.contractAddress
    # print('Contract address:' + address)
    address = '0xfBeEe3B5FD04e080BEAEabd73F4D59039d753251'
    call_number(abi, address)

    set_number(abi, address)

    contract = w3.eth.contract(address=address, abi=abi)
    event_filter = contract.events.Add.createFilter(fromBlock='latest')

    def handle_event(e):
        tx_receipt = w3.eth.waitForTransactionReceipt(e['transactionHash'])
        rich_logs = contract.events.Add().processReceipt(tx_receipt)
        print(Web3.toJSON(rich_logs[0]))

    while True:
        for new_event in event_filter.get_new_entries():
            handle_event(new_event)


if __name__ == '__main__':
    main()
