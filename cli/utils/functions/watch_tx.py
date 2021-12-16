import threading
import click
import sys
import time
from utils.common import ETHER_SCAN_URL, w3
from web3 import Web3

def keep_watch_tx(contract_address):
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

    click.echo('The program will keep printing links of new transactions to etherscan.io')
    click.echo('Press "q + ENTER" to abort')
    while True:
        if input().lower() == 'q':
            click.echo('Aborting')
            thread_stop_flag = True
            log_thread.join()
            watch_thread.join()
            break