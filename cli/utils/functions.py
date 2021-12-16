import time
import click
import json
import requests
import os
import threading
import sys
from web3 import Web3, exceptions as web3_exceptions
from bs4 import BeautifulSoup as bs

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
    target_address = target_address.lower()
    target_address = Web3.toChecksumAddress(target_address)
    contract = get_contract_object(contract_address)
    details = get_contract_detail(contract_address)
    balance = contract.functions.balanceOf(target_address).call()
    return {
        'balance': balance / (10 ** details['decimals']),
        'symbol': details['symbol']
    }


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
                m = 'Watching' + '.' * i
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


def latest_tx(n, contract_address):
    if not 1 <= n <= 100:
        click.echo('N must be between 1 and 100 (inclusive)')
        exit()

    contract_address = contract_address.lower()
    contract = get_contract_object(contract_address)

    def get_latest_n_tx_hashes(n, contract_address):
        checksum_address = Web3.toChecksumAddress(contract_address)
        transactions = []  # contain transaction hex
        block_id = w3.eth.get_block('latest')['number']
        block_interval = 50 if 50 < block_id else 0
        while len(transactions) < n:
            filter = w3.eth.filter(
                {'fromBlock': block_id-block_interval, 'toBlock': block_id, 'address': checksum_address})
            logs = w3.eth.get_filter_logs(filter.filter_id)
            logs.reverse()

            empty_space = n - len(transactions)

            if empty_space >= len(logs):
                for l in logs:
                    transactions.append(l['transactionHash'])
            else:
                for l in logs[:empty_space]:
                    transactions.append(l['transactionHash'])

            block_id -= block_interval + 1
            if block_id < 0:
                break
        return transactions

    def get_tx_info(tx_hash):
        tx = w3.eth.get_transaction(tx_hash)
        try:
            decoded_input = contract.decode_function_input(tx['input'])
            func, args = decoded_input
            return {
                'transaction': tx,
                'info': {
                    'function_name': type(func).__name__,
                    'args': args
                }
            }
        except Exception as e:
            return {
                'transaction': tx,
                'info': str(e)
            }

    def save_tx_info_to_file(idx, info, n):
        with open(f'latest_{n}_transactions.txt', 'a') as file:
            file.write(f'No. {idx}\n')
            file.write(
                f'Transaction hash : {info["transaction"]["hash"].hex()}\n')
            file.write(f'Sender address : {info["transaction"]["from"]}\n')
            if 'function_name' not in info['info']:
                file.write(f'Cannot decode function data : {info["info"]}\n')
            else:
                file.write(f'Call data\n')
                file.write(
                    f'   -> Function : {info["info"]["function_name"]}\n')
                for arg in info['info']['args']:
                    file.write(f'   -> {arg} : {info["info"]["args"][arg]}\n')
            file.write('\n\n')

    tx_hashes = get_latest_n_tx_hashes(n, contract_address)

    idx = 1
    for tx_hash in tx_hashes:
        info = get_tx_info(tx_hash)
        save_tx_info_to_file(idx, info, n)
        idx += 1


def holders(n, contract_address):
    # scraping from etherscan's holder chart
    if not 1 <= n <= 100:
        click.echo('N must be between 1 and 100 (inclusive)')
        exit()

    details = get_contract_detail(contract_address)
    data = requests.get(f'{ETHER_SCAN_URL}/token/tokenholderchart/{contract_address}',
                        headers={
                            'User-Agent': 'Firefox'  # to bypass Captcha
                        },
                        params={
                            'range': n
                        }).text

    def save_to_file(data, filename='top_n_holders.txt'):
        with open(filename, 'a') as file:
            for d in data:
                file.write(f'\
{d["rank"]}. Holder address : {d["holder_address"]}\n\
{" "*(len(d["rank"])+2)}Balance        : {d["balance"]} {d["symbol"]}\n\n')

    soup = bs(data, 'html.parser')
    rows = soup.find_all('tr')
    data = []
    for row in rows[1:]:  # 0th row is the header
        tds = row.find_all('td')
        holder_address_start_idx = tds[1].a['href'].find('?a=') + 3
        data.append({
            'rank': tds[0].string,
            'holder_address': tds[1].a['href'][holder_address_start_idx:],
            'balance': tds[2].string,
            'symbol': details['symbol']
        })
    save_to_file(data, filename=f'top_{n}_holders_of_{details["name"]}.txt')
