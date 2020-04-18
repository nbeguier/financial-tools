#!/usr/bin/env python3
"""
ISIN

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
import sys

# Own library
import lib.common as common
import lib.display as display
import lib.reporting as reporting

# Debug
# from pdb import set_trace as st

VERSION = '2.7.1'

def main(parameters):
    """
    Main function
    """
    report = reporting.get_report(parameters)
    report = reporting.simplify_report(report, parameters)
    if parameters['history']['healthy']:
        display.print_health(report, parameters['verbose'])
    else:
        display.print_report(
            report,
            mic=parameters['mic'],
            header=parameters['header'],
            footer=parameters['footer'],
            verbose=parameters['verbose'])

if __name__ == '__main__':
    PARSER = ArgumentParser()

    PARSER.add_argument('--version', action='version', version=VERSION)
    PARSER.add_argument('--verbose', action='store_true',\
        help="Affiche plus d'informations (=False)", default=False)

    PARSER.add_argument('-i', '--isin', action='store',\
        help="Code ISIN")
    PARSER.add_argument('-n', '--nom', action='store',\
        help="Nom de l'action")
    PARSER.add_argument('-m', '--market-id-code', action='store',\
        help="Code d'identification de marché (=XPAR)", default='XPAR')
    PARSER.add_argument('--no-header', action='store_true',\
        help="Cache les informations de bases (=False)", default=False)
    PARSER.add_argument('--no-footer', action='store_true',\
        help="Cache les URLs de fin (=False)", default=False)
    PARSER.add_argument('--dividendes-history', action='store_true',\
        help="Affiche plus d'informations sur les dividendes (=False)", default=False)
    PARSER.add_argument('--per-history', action='store_true',\
        help="Affiche la valeur théorique du PER (=False)", default=False)
    PARSER.add_argument('--peg-history', action='store_true',\
        help="Affiche la valeur théorique du PEG (=False)", default=False)
    PARSER.add_argument('--is-healthy', action='store_true',\
        help="Affiche l'état de santé de l'action (=False)", default=False)

    ARGS = PARSER.parse_args()

    PARAMS = dict()
    PARAMS['isin'] = ARGS.isin
    PARAMS['mic'] = ARGS.market_id_code
    PARAMS['verbose'] = ARGS.verbose
    PARAMS['header'] = not ARGS.no_header
    PARAMS['footer'] = not ARGS.no_footer
    PARAMS['history'] = dict()
    PARAMS['history']['dividendes'] = ARGS.dividendes_history
    PARAMS['history']['per'] = ARGS.per_history
    PARAMS['history']['peg'] = ARGS.peg_history
    PARAMS['history']['healthy'] = ARGS.is_healthy
    if not ARGS.isin and not ARGS.nom:
        PARSER.print_help()
        sys.exit(1)
    elif ARGS.nom is not None:
        RESULT = common.autocomplete(ARGS.nom)
        if not RESULT:
            print('No result for this name')
            sys.exit(1)
        else:
            PARAMS['isin'] = RESULT[0]['ISIN']

    main(PARAMS)
