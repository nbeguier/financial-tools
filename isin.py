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

VERSION = '1.3.1'

def main(parameters):
    """
    Main function
    """
    report = reporting.get_report(parameters)
    report['isin'] = parameters['isin']
    report = reporting.simplify_report(report, parameters)
    display.print_report(report, place=parameters['place'])

if __name__ == '__main__':
    PARSER = ArgumentParser()

    PARSER.add_argument('--version', action='version', version=VERSION)
    PARSER.add_argument('-i', '--isin', action='store',\
        help='Code ISIN')
    PARSER.add_argument('-p', '--place', action='store',\
        help="Code d'identification de marché (=XPAR)", default='XPAR')
    PARSER.add_argument('-s', '--search', action='store',\
        help="Recherche l'ISIN le plus probable")
    PARSER.add_argument('--extra-dividendes', action='store_true',\
        help="Affiche plus d'informations sur les dividendes (=False)", default=False)
    PARSER.add_argument('--extra-peg', action='store_true',\
        help="Affiche la valeur théorique du PEG (=False)", default=False)
    PARSER.add_argument('--extra-profit', action='store_true',\
        help="Affiche la valeur théorique de l'évolution des bénéfices (=False)", default=False)
    PARSER.add_argument('--extras', action='store_true',\
        help="Affiche toutes les informations supplémentaires (=False)", default=False)
    PARSER.add_argument('-f', '--force', action='store_true',\
        help='Recherche parmis beaucoup de données (=False)', default=False)

    ARGS = PARSER.parse_args()

    PARAMS = dict()
    PARAMS['isin'] = ARGS.isin
    PARAMS['place'] = ARGS.place
    PARAMS['force'] = ARGS.force
    PARAMS['extra'] = dict()
    PARAMS['extra']['dividendes'] = ARGS.extra_dividendes or ARGS.extras
    PARAMS['extra']['bénéfices'] = ARGS.extra_profit or ARGS.extra_peg or ARGS.extras
    PARAMS['extra']['peg'] = ARGS.extra_peg or ARGS.extras
    if not ARGS.isin and not ARGS.search:
        PARSER.print_help()
        sys.exit(1)
    elif ARGS.search is not None:
        RESULT = common.autocomplete(ARGS.search)
        if not RESULT:
            print('No result for this name')
            sys.exit(1)
        else:
            PARAMS['isin'] = RESULT[0]['ISIN']

    main(PARAMS)
