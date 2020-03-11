#!/usr/bin/env python3
"""
Reporter

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
from datetime import datetime
import json
import os.path
import sys
import time

# Own library
import lib.analysis as analysis
import lib.display as display
import lib.reporting as reporting
try:
    import settings
except ImportError:
    print('You need to specify a settings.py file.')
    print('$ cp settings.py.sample settings.py')
    sys.exit(1)

# Debug
# from pdb import set_trace as st

VERSION = '1.10.6'

def get_sign(value):
    """
    This function returns the sign of the value
    """
    sign = ''
    if value > 0:
        sign = '+'
    return sign

def save_report(output_dir):
    """
    Save or display the report on disk
    """
    parameters = dict()
    parameters['mic'] = 'XPAR'
    parameters['history'] = dict()
    parameters['history']['dividendes'] = False
    parameters['history']['per'] = False
    parameters['history']['peg'] = False

    for _isin in settings.ISIN_SAVE:
        parameters['isin'] = _isin
        report = reporting.get_report(parameters)
        report['isin'] = _isin
        simple_report = reporting.simplify_report(report, parameters)
        if not output_dir:
            print(simple_report)
        else:
            with open('{}/{}.txt'.format(
                    output_dir,
                    datetime.now().strftime('%Y_%m_%d')), 'a') as report_file:
                report_file.write(json.dumps(simple_report)+'\n')

def load_report(input_file, display_report=True):
    """
    Load and display the report
    """
    report = dict()
    if not os.path.exists(input_file):
        print('The specified path: {} does not exists...'.format(input_file))
        sys.exit(1)
    with open(input_file, 'r') as report_file:
        for line in report_file.readlines():
            sub_report = json.loads(line)
            report[sub_report['isin']] = sub_report
            if display_report:
                display.print_report(sub_report, footer=False)
    return report

def diff_report(oldest_file, newer_file, isin_compare):
    """
    Compare two report
    """
    old_reports = load_report(oldest_file, display_report=False)
    new_reports = load_report(newer_file, display_report=False)

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
            and 'valorisation' in old_report \
            and old_report['valorisation'] != new_report['valorisation']:
            evo_valorisation = round(100 * (-1 + \
                float(new_report['valorisation']) / float(old_report['valorisation'])), 2)
            print('Evolution valorisation: {}{} %'.format(
                get_sign(evo_valorisation), evo_valorisation))
            print('Evolution valorisation: {} -> {} EUR'.format(
                old_report['valorisation'], new_report['valorisation']))
        if 'PER' in new_report and 'PER' in old_report\
            and old_report['PER'] != new_report['PER']:
            evo_per = round(float(new_report['PER']) - float(old_report['PER']), 1)
            print('Evolution PER: {}{}'.format(get_sign(evo_per), evo_per))
            print('Evolution PER: {} -> {}'.format(old_report['PER'], new_report['PER']))
            if analysis.per_text(old_report['PER']) != analysis.per_text(new_report['PER']):
                print('Evolution PER: {} -> {}'.format(
                    analysis.per_text(old_report['PER']),
                    analysis.per_text(new_report['PER'])))

        if 'peg' in new_report and 'peg' in old_report\
            and old_report['peg'] != new_report['peg']:
            evo_peg = round(float(new_report['peg']) - float(old_report['peg']), 1)
            print('Evolution PEG: {}{}'.format(get_sign(evo_peg), evo_peg))
            print('Evolution PEG: {} -> {}'.format(old_report['peg'], new_report['peg']))
        if 'benefices' in new_report \
            and old_report['benefices'] != new_report['benefices']:
            evo_benef = round(float(new_report['benefices']) - float(old_report['benefices']), 2)
            print('Evolution benefices: {}{} points'.format(
                get_sign(evo_benef), evo_benef))
            print('Evolution benefices: {} -> {}'.format(
                old_report['benefices'], new_report['benefices']))
        if 'Prochain rdv' in new_report and 'Prochain rdv' in old_report\
            and old_report['Prochain rdv'] != new_report['Prochain rdv']:
            print('Nouveau rdv: {}'.format(new_report['Prochain rdv']))
        try:
            struct_time = time.strptime(new_report['Prochain rdv'], '%d/%m/%y')
            if 0 <= (datetime(*struct_time[:6]) - datetime.now()).days <= 3:
                print('[Reminder] Prochain rdv: {}'.format(new_report['Prochain rdv']))
        except (ValueError, KeyError, TypeError):
            pass
        if 'trend' in old_report and 'trend' in new_report:
            old_trend = analysis.trend(old_report)
            new_trend = analysis.trend(new_report)
            if old_trend['short term'] != new_trend['short term']:
                print('Tendance court terme: {}/5 -> {}/5'.format(
                    old_trend['short term'], new_trend['short term']))
            else:
                print('Tendance court terme: {}/5'.format(new_trend['short term']))
            if old_trend['mid term'] != new_trend['mid term']:
                print('Tendance moyen terme: {}/5 -> {}/5'.format(
                    old_trend['mid term'], new_trend['mid term']))
            else:
                print('Tendance moyen terme: {}/5'.format(new_trend['mid term']))
        if 'potential' in new_report:
            if 'potential' not in old_report:
                print('[Boursorama] Potentiel 3 mois: {} EUR'.format(
                    new_report['potential']['brsrm']['value']))
                print('[Fortuneo] Potentiel 3 mois: {} EUR'.format(
                    new_report['potential']['frtn']['value']))
            else:
                if 'brsrm' not in old_report['potential'] or (\
                    old_report['potential']['brsrm']['value'] != new_report['potential']['brsrm']['value']):
                    print('[Boursorama] Potentiel 3 mois: {} -> {} EUR'.format(
                        old_report['potential']['brsrm']['value'],
                        new_report['potential']['brsrm']['value']))
                if 'frtn' not in old_report['potential'] or (\
                    old_report['potential']['frtn']['value'] != new_report['potential']['frtn']['value']):
                    print('[Fortuneo] Potentiel: {} -> {} EUR'.format(
                        old_report['potential']['frtn']['value'],
                        new_report['potential']['frtn']['value']))
        # TODO: Add argument to display this
        # if 'trend' in new_report:
        #     if 'trend' not in old_report or (\
        #         old_report['trend']['echos']['short term'] != new_report['trend']['echos']['short term']):
        #         print('[Echos] Tendance court terme: {} -> {}'.format(
        #             old_report['trend']['echos']['short term'],
        #             new_report['trend']['echos']['short term']))
        #     if 'trend' not in old_report or (\
        #         old_report['trend']['echos']['mid term'] != new_report['trend']['echos']['mid term']):
        #         print('[Echos] Tendance moyen terme: {} -> {}'.format(
        #             old_report['trend']['echos']['mid term'],
        #             new_report['trend']['echos']['mid term']))
        #     if 'trend' not in old_report or (\
        #         old_report['trend']['frtn']['short term'] != new_report['trend']['frtn']['short term']):
        #         print('[Fortuneo] Tendance court terme: {} -> {}'.format(
        #             old_report['trend']['frtn']['short term'],
        #             new_report['trend']['frtn']['short term']))
        #     if 'trend' not in old_report or (\
        #         old_report['trend']['frtn']['mid term'] != new_report['trend']['frtn']['mid term']):
        #         print('[Fortuneo] Tendance moyen terme: {} -> {}'.format(
        #             old_report['trend']['frtn']['mid term'],
        #             new_report['trend']['frtn']['mid term']))
        #     if 'trend' not in old_report or (\
        #         old_report['trend']['bnp']['short term'] != new_report['trend']['bnp']['short term']):
        #         print('[BNP] Tendance court terme: {} -> {}'.format(
        #             old_report['trend']['bnp']['short term'],
        #             new_report['trend']['bnp']['short term']))
        #     if 'trend' not in old_report or (\
        #         old_report['trend']['bnp']['mid term'] != new_report['trend']['bnp']['mid term']):
        #         print('[BNP] Tendance moyen terme: {} -> {}'.format(
        #             old_report['trend']['bnp']['mid term'],
        #             new_report['trend']['bnp']['mid term']))
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
        help='Specific ISIN to compare', default='')

    ARGS = PARSER.parse_args()

    if len(sys.argv) == 1:
        PARSER.print_help()
        sys.exit(1)

    if sys.argv[1] == 'save':
        save_report(ARGS.output_dir)
    elif sys.argv[1] == 'load':
        load_report(ARGS.inputfile)
    elif sys.argv[1] == 'diff':
        ISIN_COMPARE = settings.ISIN_COMPARE
        if ARGS.isin:
            ISIN_COMPARE = [ARGS.isin]
        diff_report(ARGS.oldest_file, ARGS.newer_file, ISIN_COMPARE)

    sys.exit(0)
