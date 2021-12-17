import click
import os
from utils.functions.detail import get_contract_detail
from utils.functions.balance_of import get_balance_of
from utils.functions.watch_tx import keep_watch_tx
from utils.functions.latest_tx import get_latest_tx
from utils.functions.holders import get_holders
from utils.common import is_valid_erc_20, verify_node_url

# TODO: create a setup.py
# TODO: add loading status in latest-tx function
# TODO: write help description
# !! need to be in 'cli' folder before executing main.py (because of file opening is relative to CWD)


@click.group()
def cli():
    """
    \b
    A CLI program for accessing some functionalities of Ethereum block chain.
    This program requires a URL endpoint to a running Ethereum node
    It also requires etherscan's API to retrieve contracts' ABI

    \b
    Where to set Ethereum node's endpoint?
     - For HTTP endpoint -> ETHER_NODE_HTTP_URL environment variable
     - For Websocket endpoint -> ETHER_NODE_WEBSOCKET_URL evironment variable
     - You must set at least one of these variables, if both are set, Websocket URL will be used

    \b
    Where to set etherscan's API KEY?
     - ETHER_SCAN_API_KEY

    \b
    Examples for Infura Ethereum node
     - export ETHER_NODE_HTTP_URL=https://mainnet.infura.io/v3/xxxx
     - export ETHER_SCAN_API_KEY=xxxxxxxxxxxxxxxxxx
    """
    web_socket_url = os.getenv('ETHER_NODE_WEBSOCKET_URL')
    http_url = os.getenv('ETHER_NODE_HTTP_URL')
    ether_scan_api_key = os.getenv('ETHER_SCAN_API_KEY')
    if web_socket_url is None and http_url is None:
        click.echo(
            'Either ETHER_NODE_WEBSOCKET_URL or ETHER_NODE_HTTP_URL environment variable needs to be set')
        exit(1)
    if ether_scan_api_key is None:
        click.echo(
            'ETHER_SCAN_API_KEY must be set')
        exit(1)
    verify_node_url()


@cli.command()
@click.argument('contract_address', type=str)
def detail(contract_address):
    """
    Get name, symbol and decimals of a contract
    """
    is_valid_erc_20(contract_address)
    details = get_contract_detail(contract_address)
    click.echo(
        f'Name : {details["name"] if details["name"] is not None else "Function name() is not implemented"}')
    click.echo(
        f'Symbol : {details["symbol"] if details["symbol"] is not None else "Function symbol() is not implemented"}')
    click.echo(
        f'Decimals : {details["decimals"] if details["decimals"] is not None else "Function decimals() is not implemented"}')


@cli.command()
@click.argument('contract_address', type=str)
@click.argument('target_address', type=str)
def balance_of(contract_address, target_address):
    """
    Get total balance of target address in a contract
    """
    is_valid_erc_20(contract_address)
    balance = get_balance_of(contract_address, target_address)
    click.echo(f'Balance : {balance["balance"]:,} {balance["symbol"]}')


@cli.command()
@click.argument('contract_address', type=str)
def watch_tx(contract_address):
    """
    Watch for new transactions in a contract
    """
    is_valid_erc_20(contract_address)
    keep_watch_tx(contract_address)


@cli.command()
@click.argument('n', type=int)
@click.argument('contract_address', type=str)
def latest_tx(n, contract_address):
    """
    Get latest N transactions of a contract
    """
    is_valid_erc_20(contract_address)
    get_latest_tx(n, contract_address)


@cli.command()
@click.argument('n', type=int)
@click.argument('contract_address', type=str)
def holders(n, contract_address):
    """
    Get top N holders of a contract
    """
    is_valid_erc_20(contract_address)
    get_holders(n, contract_address)


if __name__ == "__main__":
    cli()
