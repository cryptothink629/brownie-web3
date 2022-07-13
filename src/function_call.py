from src.constants import ERC721
from src.utils import get_abi_from_source
from src.web3_client import w3

w3.eth.default_account = w3.eth.accounts[0]


def call_721_mint(address, path, params=()):
    abi, _ = get_abi_from_source(path)
    g = w3.eth.contract(address=address, abi=abi)

    tx_hash = g.functions.mint(*params).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


if __name__ == '__main__':
    call_721_mint('0x01440Df37afbc0253Ed8a07d7eC0402BfeC2F49d', ERC721, (w3.eth.accounts[0], 1))
