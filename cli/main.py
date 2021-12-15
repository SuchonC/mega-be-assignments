import click
import os
from utils import functions

# TODO: create a setup.py
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
    click.echo(f'Balance : {balance}')


@cli.command()
@click.argument('contract_address', type=str)
def watch_tx(contract_address):
    functions.is_valid_erc_20(contract_address)
    functions.watch_tx(contract_address)


@cli.command()
@click.argument('n', type=int)
@click.argument('contract_address', type=str)
def latest_tx(n, contract_address):
    pass


@cli.command()
@click.argument('n', type=int)
@click.argument('contract_address', type=str)
def holders(n, contract_address):
    pass


if __name__ == "__main__":
    cli()
