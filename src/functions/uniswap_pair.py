import time

from web3.exceptions import BadFunctionCallOutput

from src.log import logger
from src.utils import get_abi_from_json_file
from src.web3_client import w3


class UniPair(object):
    UNISWAP_PAIR_ABI = './src/abi/uniswap_pair.json'

    def __init__(self, addr):
        self.addr = addr
        self.token0_addr = self.get_token0()
        self.token1_addr = self.get_token1()

    def get_reserves(self):
        return self._call(self.addr, 'getReserves')

    def get_kLast(self):
        return self._call(self.addr, 'kLast')

    def get_token0(self):
        return self._call(self.addr, 'token0')

    def get_token1(self):
        return self._call(self.addr, 'token1')

    def _call(self, address, fuction_name, params=()):
        abi = get_abi_from_json_file(UniPair.UNISWAP_PAIR_ABI)
        g = w3.eth.contract(address=address, abi=abi)
        try:
            result = g.functions[fuction_name](*params).call()
        except BadFunctionCallOutput as e:
            logger.error(e, exc_info=True)
            logger.error('error address {}, function name {}'.format(address, fuction_name))
            time.sleep(5)
            result = g.functions[fuction_name](*params).call()
        return result


if __name__ == '__main__':
    # test
    pass
