from web3 import Web3
from web3.middleware import geth_poa_middleware

from src.log import logger

# configure your own provider
# ipc_provider = Web3.IPCProvider(GOERLI_IPC)
http_provider = Web3.HTTPProvider('http://localhost:8545')

w3 = Web3(http_provider)

w3.middleware_onion.inject(geth_poa_middleware, layer=0)
logger.info('web3 connection: ' + str(w3.isConnected()))
logger.info('gas price in Wei: ' + str(w3.eth.gas_price))
logger.info('current new block number: ' + str(w3.eth.block_number))
