from web3 import Web3
from utils.common import get_contract_object
from utils.functions.detail import get_contract_detail


def get_balance_of(contract_address, target_address):
    contract_address = contract_address.lower()
    target_address = target_address.lower()
    target_address = Web3.toChecksumAddress(target_address)
    contract = get_contract_object(contract_address)
    details = get_contract_detail(contract_address)
    balance = contract.functions.balanceOf(target_address).call()
    return {
        'balance': balance / (10 ** details['decimals']),
        'symbol': details['symbol']
    }
