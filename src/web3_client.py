from web3 import Web3
from web3.middleware import geth_poa_middleware

from src.constants import ROPSTEN_IPC

w3 = Web3(Web3.HTTPProvider(ROPSTEN_IPC))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('web3 connection: ' + str(w3.isConnected()))
