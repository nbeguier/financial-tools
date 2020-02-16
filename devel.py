#!/usr/bin/env python3
"""
Features in development

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
import sys

# Own library
import lib.analysis as analysis
import lib.common as common
import lib.display as display
import lib.reporting as reporting

# Debug
# from pdb import set_trace as st

VERSION = '1.0.0'

def best_per(parameters):
    """
    Display the differents stage of the PER and when
    it was reach for the last time
    """
    parameters['extra'] = dict()
    parameters['extra']['dividendes'] = False
    parameters['extra']['bénéfices'] = False
    parameters['extra']['peg'] = False

    report = reporting.get_report(parameters)
    report['isin'] = parameters['isin']
    simple_report = reporting.simplify_report(report, parameters)
    pers = analysis.per_by_value(simple_report)
    for per in pers:
        pers[per]['date'] = analysis.get_last_val_date(
            parameters['isin'], pers[per]['value'])
    display.print_per(pers)

def best_peg(parameters):
    """
    Display the differents stage of the PEG and when
    it was reach for the last time
    """
    parameters['extra'] = dict()
    parameters['extra']['dividendes'] = False
    parameters['extra']['bénéfices'] = False
    parameters['extra']['peg'] = True

    report = reporting.get_report(parameters)
    report['isin'] = parameters['isin']
    simple_report = reporting.simplify_report(report, parameters)
    pegs = analysis.peg_by_value(simple_report)
    for peg in pegs:
        pegs[peg]['date'] = analysis.get_last_val_date(
            parameters['isin'], pegs[peg]['value'])
    display.print_peg(pegs)

def is_healthy(parameters):
    """
    Returns true if the share is health:
        both PER and PEG are ok
    """
    parameters['extra'] = dict()
    parameters['extra']['dividendes'] = False
    parameters['extra']['bénéfices'] = False
    parameters['extra']['peg'] = True

    report = reporting.get_report(parameters)
    report['isin'] = parameters['isin']
    simple_report = reporting.simplify_report(report, parameters)

    if 'PER' not in simple_report or 'peg' not in simple_report:
        return False
    if analysis.per_text(simple_report['PER']) == 'ration bon' \
        and analysis.peg_text(simple_report['peg']) == 'croissance annoncée ok':
        return True
    return False

if __name__ == '__main__':
    PARSER = ArgumentParser()

    PARSER.add_argument('--version', action='version', version=VERSION)

    PARSER.add_argument('-i', '--isin', action='store',\
        help='Code ISIN')
    PARSER.add_argument('-p', '--place', action='store',\
        help="Code d'identification de marché (=XPAR)", default='XPAR')
    PARSER.add_argument('-s', '--search', action='store',\
        help="Recherche l'ISIN le plus probable")
    PARSER.add_argument('--best-per', action='store_true',\
        help="Affiche le cours de l'action selon différentes valeurs du PER (=False)",\
        default=False)
    PARSER.add_argument('--best-peg', action='store_true',\
        help="Affiche le cours de l'action selon différentes valeurs du PEG (=False)",\
        default=False)
    PARSER.add_argument('--is-healthy', action='store_true',\
        help="Affiche si l'action est saine (=False)",\
        default=False)
    ARGS = PARSER.parse_args()

    PARAMS = dict()
    PARAMS['isin'] = ARGS.isin
    PARAMS['place'] = ARGS.place
    PARAMS['force'] = True
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

    if ARGS.best_per:
        best_per(PARAMS)
    elif ARGS.best_peg:
        best_peg(PARAMS)
    elif ARGS.is_healthy:
        print(is_healthy(PARAMS))
    else:
        PARSER.print_help()
