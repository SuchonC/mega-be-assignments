import time
import click
import json
import requests
import os
import threading
import sys
from web3 import Web3, exceptions as web3_exceptions

ETHER_SCAN_MAINNET_URL = 'https://api.etherscan.io'
ETHER_SCAN_URL = 'https://etherscan.io'
ETHER_SCAN_API_KEY = os.getenv('ETHER_SCAN_API_KEY')
w3 = Web3(Web3.WebsocketProvider(os.getenv('ETHER_NODE_WEBSOCKET_URL')))


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


def is_valid_erc_20(contract_address):
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
        for func_b in abi:
            if func_a['type'] != func_b['type'] or func_a['name'] != func_b['name']:
                continue
            if func_a['type'] == 'function':
                if len(func_a['inputs']) != len(func_b['inputs']):
                    click.echo(
                        f'Function {func_a["name"]}\'s inputs do not match the ERC-20 specification as specified in {ref_link}')
                    exit(1)
                if len(func_a['outputs']) != len(func_b['outputs']):
                    click.echo(
                        f'Function {func_a["name"]}\'s outputs do not match the ERC-20 specification as specified in {ref_link}')
                    exit(1)
                for i in range(len(func_a['inputs'])):
                    if func_a['inputs'][i]['type'] != func_b['inputs'][i]['type']:
                        click.echo(
                            f'Input {func_a["inputs"][i]} of function {func_a["name"]} has an invalid type')
                        exit(1)
                for i in range(len(func_a['outputs'])):
                    if func_a['outputs'][i]['type'] != func_b['outputs'][i]['type']:
                        click.echo(
                            f'Output {func_a["outputs"][i]} of function {func_a["name"]} has an invalid type')
                        exit(1)
                func_found = True
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


def get_balance_of(contract_address, target_address):
    contract_address = contract_address.lower()
    contract = get_contract_object(contract_address)
    return contract.functions.balanceOf(target_address).call()


def watch_tx(contract_address):
    contract_address = contract_address.lower()
    checksum_address = Web3.toChecksumAddress(contract_address)

    thread_stop_flag = False

    def log_loop(event_filter, interval):
        while True:
            for event in event_filter.get_new_entries():
                click.echo(
                    f'{ETHER_SCAN_URL}/tx/{event["transactionHash"].hex()}')
            if thread_stop_flag:
                break
            time.sleep(interval)

    def print_watching():
        while True:
            for i in range(1, 5):
                if thread_stop_flag:
                    return
                m = 'Wathing' + '.' * i
                print(m, end='\r')
                time.sleep(1)
            sys.stdout.write('\033[K')

    block_filter = w3.eth.filter(
        {'fromBlock': 'latest', 'address': checksum_address})

    log_thread = threading.Thread(target=log_loop, args=(block_filter, 2))
    watch_thread = threading.Thread(target=print_watching)
    log_thread.start()
    watch_thread.start()

    click.echo('The program will keep printing links to etherscan.io')
    click.echo('Press "q + ENTER" to abort')
    while True:
        if input().lower() == 'q':
            click.echo('Aborting')
            thread_stop_flag = True
            log_thread.join()
            watch_thread.join()
            break
