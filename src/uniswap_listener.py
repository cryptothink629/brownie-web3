import asyncio
import math
import os
from collections import deque

from src.constants import DISCORD_WEBHOOK
from src.functions.discord import discord
from src.functions.erc20 import UniERC20
from src.functions.uniswap_pair import UniPair
from src.log import logger
from src.utils import fetch_abi_from_address
from src.web3_client import w3

UNISWAP_V2 = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
UNISWAP_V3 = '0x1F98431c8aD98523631AE4a59f267346ea31F984'

pair_created_wait_liquidity = deque()
uni_v2_abi = None
uni_v3_abi = None


async def check_liquidity():
    logger.debug('check liquidity')
    while True:
        if len(pair_created_wait_liquidity) == 0:
            logger.debug('no pending tasks, wait 1 mins')
            await asyncio.sleep(60)
            continue
        task_number = len(pair_created_wait_liquidity)
        logger.debug('there is/are {} task(s) in queue'.format(task_number))
        logger.debug('wait 5 mins to check liquidity')
        await asyncio.sleep(60 * 5)
        for t in range(task_number):
            logger.debug('execute task {}'.format(t + 1))
            pair = pair_created_wait_liquidity.popleft()  # First in first out
            t0, t1 = pair.token0, pair.token1
            reserves = pair.get_reserves()
            t0.pooled = reserves[0] / math.pow(10, t0.decimals)
            t1.pooled = reserves[1] / math.pow(10, t1.decimals)
            log_token_info(t0, t1)


def log_token_info(token0, token1):
    if token0.symbol in ['WETH', 'USDC']:
        token0, token1 = token1, token0

        # log info
    logger.info('------------')
    logger.info('Token0: {}({})'.format(token0.symbol, token0.name))
    logger.debug('name: {}'.format(token0.name))
    logger.info('contract: {}'.format(token0.addr))
    logger.info('pooled {}: {}'.format(token0.symbol, token0.pooled))

    logger.info('Token1: {}({})'.format(token1.symbol, token1.name))
    logger.debug('name: {}'.format(token1.name))
    logger.info('contract: {}'.format(token1.addr))
    logger.info('pooled {}: {}'.format(token1.symbol, token1.pooled))
    # discord
    if token1.symbol == 'WETH' and token1.pooled >= 2:
        logger.debug('find a pool ETH >= 2')
        content = '[{}/{}], pooled ETH {}, name {}, address {}.' \
            .format(token0.symbol, token1.symbol, round(token1.pooled, 3), token0.name, token0.addr)
        discord(os.environ[DISCORD_WEBHOOK], content)


def v2_handler(e):
    logger.debug('Enter v2 handler')
    tx_receipt = w3.eth.waitForTransactionReceipt(e['transactionHash'])
    global uni_v2_abi
    if not uni_v2_abi:
        uni_v2_abi = fetch_abi_from_address(UNISWAP_V2)
    contract = w3.eth.contract(address=UNISWAP_V2, abi=uni_v2_abi)
    pair_created_event = contract.events.PairCreated()

    rich_logs = pair_created_event.processReceipt(tx_receipt)
    data = rich_logs[0]
    logger.debug('get v2 PairCreated event: {}'.format(w3.toJSON(data)))

    token0_addr = data['args']['token0']
    token1_addr = data['args']['token1']
    pair_addr = data['args']['pair']
    token0 = UniERC20(token0_addr)
    token1 = UniERC20(token1_addr)

    pair = UniPair(pair_addr)
    assert token0_addr == pair.token0_addr, 'token0 address not equal'
    assert token1_addr == pair.token1_addr, 'token1 address not equal'
    pair.token0 = token0  # in advanced bind for message queue
    pair.token1 = token1
    reserves = pair.get_reserves()
    token0.pooled = reserves[0] / math.pow(10, token0.decimals)
    token1.pooled = reserves[1] / math.pow(10, token1.decimals)
    if token0.symbol in ['WETH', 'USDC']:
        token0, token1 = token1, token0

    if token1.pooled == 0:
        logger.debug('WETH pool is empty')
        logger.info('------------')
        logger.info('got new pair({}/{} {}) with no liquidity, '
                    'waiting for add liquidity.'.format(token0.symbol, token1.symbol, token0.addr))
        pair_created_wait_liquidity.append(pair)
        return

    log_token_info(token0, token1)


def v3_handler(e):
    logger.debug('Enter v3 handler')
    tx_receipt = w3.eth.waitForTransactionReceipt(e['transactionHash'])
    global uni_v3_abi
    if not uni_v3_abi:
        uni_v3_abi = fetch_abi_from_address(UNISWAP_V3)
    contract = w3.eth.contract(address=UNISWAP_V3, abi=uni_v3_abi)
    pool_created_event = contract.events.PoolCreated()

    rich_logs = pool_created_event.processReceipt(tx_receipt)
    data = rich_logs[0]
    logger.debug('get v3 PoolCreated event: {}.'.format(w3.toJSON(data)))
    token0_addr = data['args']['token0']
    token1_addr = data['args']['token1']
    pool_addr = data['args']['pool']
    token0 = UniERC20(token0_addr)
    token1 = UniERC20(token1_addr)
    # log info
    logger.info('------------')
    logger.info('get v3 pool')
    logger.info('Token0: {}({})'.format(token0.symbol, token0.name))
    logger.debug('name: {}'.format(token0.name))
    logger.info('contract: {}'.format(token0_addr))
    # TODO: how to get pooled value

    logger.info('Token1: {}({})'.format(token1.symbol, token1.name))
    logger.debug('name: {}'.format(token1.name))
    logger.info('contract: {}'.format(token1_addr))


async def log_loop(event_filter, handler, poll_interval=1):
    while True:
        for new_event in event_filter.get_new_entries():
            handler(new_event)
        # logger.debug('pause for %ds', poll_interval)
        await asyncio.sleep(poll_interval)


def main():
    v2_filter = w3.eth.filter({'fromBlock': 'latest', 'address': UNISWAP_V2})
    v3_filter = w3.eth.filter({'fromBlock': 'latest', 'address': UNISWAP_V3})

    loop = asyncio.get_event_loop()
    logger.info('start main loop')
    loop.create_task(log_loop(v2_filter, v2_handler))
    loop.create_task(log_loop(v3_filter, v3_handler))
    loop.create_task(check_liquidity())
    loop.run_forever()


if __name__ == '__main__':
    main()
