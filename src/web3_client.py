from web3 import Web3
from web3.middleware import geth_poa_middleware

from src.constants import RINKEBY_HTTP, GOERLI_IPC

# ipc_provider = Web3.IPCProvider(GOERLI_IPC)
http_provider = Web3.HTTPProvider(RINKEBY_HTTP)

w3 = Web3(http_provider)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('web3 connection: ' + str(w3.isConnected()))
print('gas price in Wei: ' + str(w3.eth.gas_price))
print('current new block number: ' + str(w3.eth.block_number))
