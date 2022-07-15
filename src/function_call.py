from src.constants import BAYC
from src.utils import get_abi_from_source
from src.web3_client import w3

w3.eth.default_account = w3.eth.accounts[0]

transaction = {
    'gas': 130000,  # gas limit
    'maxFeePerGas': 3000000000,  # base fee + priority
    'maxPriorityFeePerGas': 2000000000  # give it to miner
}


def _call(address, path, fuction_name, params=()):
    print('calling func: ' + fuction_name)
    abi, _ = get_abi_from_source(path)
    g = w3.eth.contract(address=address, abi=abi)
    print('estimate gas: ' + str(g.functions[fuction_name](*params).estimateGas()))
    tx_hash = g.functions[fuction_name](*params).transact(transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def call_721_mint(address, path, params=()):
    abi, _ = get_abi_from_source(path)
    g = w3.eth.contract(address=address, abi=abi)

    tx_hash = g.functions.mint(*params).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def call_bayc_reserveApes(address, path, params=()):
    abi, _ = get_abi_from_source(path)
    g = w3.eth.contract(address=address, abi=abi)

    tx_hash = g.functions.reserveApes(*params).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def call_bayc_setBaseURI(address, params=()):
    _call(address, BAYC, 'setBaseURI', params)


if __name__ == '__main__':
    # call_721_mint('0x01440Df37afbc0253Ed8a07d7eC0402BfeC2F49d', ERC721, (w3.eth.accounts[0], 1))
    # call_bayc_reserveApes('0xEAeBB77348788062d8b6741eb6a2a45Bf4fBf9a3', BAYC)
    call_bayc_setBaseURI('0xEAeBB77348788062d8b6741eb6a2a45Bf4fBf9a3',
                         ('ipfs://QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/',))
