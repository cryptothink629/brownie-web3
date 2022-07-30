from src.utils import get_abi_from_json_file
from src.web3_client import w3


class UniERC20(object):
    ERC20_ABI = './src/abi/erc20.json'

    def __init__(self, addr):
        self.addr = addr
        self.name = self.get_name()
        self.symbol = self.get_symbol()
        self.decimals = self.get_decimals()

    def get_name(self):
        return self._call(self.addr, 'name')

    def get_symbol(self):
        return self._call(self.addr, 'symbol')

    def get_decimals(self):
        return self._call(self.addr, 'decimals')

    def _call(self, address, fuction_name, params=()):
        # error 'Contract source code not verified', use custom abi instead
        # abi = fetch_abi_from_address(address)
        abi = get_abi_from_json_file(UniERC20.ERC20_ABI)
        g = w3.eth.contract(address=address, abi=abi)
        result = g.functions[fuction_name](*params).call()
        return result


if __name__ == '__main__':
    # test
    pass
