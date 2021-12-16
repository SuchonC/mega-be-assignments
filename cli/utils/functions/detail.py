from web3 import exceptions as web3_exceptions
from utils.common import get_contract_object

def get_contract_detail(contract_address):
    contract_address = contract_address.lower()
    contract = get_contract_object(contract_address)

    try:
        name = contract.functions.name().call()
    except web3_exceptions.ABIFunctionNotFound:
        name = None

    try:
        symbol = contract.functions.symbol().call()
    except web3_exceptions.ABIFunctionNotFound:
        symbol = None

    try:
        decimals = contract.functions.decimals().call()
    except web3_exceptions.ABIFunctionNotFound:
        decimals = None

    return {
        'name': name,
        'symbol': symbol,
        'decimals': decimals
    }