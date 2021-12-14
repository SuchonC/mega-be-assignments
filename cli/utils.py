import click
import requests
import os
from web3 import Web3, exceptions as web3_exceptions

ETHER_SCAN_MAINNET_URL = 'https://api.etherscan.io'
w3 = Web3(Web3.WebsocketProvider(os.getenv('ETHER_NODE_WEBSOCKET_URL')))


def get_abi(contract_address):
    payload = {
        'module': 'contract',
        'action': 'getabi',
        'address': contract_address
    }

    try:
        response = requests.get(
            f"{ETHER_SCAN_MAINNET_URL}/api", params=payload)
    except Exception as e:
        click.echo(e)

    return response.json()


def get_contract_detail(contract_address):
    contract_address = contract_address.lower()
    abi_response = get_abi(contract_address)

    # check abi response status
    if int(abi_response['status']) != 1:
        click.echo(f'Getting the ABI of {contract_address} failed')
        click.echo(f'Message : {abi_response["message"]}')
        click.echo(f'Result : {abi_response["result"]}')
        exit()

    abi = abi_response['result']
    checksum_address = Web3.toChecksumAddress(contract_address)
    contract = w3.eth.contract(abi=abi, address=checksum_address)
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


def get_balance_of(contract_address, target_address):
    pass