#!/usr/bin/env python3
"""
ISIN

Copyright (c) 2020-2022 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
import sys

# Own library
from lib import common, display, reporting

# Debug
# from pdb import set_trace as st

VERSION = '3.0.0'

def main(parameters):
    """
    Main function
    """
    report = reporting.get_report(parameters)
    display.print_report(
        report,
        header=parameters['header'])

if __name__ == '__main__':
    PARSER = ArgumentParser()

    PARSER.add_argument('--version', action='version', version=VERSION)

    PARSER.add_argument('-i', '--isin', action='store',\
        help="Code ISIN")
    PARSER.add_argument('-n', '--nom', action='store',\
        help="Nom de l'action")
    PARSER.add_argument('-m', '--market-id-code', action='store',\
        help="Code d'identification de marché (=XPAR)", default='XPAR')
    PARSER.add_argument('--no-header', action='store_true',\
        help="Cache les informations de bases (=False)", default=False)

    ARGS = PARSER.parse_args()

    PARAMS = {}
    PARAMS['isin'] = ARGS.isin
    PARAMS['mic'] = ARGS.market_id_code
    PARAMS['header'] = not ARGS.no_header
    if not ARGS.isin and not ARGS.nom:
        PARSER.print_help()
        sys.exit(1)
    elif ARGS.nom is not None:
        RESULT = common.autocomplete(ARGS.nom)
        if not RESULT or 'ISIN' not in RESULT[0]:
            print('No result for this name')
            sys.exit(1)
        else:
            PARAMS['isin'] = RESULT[0]['ISIN']

    main(PARAMS)
