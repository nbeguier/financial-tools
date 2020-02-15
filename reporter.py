#!/usr/bin/env python3
"""
Reporter

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
import json
import sys

# Third party library imports
from datetime import datetime

# Own library
import isin

# Debug
# from pdb import set_trace as st

VERSION = '1.0.0'

ISIN_SAVE = [
    'FR0000045072',
    'FR0000051732',
    'FR0000052292',
    'FR0000073272',
    'FR0000120073',
    'FR0000120172',
    'FR0000120271',
    'FR0000120321',
    'FR0000120404',
    'FR0000120503',
    'FR0000120578',
    'FR0000120628',
    'FR0000120644',
    'FR0000120693',
    'FR0000121014',
    'FR0000121220',
    'FR0000121261',
    'FR0000121329',
    'FR0000121485',
    'FR0000121501',
    'FR0000121667',
    'FR0000121972',
    'FR0000124141',
    'FR0000125007',
    'FR0000125338',
    'FR0000125486',
    'FR0000127771',
    'FR0000130577',
    'FR0000130650',
    'FR0000130809',
    'FR0000131104',
    'FR0000131906',
    'FR0000133308',
    'FR0010208488',
    'FR0010307819',
    'FR0013176526',
    'FR0013326246',
    'GB00BDSFG982',
    'LU1598757687',
    'NL0000226223',
    'NL0000235190',
]

ISIN_COMPARE = ['FR0000121485', 'FR0000120073', 'FR0000120628']

def save_report(output_dir):
    """
    Save or display the report on disk
    """
    parameters = dict()
    parameters['place'] = 'XPAR'
    parameters['extra'] = dict()
    parameters['extra']['dividendes'] = True
    parameters['extra']['bénéfices'] = True
    parameters['extra']['peg'] = True

    for _isin in ISIN_SAVE:
        parameters['isin'] = _isin
        report = isin.get_report(parameters)
        report['isin'] = _isin
        simple_report = isin.simplify_report(report, parameters)
        if not output_dir:
            print(simple_report)
        else:
            with open('{}/{}.txt'.format(
                    output_dir,
                    datetime.now().strftime('%Y_%m_%d')), 'a') as report_file:
                report_file.write(json.dumps(simple_report)+'\n')

def load_report(input_file, display=True):
    """
    Load and display the report
    """
    report = dict()
    with open(input_file, 'r') as report_file:
        for line in report_file.readlines():
            sub_report = json.loads(line)
            report[sub_report['isin']] = sub_report
            if display:
                isin.print_report(sub_report, display_urls=False)
    return report

def diff_report(oldest_file, newer_file, isin_compare):
    """
    Compare two report
    """
    old_reports = load_report(oldest_file, display=False)
    new_reports = load_report(newer_file, display=False)

    if isin_compare != ISIN_COMPARE:
        isin_compare = [isin_compare]

    print('==============')
    for _isin in isin_compare:
        if _isin not in old_reports or _isin not in new_reports:
            continue
        old_report = old_reports[_isin]
        new_report = new_reports[_isin]
        print('ISIN: {}'.format(new_report['isin']))
        if 'nom' in new_report:
            print('Nom: {}'.format(new_report['nom']))
        if 'valorisation' in new_report \
            and old_report['valorisation'] != new_report['valorisation']:
            evo_valorisation = round(100 * (-1 + \
                float(new_report['valorisation']) / float(old_report['valorisation'])), 2)
            sign = ''
            if evo_valorisation >= 0:
                sign = '+'
            print('Evolution valorisation: {}{} %'.format(sign, evo_valorisation))
            print('Evolution valorisation: {} -> {}'.format(
                old_report['valorisation'], new_report['valorisation']))
        if 'PER' in new_report \
            and old_report['PER'] != new_report['PER']:
            evo_per = round(float(new_report['PER']) - float(old_report['PER']), 1)
            sign = ''
            if evo_per >= 0:
                sign = '+'
            print('Evolution PER: {}{}'.format(sign, evo_per))
            print('Evolution PER: {} -> {}'.format(old_report['PER'], new_report['PER']))
            if isin.per_analysis(old_report['PER']) != isin.per_analysis(new_report['PER']):
                print('Evolution PER: {} -> {}'.format(
                    isin.per_analysis(old_report['PER']),
                    isin.per_analysis(new_report['PER'])))

        if 'peg' in new_report \
            and old_report['peg'] != new_report['peg']:
            evo_peg = round(float(new_report['peg']) - float(old_report['peg']), 1)
            sign = ''
            if evo_peg >= 0:
                sign = '+'
            print('Evolution PEG: {}{}'.format(sign, evo_peg))
            print('Evolution PEG: {} -> {}'.format(old_report['peg'], new_report['peg']))
        if 'benefices' in new_report \
            and old_report['benefices'] != new_report['benefices']:
            evo_benef = round(float(new_report['benefices']) - float(old_report['benefices']), 2)
            sign = ''
            if evo_benef >= 0:
                sign = '+'
            print('Evolution benefices: {}{} points'.format(sign, evo_benef))
            print('Evolution benefices: {} -> {}'.format(
                old_report['benefices'], new_report['benefices']))
        if 'Prochain rdv' in new_report \
            and old_report['Prochain rdv'] != new_report['Prochain rdv']:
            print('Nouveau rdv: {}'.format(new_report['Prochain rdv']))
        print('==============')

if __name__ == '__main__':

    PARSER = ArgumentParser()

    SUBPARSERS = PARSER.add_subparsers(help='commands')

    PARSER.add_argument('--version', action='version', version=VERSION)

    # SAVE Arguments
    SAVE_PARSER = SUBPARSERS.add_parser('save',\
        help='Save command')
    SAVE_PARSER.add_argument('-o', '--output-dir', action='store',\
        help='Save report into the specified directory', default='')

    # LOAD Arguments
    LOAD_PARSER = SUBPARSERS.add_parser('load',\
        help='Load command')
    LOAD_PARSER.add_argument('inputfile', action='store',\
        help='Load and display a saved report')

    # DIFF Arguments
    DIFF_PARSER = SUBPARSERS.add_parser('diff',\
        help='Diff command')
    DIFF_PARSER.add_argument('oldest_file', action='store',\
        help='Compare this oldest file with...')
    DIFF_PARSER.add_argument('newer_file', action='store',\
        help='... this newer file')
    DIFF_PARSER.add_argument('-i', '--isin', action='store',\
        help='Specific ISIN to compare', default=ISIN_COMPARE)

    ARGS = PARSER.parse_args()

    if len(sys.argv) == 1:
        PARSER.print_help()
        sys.exit(1)

    if sys.argv[1] == 'save':
        save_report(ARGS.output_dir)
    elif sys.argv[1] == 'load':
        load_report(ARGS.inputfile)
    elif sys.argv[1] == 'diff':
        diff_report(ARGS.oldest_file, ARGS.newer_file, ARGS.isin)

    sys.exit(0)
