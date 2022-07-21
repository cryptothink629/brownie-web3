import requests

from src.utils import fetch_abi_from_address
from src.web3_client import w3

w3.eth.default_account = w3.eth.accounts[0]

ESTIMATE_GAS_URL = 'https://blocknative-api.herokuapp.com/data'

gas_limit = 69909  # unit
gas_price = 40  # Gwei
ether_price = 1200

gas_price_in_ether = w3.fromWei(w3.toWei(gas_price, 'Gwei'), 'Ether')
transaction_fee = gas_limit * gas_price_in_ether * ether_price
print('transaction fee: $' + str(transaction_fee))

transaction_example = {
    'gas': 210000,  # gas limit
    'maxFeePerGas': 3000000000,  # base fee + priority
    'maxPriorityFeePerGas': 2000000000,  # give it to miner
    'value': 0
}


def query_gas_estimation():
    res = requests.get(url=ESTIMATE_GAS_URL)
    if res.status_code != 200:
        raise Exception('no response from gas estimation service.')
    estimated_prices = res.json()['estimatedPrices'][0]

    base_fee = w3.toWei(estimated_prices['price'], 'Gwei')  # got in Gwei, transfer to wei
    max_fee_per_gas = w3.toWei(estimated_prices['maxFeePerGas'], 'Gwei')
    max_priority_fee_per_gas = w3.toWei(estimated_prices['maxPriorityFeePerGas'], 'Gwei')

    return base_fee, max_fee_per_gas, max_priority_fee_per_gas


def build_transaction(estimate_gas):
    base_fee, max_fee_per_gas, max_priority_fee_per_gas = query_gas_estimation()
    transaction = {}
    transaction['gas'] = int(estimate_gas * 1.5)
    transaction['maxFeePerGas'] = int(max_fee_per_gas * 1.2)
    transaction['maxPriorityFeePerGas'] = int(max_priority_fee_per_gas * 1.1)
    print('transaction with gas: {}'.format(transaction))
    return transaction


def _mint(address, function_name, params=()):
    print('calling func: ' + function_name)
    abi = fetch_abi_from_address(address)
    g = w3.eth.contract(address=address, abi=abi)
    estimate_gas = g.functions[function_name](*params).estimateGas()
    print('estimate gas: ' + str(estimate_gas))
    transaction = build_transaction(estimate_gas)
    tx_hash = g.functions[function_name](*params).transact(transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


def main():
    _mint('0x761cE323e352Bc28BE5568a536A1E8aa51674DDf', 'mint', (1,))


if __name__ == '__main__':
    query_gas_estimation()
    main()


