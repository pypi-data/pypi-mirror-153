# https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/
import colorama
from colorama import Fore
from pyfiglet import Figlet
# from johnsnowlabs.cli_utils.cli_flows import *
import click

from johnsnowlabs import ProductName

f = Figlet(font='doh', width=70)
print(Fore.BLUE + f.renderText('JSL-LIB'), )

jsl_actions = [
    'list-keys',
    'license-status',
]


@click.group()
def cli():
    pass

# https://www.youtube.com/watch?v=kNke39OZ2k0
@cli.command()
@click.option('--product','-p', default=ProductName.nlu, type=click.Choice([p.value for p in ProductName]), help='Product to install')
# @click.option('--name3', prompt='Wassup Bitch tell my your fav food ', default='your mom',help='The person to greet.')
def install(product):
    """
    Install JSL-Software"""
    click.echo(f"Hello {product}!")

@cli.command()
def login(count, name, name2,name3):
    """
    Login to My-JSL and store credentials in ~/.johnsnowlabs"""
    for x in range(count):
        click.echo(f"Hello {name}!")



@cli.command()
def license_status(count, name, name2,name3):
    """ Get information about license status in  ~/.johnsnowlabs"""
    for x in range(count):
        click.echo(f"Hello {name}!")


@cli.command()
def list_licenses(count, name, name2,name3):
    """ Get information about license status connected to My-JSL account identified
    by E-Mail+Password or Token"""
    for x in range(count):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    cli()
