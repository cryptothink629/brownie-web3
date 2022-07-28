import math
import time

from src.functions.erc20 import UniERC20
from src.functions.uniswap_pair import UniPair
from src.log import logger
from src.utils import fetch_abi_from_address
from src.web3_client import w3

UNISWAP_V2 = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'

abi = fetch_abi_from_address(UNISWAP_V2)
contract = w3.eth.contract(address=UNISWAP_V2, abi=abi)
pair_created_event = contract.events.PairCreated()


def handle_event(e):
    tx_receipt = w3.eth.waitForTransactionReceipt(e['transactionHash'])
    rich_logs = pair_created_event.processReceipt(tx_receipt)
    data = rich_logs[0]
    logger.debug('get PairCreated event: {}'.format(data))

    token0_addr = data['args']['token0']
    token1_addr = data['args']['token1']
    pair_addr = data['args']['pair']
    token0 = UniERC20(token0_addr)
    token1 = UniERC20(token1_addr)

    pair = UniPair(pair_addr)
    assert token0_addr == pair.token0_addr, 'token0 address not equal'
    assert token1_addr == pair.token1_addr, 'token1 address not equal'
    reserves = pair.get_reserves()
    n0 = reserves[0] / math.pow(10, token0.decimals)
    n1 = reserves[1] / math.pow(10, token1.decimals)
    # log info
    logger.info('------------')
    logger.info('Token0: {}({})'.format(token0.symbol, token0.name))
    logger.debug('name: {}'.format(token0.name))
    logger.info('contract: {}'.format(token0_addr))
    logger.info('pooled {}: {}'.format(token0.symbol, n0))

    logger.info('Token1: {}({})'.format(token1.symbol, token1.name))
    logger.debug('name: {}'.format(token1.name))
    logger.info('contract: {}'.format(token1_addr))
    logger.info('pooled {}: {}'.format(token1.symbol, n1))
    logger.info('------------')


def main():
    event_filter = w3.eth.filter({'fromBlock': 'latest', 'address': UNISWAP_V2})
    logger.debug('start event filter')
    while True:
        for new_event in event_filter.get_new_entries():
            handle_event(new_event)
            logger.info('sleep for 30s')
            time.sleep(30)


if __name__ == '__main__':
    main()
