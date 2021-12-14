import click
import os

# TODO: create a setup.py


@click.group()
def cli():
    pass


@cli.command()
@click.argument('contract_address', type=str)
def detail():
    pass


@cli.command()
@click.argument('contract_address', type=str)
@click.argument('target_address', type=str)
def balance_of(contract_address, target_address):
    pass


@cli.command()
@click.argument('contract_address', type=str)
def watch_tx(contract_address):
    pass


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
