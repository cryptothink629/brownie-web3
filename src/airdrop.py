from src.utils import get_abi_from_source
from src.web3_client import w3

w3.eth.default_account = w3.eth.accounts[0]

token_contract_addr = '0xBe73B67ac3dEacC0afd52Bb703FAE6Bf7e0287Bb'
airdrop_contract_addr = '0xa872270251cAa8EbaF9Afd9697F62fcE0EC9Ad4C'


def approve(spender, approve_number):
    file_path = '../contracts/MyERC20.sol'
    abi, _ = get_abi_from_source(file_path)
    token_contract = w3.eth.contract(address=token_contract_addr, abi=abi)
    tx_hash = token_contract.functions.approve(spender, approve_number).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    print(tx_receipt)

    # check
    allowance = token_contract.functions.allowance(w3.eth.default_account, spender).call()
    print('allowance: ' + str(allowance))


def airdrop(list_, number_):
    abi, _ = get_abi_from_source('../contracts/Airdrop.sol')
    airdrop_contract = w3.eth.contract(address=airdrop_contract_addr, abi=abi)
    tx_hash = airdrop_contract.functions.airdrop(token_contract_addr, list_, number_).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    print(tx_receipt)


if __name__ == '__main__':
    approve_number = 1000 * 10 ** 18
    approve(airdrop_contract_addr, approve_number)

    airdrop_list = ['0xc0819E1e01204BCB9CB5a0a3Be826afedAd6EDEf',
                    '0x51B7C437c3B0662772dF1Ba4DF1e2F6E1bBc4437',
                    '0x588354A410E8E5A14A47D8f114bdE9Ab5D70abba',
                    '0xcBF28602Be5D9334e1838586CcA93Df6060f0eF6',
                    '0x420A6C1c79a6Ce31ED9dC1C4343310C97b378F83',
                    '0x6CcaF7C0BFabCbdcC28c20f123e497ec208168B0',
                    '0x0d24f692c05036602076b3f51242b5A34C55Ee38',
                    '0xE0e7d31d3b79B96dBe41E0A75a3606DD91dd2873',
                    '0x2458243F21518e366928436D828b2bc01D327EA8',
                    '0xdD21EefFCeeBAb85C61a222Cf6f79c376ECb4E73']
    airdrop_number = [100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      100 * 10 ** 18,
                      ]
    airdrop(airdrop_list, airdrop_number)
