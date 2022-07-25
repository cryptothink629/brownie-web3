from brownie import CuZuki, accounts


def main():
    account = accounts[0]
    result = CuZuki.deploy('CuZuki',
                           'CZK',
                           'ipfs://QmeQNQxF8kBtc73gWZKfsjD1K3XWUm3SPx6r5ooS759Pp8/',
                           {'from': account},
                           publish_source=True)
    print(result)
