from brownie import Number, accounts

def main():
    account = accounts[0]
    # Number.deploy(1, {'from': account}, publish_source=True)
    Number.deploy(1, {'from': account})
