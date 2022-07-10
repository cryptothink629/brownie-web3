from src.utils import get_abi_from_source
from src.web3_client import w3

w3.eth.default_account = w3.eth.accounts[0]

token_address = '0xd63e17F85Ee3EEA679DadF58BDF1E45546066F37'
airdrop_contract_addr = '0xa872270251cAa8EbaF9Afd9697F62fcE0EC9Ad4C'


def approve(spender, approve_number):
    file_path = '../contracts/MyERC20.sol'
    abi, _ = get_abi_from_source(file_path)
    token_contract = w3.eth.contract(address=token_address, abi=abi)
    tx_hash = token_contract.functions.approve(spender, approve_number).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def airdrop(list_, number_):
    abi, _ = get_abi_from_source('../contracts/Airdrop.sol')
    airdrop_contract = w3.eth.contract(address=airdrop_contract_addr, abi=abi)
    tx_hash = airdrop_contract.functions.airdrop(token_address, list_, number_).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


if __name__ == '__main__':
    approve_number = 1000 * 10 ** 18
    approve(airdrop_contract_addr, approve_number)

    airdrop_list = []
    airdrop_number = [100 * 10 ** 18, 100 * 10 ** 18]
    airdrop(airdrop_list, airdrop_number)
