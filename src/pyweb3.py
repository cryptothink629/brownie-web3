from web3 import Web3
from web3.middleware import geth_poa_middleware

from src.constants import GOERLI_IPC

# infura_mainnet_url = 'https://mainnet.infura.io/v3/c66311e1efb04a0b8bb0e1b2177b54cc'

# w3 = Web3(Web3.HTTPProvider(infura_mainnet_url))

w3 = Web3(Web3.IPCProvider(GOERLI_IPC))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('web3 connection: ' + str(w3.isConnected()))
