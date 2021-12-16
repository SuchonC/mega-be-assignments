import requests
import click
import os
import json
from web3 import Web3

ETHER_SCAN_MAINNET_URL = 'https://api.etherscan.io'
ETHER_SCAN_URL = 'https://etherscan.io'
ETHER_SCAN_API_KEY = os.getenv('ETHER_SCAN_API_KEY')
ETHER_NODE_WEBSOCKET_URL = os.getenv('ETHER_NODE_WEBSOCKET_URL')
ETHER_NODE_HTTP_URL = os.getenv('ETHER_NODE_HTTP_URL')

if ETHER_NODE_WEBSOCKET_URL is not None:
    w3 = Web3(Web3.WebsocketProvider(ETHER_NODE_WEBSOCKET_URL))
elif ETHER_NODE_HTTP_URL is not None:
    w3 = Web3(Web3.HTTPProvider(ETHER_NODE_HTTP_URL))
else:
    click.echo('Error: cannot find Ethereum node\'s endpoint')


def get_abi(contract_address):
    payload = {
        'module': 'contract',
        'action': 'getabi',
        'address': contract_address,
        'apiKey': ETHER_SCAN_API_KEY
    }

    try:
        response = requests.get(
            f"{ETHER_SCAN_MAINNET_URL}/api", params=payload).json()
    except Exception as e:
        click.echo(e)
        exit(1)

    # check abi response status
    if int(response['status']) != 1:
        click.echo(f'Getting the ABI of {contract_address} failed')
        click.echo(f'Message : {response["message"]}')
        click.echo(f'Result : {response["result"]}')
        exit()

    return response['result']


def get_contract_object(contract_address):
    contract_address = contract_address.lower()
    abi = get_abi(contract_address)
    checksum_address = Web3.toChecksumAddress(contract_address)
    return w3.eth.contract(abi=abi, address=checksum_address)


def is_valid_erc_20(contract_address, strict=False):
    # follows ERC-20 specifications specified in https://eips.ethereum.org/EIPS/eip-20
    ref_link = 'https://eips.ethereum.org/EIPS/eip-20'

    contract_address = contract_address.lower()
    try:
        with open('utils/erc-20-abi.json', 'r') as file:
            erc_20 = json.load(file)
    except FileNotFoundError as e:
        click.echo(e)
        click.echo('Make sure you are in "cli" folder before executing "main.py"')
        exit(1)

    abi = json.loads(get_abi(contract_address))

    for func_a in erc_20:
        func_found = False
        if not strict and func_a['type'] == 'event':
            continue
        for func_b in abi:
            if 'name' not in func_b:
                continue
            if func_a['type'] != func_b['type'] or func_a['name'] != func_b['name']:
                continue
            if func_a['type'] == 'function':
                if len(func_a['inputs']) != len(func_b['inputs']):
                    click.echo(
                        f'Function {func_a["name"]}\'s inputs do not match the ERC-20 specification as specified in {ref_link}')
                    exit(1)
                if strict and len(func_a['outputs']) != len(func_b['outputs']):
                    click.echo(
                        f'Function {func_a["name"]}\'s outputs do not match the ERC-20 specification as specified in {ref_link}')
                    exit(1)
                for i in range(len(func_a['inputs'])):
                    if func_a['inputs'][i]['type'] != func_b['inputs'][i]['type']:
                        click.echo(
                            f'Input {func_b["inputs"][i]} of function {func_a["name"]} has an invalid type')
                        exit(1)
                if strict:
                    for i in range(len(func_a['outputs'])):
                        if func_a['outputs'][i]['type'] != func_b['outputs'][i]['type']:
                            click.echo(
                                f'Output {func_b["outputs"][i]} of function {func_a["name"]} has an invalid type')
                            exit(1)
            elif func_a['type'] == 'event':
                if len(func_a['inputs']) != len(func_b['inputs']):
                    click.echo(
                        f'Event {func_a["name"]}\'s inputs do not match the ERC-20 specification as specified in {ref_link}')
                    exit(1)
                for i in range(len(func_a['inputs'])):
                    if func_a['inputs'][i]['type'] != func_b['inputs'][i]['type']:
                        click.echo(
                            f'Input {func_a["inputs"][i]} of event {func_a["name"]} has an invalid type')
                        exit(1)
            func_found = True
        if not func_found:
            click.echo(f'{func_a["type"]} {func_a["name"]} is not implemented')
            exit(1)
    return True
