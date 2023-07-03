#!/usr/bin/env python3
"""
Reporter

Copyright (c) 2020-2023 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
from datetime import datetime
import json
import glob
import os
import sys
from pathlib import Path

# Own library
from lib import analysis, display, reporting
try:
    import settings
except ImportError:
    print('You need to specify a settings.py file.')
    print('$ cp settings.py.sample settings.py')
    sys.exit(1)

# Debug
# from pdb import set_trace as st

VERSION = '3.1.0'

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
            and old_report[key]['v'] != new_report[key]['v'] \
            and old_report[key]['v'] is not None and new_report[key]['v'] is not None

def save_report(output_dir):
    """
    Save or display the report on disk
    """
    parameters = {}

    for _isin in settings.ISIN_SAVE:
        parameters['isin'] = _isin
        parameters['mic'] = 'XPAR'
        if ',' in _isin:
            parameters['isin'] = _isin.split(',', maxsplit=1)[0]
            parameters['mic'] = _isin.split(',')[1]
        report = reporting.get_report(parameters)
        if report is None:
            report = {}
        report['isin'] = _isin
        if not output_dir:
            print(report)
        else:
            if not Path(output_dir).is_dir():
                print(f'{output_dir} is not a directory...')
                return
            report_path = Path(f'{output_dir}/{datetime.now().strftime("%Y_%m_%d")}.txt')
            with report_path.open('a', encoding ='utf-8') as report_file:
                report_file.write(json.dumps(report)+'\n')

def load_report(input_file, display_report=True):
    """
    Load and display the report
    """
    report = {}
    report_path = Path(input_file)
    if not report_path.exists():
        print(f'The specified path: {input_file} does not exists...')
        sys.exit(1)
    with report_path.open('r', encoding ='utf-8') as report_file:
        for line in report_file.readlines():
            sub_report = json.loads(line)
            report[sub_report['isin']] = sub_report
            if display_report:
                display.print_report(sub_report)
    return report

def report_valorisation(old_report, new_report, html_tag):
    """
    Report the valorisation
    """
    if is_different_and_valid(old_report, new_report, 'LVAL_NORM'):
        evo_valorisation = round(100 * (-1 + \
            float(new_report['LVAL_NORM']['v']) / float(old_report['LVAL_NORM']['v'])), 2)
        sign = get_sign(evo_valorisation)
        if sign == '+':
            evo_valorisation = f'{html_tag["green_in"]}{sign}{evo_valorisation} %{html_tag["green_out"]}'
        else:
            evo_valorisation = f'{html_tag["red_in"]}{sign}{evo_valorisation} %{html_tag["red_out"]}'
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution valorisation{html_tag["bold_out"]}: {evo_valorisation}{html_tag["li_out"]}')
        currency = ''
        if 'M_CUR' in new_report:
            currency = ' '+new_report['M_CUR']['v']
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution valorisation{html_tag["bold_out"]}: {old_report["LVAL_NORM"]["v"]} -> {new_report["LVAL_NORM"]["v"]}{currency}{html_tag["li_out"]}')

def report_per(old_report, new_report, html_tag):
    """
    Report the PER
    """
    if is_different_and_valid(old_report, new_report, 'PER_ANNEE_ESTIMEE'):
        evo_per = round(float(new_report['PER_ANNEE_ESTIMEE']['v']) - float(old_report['PER_ANNEE_ESTIMEE']['v']), 1)
        evo_per = f'{html_tag["blue_in"]}{get_sign(evo_per)}{evo_per}{html_tag["blue_out"]}'
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PER{html_tag["bold_out"]}: {evo_per}{html_tag["li_out"]}')
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PER{html_tag["bold_out"]}: {old_report["PER_ANNEE_ESTIMEE"]["v"]} -> {new_report["PER_ANNEE_ESTIMEE"]["v"]}{html_tag["li_out"]}')
        if analysis.per_text(old_report['PER_ANNEE_ESTIMEE']['v']) != analysis.per_text(new_report['PER_ANNEE_ESTIMEE']['v']):
            print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PER{html_tag["bold_out"]}: {analysis.per_text(old_report["PER_ANNEE_ESTIMEE"]["v"])} -> {analysis.per_text(new_report["PER_ANNEE_ESTIMEE"]["v"])}{html_tag["li_out"]}')

def report_peg(old_report, new_report, html_tag):
    """
    Report the PEG
    """
    if is_different_and_valid(old_report, new_report, 'peg'):
        evo_peg = round(float(new_report['peg']) - float(old_report['peg']), 1)
        evo_peg = f'{html_tag["blue_in"]}{get_sign(evo_peg)}{evo_peg}{html_tag["blue_out"]}'
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PEG{html_tag["bold_out"]}: {evo_peg}{html_tag["li_out"]}')
        print(f'{html_tag["li_in"]}{html_tag["bold_in"]}Evolution PEG{html_tag["bold_out"]}: {old_report["peg"]} -> {new_report["peg"]}{html_tag["li_out"]}')

def diff_report(oldest_file, newer_file, isin_compare, is_html):
    """
    Compare two report
    """
    html_tag = {
        'bold_in': '',
        'bold_out': '',
        'h3_in': '',
        'h3_out': '',
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
            'h3_in': '<h3>',
            'h3_out': '</h3>',
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
        print(f'{html_tag["h3_in"]}{new_report["DISPLAY_NAME"]["v"]} ({new_report["isin"]}){html_tag["h3_out"]}')

        report_valorisation(old_report, new_report, html_tag)

        report_per(old_report, new_report, html_tag)

        report_peg(old_report, new_report, html_tag)

        if is_html:
            print('</ul></div>')
        else:
            print('==============')
    if is_html:
        print('</body></html>')


def get_negative_values(oldest_file, newer_file, isin_compare):
    """
    Check for negative valorisation and return corresponding ISINs
    """
    old_reports = load_report(oldest_file, display_report=False)
    new_reports = load_report(newer_file, display_report=False)

    negative_valorisation_isins = []
    equal_valorisation_isins = []

    for _isin in isin_compare:
        if _isin not in old_reports or _isin not in new_reports:
            continue
        old_report = old_reports[_isin]
        new_report = new_reports[_isin]

        # Check if 'LVAL_NORM' is in report and if its value is less than 0
        if 'LVAL_NORM' in new_report and new_report['LVAL_NORM']['v'] is not None:
            if float(new_report['LVAL_NORM']['v']) - float(old_report['LVAL_NORM']['v']) < 0:
                negative_valorisation_isins.append(new_report['isin'])
            if float(new_report['LVAL_NORM']['v']) == float(old_report['LVAL_NORM']['v']):
                equal_valorisation_isins.append(new_report['isin'])

    return negative_valorisation_isins, equal_valorisation_isins


def diff3_report(directory, isin_compare, is_html):
    """
    Compare two report
    """
    html_tag = {
        'bold_in': '',
        'bold_out': '',
        'h3_in': '',
        'h3_out': '',
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
            'h3_in': '<h3>',
            'h3_out': '</h3>',
            'li_in': '<li>',
            'li_out': '</li>',
            'red_in': '<span style="color: #f00;">',
            'red_out': '</span>',
            'green_in': '<span style="color: #18b724;">',
            'green_out': '</span>',
            'blue_in': '<span style="color: #007eff;">',
            'blue_out': '</span>',
        }

    # Get a list of all report files in the directory, sorted by creation time
    report_files = sorted(glob.glob(os.path.join(directory, '*.txt')))

    # Take only the last 7 files
    report_files = report_files[-7:]

    count_negative_isins = {}
    for i in range(len(report_files) - 1):
        negative_isins, equal_isins = get_negative_values(report_files[i], report_files[i+1], isin_compare)

        # Initialize isin in negative_isins
        for _isin in negative_isins:
            if _isin not in count_negative_isins:
                count_negative_isins[_isin] = 0

        # Update count
        for _isin in count_negative_isins:
            if _isin in negative_isins:
                count_negative_isins[_isin] += 1
            elif _isin not in equal_isins:
                count_negative_isins[_isin] = 0

    if is_html:
        print('<html><body>')

    for _isin in count_negative_isins:
        if count_negative_isins[_isin] >= 2:
            print(f'{html_tag["h3_in"]}{_isin}: {count_negative_isins[_isin]} days in a row !{html_tag["h3_out"]}')
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

    # DIFF3 Arguments
    DIFF3_PARSER = SUBPARSERS.add_parser('diff3',\
        help='Diff3 command')
    DIFF3_PARSER.add_argument('directory', action='store',\
        help='Directory with reports for comparison')
    DIFF3_PARSER.add_argument('--html', action='store_true',\
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
    elif sys.argv[1] == 'diff3':
        diff3_report(ARGS.directory, settings.ISIN_COMPARE, ARGS.html)

    sys.exit(0)
