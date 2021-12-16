import click
import os
from utils import functions

# TODO: create a setup.py
# TODO: add loading status in latest-tx function
# !! require Microsoft Visual C++ 14.00 and newer for windows
# !! need to be in 'cli' folder before executing main.py (because of file opening is relative to CWD)


@click.group()
def cli():
    web_socket_url = os.getenv('ETHER_NODE_WEBSOCKET_URL')
    http_url = os.getenv('ETHER_NODE_HTTP_URL')
    if web_socket_url is None and http_url is None:
        click.echo(
            'Either ETHER_NODE_WEBSOCKET_URL or ETHER_NODE_HTTP_URL environment variable needs to be set')
        exit(1)


@cli.command()
@click.argument('contract_address', type=str)
def detail(contract_address):
    functions.is_valid_erc_20(contract_address)
    details = functions.get_contract_detail(contract_address)
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
    functions.is_valid_erc_20(contract_address)
    balance = functions.get_balance_of(contract_address, target_address)
    click.echo(f'Balance : {balance["balance"]} {balance["symbol"]}')


@cli.command()
@click.argument('contract_address', type=str)
def watch_tx(contract_address):
    functions.is_valid_erc_20(contract_address)
    functions.watch_tx(contract_address)


@cli.command()
@click.argument('n', type=int)
@click.argument('contract_address', type=str)
def latest_tx(n, contract_address):
    functions.is_valid_erc_20(contract_address)
    functions.latest_tx(n, contract_address)


@cli.command()
@click.argument('n', type=int)
@click.argument('contract_address', type=str)
def holders(n, contract_address):
    functions.is_valid_erc_20(contract_address)
    functions.holders(n, contract_address)


if __name__ == "__main__":
    cli()
