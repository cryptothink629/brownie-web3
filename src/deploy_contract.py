from solcx import compile_files

from src.pyweb3 import w3

w3.eth.default_account = w3.eth.accounts[0]


def deploy(file_path, transaction=None):
    compiled_sols = compile_files([file_path], output_values=['abi', 'bin'])
    while compiled_sols:
        contract_id, contract_interface = compiled_sols.popitem()
        print('compiling contract id: ' + contract_id)
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']

        c = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = c.constructor().transact(transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)


if __name__ == '__main__':
    file_path = '../contracts/ReceiveETH.sol'
    value = w3.toWei(0.0001, 'ether')
    transaction = {'value': value}
    deploy(file_path)
