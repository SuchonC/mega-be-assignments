import click
from web3 import Web3
from utils.common import get_contract_object, w3

def get_latest_tx(n, contract_address):
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