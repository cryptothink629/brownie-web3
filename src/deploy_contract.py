from src.utils import get_abi_from_source
from src.web3_client import w3

w3.eth.default_account = w3.eth.accounts[0]


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
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def deploy_airdrop():
    file_path = '../contracts/Airdrop.sol'
    deploy(file_path)
    # 0xa872270251cAa8EbaF9Afd9697F62fcE0EC9Ad4C


def deploy_myerc20():
    file_path = '../contracts/MyERC20.sol'
    deploy(file_path, const=('Nothing', 'NONE'))
    # 0xd63e17F85Ee3EEA679DadF58BDF1E45546066F37


def deploy_sendeth():
    file_path = '../contracts/SendETH.sol'
    value = w3.toWei(0.0001, 'ether')
    transaction = {'value': value}
    deploy(file_path, transaction=transaction)


if __name__ == '__main__':
    deploy_airdrop()
