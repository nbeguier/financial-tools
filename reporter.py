#!/usr/bin/env python3
"""
Reporter

Copyright (c) 2020-2022 Nicolas Beguier
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

VERSION = '1.13.2'

def get_sign(value):
    """
    This function returns the sign of the value
    """
    sign = ''
    if value > 0:
        sign = '+'
    return sign

def is_different_and_valid(old_report, new_report, key):
    """
    Returns True if the key is present in both report and valid
    """
    return key in new_report and key in old_report\
            and old_report[key] != new_report[key] \
            and old_report[key] is not None and new_report[key] is not None

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

def report_valorisation(old_report, new_report, html_tag):
    """
    Report the valorisation
    """
    if is_different_and_valid(old_report, new_report, 'valorisation'):
        evo_valorisation = round(100 * (-1 + \
            float(new_report['valorisation']) / float(old_report['valorisation'])), 2)
        sign = get_sign(evo_valorisation)
        if sign == '+':
            evo_valorisation = f'{html_tag["green_in"]}{sign}{evo_valorisation} %{html_tag["green_out"]}'
        else:
            evo_valorisation = f'{html_tag["red_in"]}{sign}{evo_valorisation} %{html_tag["red_out"]}'
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution valorisation{html_tag["bold_out"]}: {evo_valorisation}{html_tag["li_out"]}')
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution valorisation{html_tag["bold_out"]}: {old_report["valorisation"]} -> {new_report["valorisation"]} EUR{html_tag["li_out"]}')

def report_per(old_report, new_report, html_tag):
    """
    Report the PER
    """
    if is_different_and_valid(old_report, new_report, 'PER'):
        evo_per = round(float(new_report['PER']) - float(old_report['PER']), 1)
        evo_per = f'{html_tag["blue_in"]}{get_sign(evo_per)}{evo_per}{html_tag["blue_out"]}'
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PER{html_tag["bold_out"]}: {evo_per}{html_tag["li_out"]}')
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PER{html_tag["bold_out"]}: {old_report["PER"]} -> {new_report["PER"]}{html_tag["li_out"]}')
        if analysis.per_text(old_report['PER']) != analysis.per_text(new_report['PER']):
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PER{html_tag["bold_out"]}: {analysis.per_text(old_report["PER"])} -> {analysis.per_text(new_report["PER"])}{html_tag["li_out"]}')

def report_peg(old_report, new_report, html_tag):
    """
    Report the PEG
    """
    if is_different_and_valid(old_report, new_report, 'peg'):
        evo_peg = round(float(new_report['peg']) - float(old_report['peg']), 1)
        evo_peg = f'{html_tag["blue_in"]}{get_sign(evo_peg)}{evo_peg}{html_tag["blue_out"]}'
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PEG{html_tag["bold_out"]}: {evo_peg}{html_tag["li_out"]}')
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PEG{html_tag["bold_out"]}: {old_report["peg"]} -> {new_report["peg"]}{html_tag["li_out"]}')

def report_benefices(old_report, new_report, html_tag):
    """
    Report the benefices
    """
    if is_different_and_valid(old_report, new_report, 'benefices'):
        evo_benef = round(float(new_report['benefices']) - float(old_report['benefices']), 2)
        sign = get_sign(evo_benef)
        if sign == '+':
            evo_benef = f'{html_tag["green_in"]}{sign}{evo_benef} pts{html_tag["green_out"]}'
        else:
            evo_benef = f'{html_tag["red_in"]}{sign}{evo_benef} pts{html_tag["red_out"]}'
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution benefices{html_tag["bold_out"]}: {evo_benef}{html_tag["li_out"]}')
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution benefices{html_tag["bold_out"]}: {old_report["benefices"]} -> {new_report["benefices"]}{html_tag["li_out"]}')

def report_rdv(old_report, new_report, html_tag):
    """
    Report the Rendez-vous
    """
    if is_different_and_valid(old_report, new_report, 'Prochain rdv'):
        print(f'{html_tag["li_in"]}{html_tag["blue_in"]}{html_tag["bold_in"]}Nouveau rdv{html_tag["bold_out"]}: {new_report["Prochain rdv"]}{html_tag["blue_out"]}{html_tag["li_out"]}')
    try:
        struct_time = time.strptime(new_report['Prochain rdv'], '%d/%m/%y')
        if 0 <= (datetime(*struct_time[:6]) - datetime.now()).days <= 3:
            print(f'{html_tag["li_in"]}{html_tag["blue_in"]}{html_tag["bold_in"]}[Reminder] Prochain rdv{html_tag["bold_out"]}: {new_report["Prochain rdv"]}{html_tag["blue_out"]}{html_tag["li_out"]}')
    except (ValueError, KeyError, TypeError):
        pass

def report_trend(old_report, new_report, html_tag):
    """
    Report the trending
    """
    if 'trend' in old_report and 'trend' in new_report:
        old_trend = analysis.trend(old_report)
        new_trend = analysis.trend(new_report)
        if old_trend['short term'] != new_trend['short term']:
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Tendance court terme{html_tag["bold_out"]}: {old_trend["short term"]}/5 -> {new_trend["short term"]}/5{html_tag["li_out"]}')
        else:
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Tendance court terme{html_tag["bold_out"]}: {new_trend["short term"]}/5{html_tag["li_out"]}')
        if old_trend['mid term'] != new_trend['mid term']:
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Tendance moyen terme{html_tag["bold_out"]}: {old_trend["mid term"]}/5 -> {new_trend["mid term"]}/5{html_tag["li_out"]}')
        else:
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Tendance moyen terme{html_tag["bold_out"]}: {new_trend["mid term"]}/5{html_tag["li_out"]}')

def report_potential(old_report, new_report, html_tag):
    """
    Report the potential
    """
    if 'potential' in new_report:
        if 'potential' not in old_report:
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}[Boursorama] Potentiel 3 mois{html_tag["bold_out"]}: {new_report["potential"]["brsrm"]["value"]} EUR{html_tag["li_out"]}')
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}[Fortuneo] Potentiel 3 mois{html_tag["bold_out"]}: {new_report["potential"]["frtn"]["value"]} EUR{html_tag["li_out"]}')
        else:
            if 'brsrm' not in old_report['potential'] or (\
                old_report['potential']['brsrm']['value'] != \
                new_report['potential']['brsrm']['value']):
                print(f'{html_tag["li_in"]}{html_tag["bold_in"]}[Boursorama] Potentiel 3 mois{html_tag["bold_out"]}: {old_report["potential"]["brsrm"]["value"]} -> {new_report["potential"]["brsrm"]["value"]} EUR{html_tag["li_out"]}')
            if 'frtn' not in old_report['potential'] or (\
                old_report['potential']['frtn']['value'] != \
                new_report['potential']['frtn']['value']):
                print(f'{html_tag["li_in"]}{html_tag["bold_in"]}[Fortuneo] Potentiel{html_tag["bold_out"]}: {old_report["potential"]["frtn"]["value"]} -> {new_report["potential"]["frtn"]["value"]} EUR{html_tag["li_out"]}')

def diff_report(oldest_file, newer_file, isin_compare, is_html):
    """
    Compare two report
    """
    html_tag = {
        'bold_in': '',
        'bold_out': '',
        'li_in': '',
        'li_out': '',
        'red_in': '',
        'red_out': '',
        'green_in': '',
        'green_out': '',
        'blue_in': '',
        'blue_out': '',
    }
    if is_html:
        html_tag = {
            'bold_in': '<b>',
            'bold_out': '</b>',
            'li_in': '<li>',
            'li_out': '</li>',
            'red_in': '<span style="color: #f00;">',
            'red_out': '</span>',
            'green_in': '<span style="color: #18b724;">',
            'green_out': '</span>',
            'blue_in': '<span style="color: #007eff;">',
            'blue_out': '</span>',
        }

    old_reports = load_report(oldest_file, display_report=False)
    new_reports = load_report(newer_file, display_report=False)

    if is_html:
        print('<html><body>')
    else:
        print('==============')
    for _isin in isin_compare:
        if is_html:
            print('<div><ul>')
        if _isin not in old_reports or _isin not in new_reports:
            continue
        old_report = old_reports[_isin]
        new_report = new_reports[_isin]
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}ISIN{html_tag["bold_out"]}: {new_report["isin"]}{html_tag["li_out"]}')
        if 'nom' in new_report:
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Nom{html_tag["bold_out"]}: {new_report["nom"]}{html_tag["li_out"]}')

        report_valorisation(old_report, new_report, html_tag)

        report_per(old_report, new_report, html_tag)

        report_peg(old_report, new_report, html_tag)

        report_benefices(old_report, new_report, html_tag)

        report_rdv(old_report, new_report, html_tag)

        report_trend(old_report, new_report, html_tag)

        report_potential(old_report, new_report, html_tag)

        if is_html:
            print('</ul></div>')
        else:
            print('==============')
    if is_html:
        print('</body></html>')

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
    DIFF_PARSER.add_argument('--html', action='store_true',\
        help='Output in HTML format', default=False)

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
        diff_report(ARGS.oldest_file, ARGS.newer_file, ISIN_COMPARE, ARGS.html)

    sys.exit(0)
