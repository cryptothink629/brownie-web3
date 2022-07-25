import os

from src.constants import BAYC, CUZUKI, PRIVATE_KEY, ACCOUNT_ADDRESS
from src.utils import get_abi_from_source
from src.web3_client import w3

private_key = os.environ[PRIVATE_KEY]
account = os.environ[ACCOUNT_ADDRESS]
w3.eth.default_account = w3.eth.accounts[0]


def _transact_by_key(address, path, fuction_name, params=()):
    print('calling func: ' + fuction_name)
    abi, _ = get_abi_from_source(path)
    g = w3.eth.contract(address=address, abi=abi)
    print('estimate gas: ' + str(g.functions[fuction_name](*params).estimateGas()))

    nonce = w3.eth.get_transaction_count(account)
    transaction = {'nonce': nonce}
    unicorn_txn = g.functions[fuction_name](*params).buildTransaction(transaction)
    print(unicorn_txn)

    signed = w3.eth.account.sign_transaction(unicorn_txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def _transact(address, path, fuction_name, params=()):
    print('calling func: ' + fuction_name)
    abi, _ = get_abi_from_source(path)
    g = w3.eth.contract(address=address, abi=abi)
    print('estimate gas: ' + str(g.functions[fuction_name](*params).estimateGas()))
    tx_hash = g.functions[fuction_name](*params).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def _call(address, path, fuction_name, params=()):
    print('calling func: ' + fuction_name)
    abi, _ = get_abi_from_source(path)
    g = w3.eth.contract(address=address, abi=abi)
    result = g.functions[fuction_name](*params).call()
    print(result)


def call_721_mint(address, path, params=()):
    _transact(address, path, 'mint', params)


def call_bayc_reserveApes(address, path, params=()):
    _transact(address, path, 'reserveApes', params)


def call_bayc_setBaseURI(address, params=()):
    _transact(address, BAYC, 'setBaseURI', params)


def call_cuzuki_mint(address, params=()):
    _transact_by_key(address, CUZUKI, 'MintCuZuki', params)


if __name__ == '__main__':
    # call_721_mint('0x987760Cb138818dbB373710d3837718b7cA3a048', ERC721, (w3.eth.accounts[0], 2))
    # call_bayc_reserveApes('0x901a6151076Af632A413e8a8D1ADEC1f8Dc80859', BAYC)
    # call_bayc_setBaseURI('0x855B23acfb8C5d72D3e5D7a5cC1d6591fcDb1aE0', ('ipfs://QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/',))
    # _call('0x901a6151076Af632A413e8a8D1ADEC1f8Dc80859', BAYC, 'tokenURI', (1,))
    # _transact('0xA0E18d15863B8236e77243AC11f4138C1C0B73C0', CUZUKI, 'pause', (False, ))
    call_cuzuki_mint('0xA0E18d15863B8236e77243AC11f4138C1C0B73C0', (1,))
