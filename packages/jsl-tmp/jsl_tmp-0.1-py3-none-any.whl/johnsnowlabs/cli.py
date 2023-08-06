# https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/
import colorama
from colorama import Fore
from pyfiglet import Figlet
from johnsnowlabs.cli_utils.cli_flows import *


f = Figlet(font='doh', width=70)
print(Fore.BLUE + f.renderText('JSL-LIB'), )

jsl_actions = [
    'login',
    'list-keys',
    'install',
    'license-status',
]

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='JSL-CLI Do stuff')
    parser.add_argument('action', metavar='action', type=str, nargs=1,
                        choices=jsl_actions,
                        help='an integer for the accumulator')
    parser.add_argument('--sum', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')
    print('ARGV IS', sys.argv)

    args = parser.parse_args()
    print('ARGS ARE', args)

    print('act', args.action)
    action = args.action[0]
    if action == 'login':
        print('todo')
    elif action == 'list-keys':
        print('todo')
    elif action == 'install':
        # Test if offline, if yes suggest offline mode otherwise just install
        # 1. Find Spark version if any
        print('todo')
    elif action == 'install-offline':
        # Test if offline, if yes suggest offline mode
        print('todo')
        install_offline()
    elif action == 'license-status':
        print('todo')



