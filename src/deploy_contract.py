import os

from src.constants import CUZUKI, PRIVATE_KEY, ACCOUNT_ADDRESS
from src.utils import get_abi_from_source
from src.web3_client import w3

private_key = os.environ[PRIVATE_KEY]
account = os.environ[ACCOUNT_ADDRESS]
w3.eth.default_account = w3.eth.accounts[0]


def deploy_with_key(file_path, const=(), transaction=None):
    """
    from one single file
    :param file_path:
    :param const:
    :param transaction: {'value': value} transfer ether
    :return:
    """
    abi, bytecode = get_abi_from_source(file_path)
    c = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(account)
    if transaction:
        transaction['nonce'] = nonce
    else:
        transaction = {'nonce': nonce}
    unicorn_txn = c.constructor(*const).buildTransaction(transaction)
    print(unicorn_txn)

    signed = w3.eth.account.sign_transaction(unicorn_txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    print(tx_receipt)


def deploy(file_path, const=(), transaction=None):
    """
    from one single file
    :param file_path:
    :param const:
    :param transaction: {'value': value} transfer ether
    :return:
    """
    abi, bytecode = get_abi_from_source(file_path)
    c = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = c.constructor(*const).transact(transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    print(tx_receipt)


def deploy_airdrop():
    file_path = '../contracts/Airdrop.sol'
    deploy(file_path)
    # 0xa872270251cAa8EbaF9Afd9697F62fcE0EC9Ad4C


def deploy_sendeth():
    file_path = '../contracts/SendETH.sol'
    value = w3.toWei(0.0001, 'ether')
    transaction = {'value': value}
    deploy(file_path, transaction=transaction)


def deploy_erc20(path, name, symbol):
    deploy(path, const=(name, symbol))


def deploy_erc721(path, name, symbol):
    deploy(path, const=(name, symbol))


def deploy_BAYC(path, name, symbol, max, time_start):
    deploy(path, const=(name, symbol, max, time_start))


def deploy_CuZuki(path, name, symbol, uri):
    deploy_with_key(path, const=(name, symbol, uri))


if __name__ == '__main__':
    # deploy_erc721(ERC721, 'Bored ape yat club', 'BAYC')
    # deploy_BAYC(BAYC, 'Bored Ape Yacht Club', 'BAYC', 10000, 10000)
    # deploy_erc20(ERC20, 'Nothing', 'NONE')
    deploy_CuZuki(CUZUKI, 'CuZuki', 'CZK', 'ipfs://QmeQNQxF8kBtc73gWZKfsjD1K3XWUm3SPx6r5ooS759Pp8/')
