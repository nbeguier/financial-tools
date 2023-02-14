#!/usr/bin/env python3
"""
Display library

Copyright (c) 2020-2023 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Own library
# pylint: disable=E0401
from lib import analysis

# Debug
# from pdb import set_trace as st

def display_header(report):
    """
    Display the header
    """
    print(f"Nom: {report['DISPLAY_NAME']['v']}")
    print(f"Secteur: {report['SEC']['description']}")
    print(f"Valorisation: {report['LVAL_NORM']['v']} {report['M_CUR']['v']}")
    print(f"Variation 1 an: {round(report['52W_PERF_PR']['v'], 2)} %")

def display_body(report):
    """
    Display the body
    """
    if 'DIVIDEND' in report:
        print(f"|| Dividendes: {report['DIVIDEND']['v']} {report['M_CUR']['v']}")
    if 'DIVIDEND' in report and 'CUSTOM_DIVIDEND_PERCENT' in report:
        print(f"||           : {report['CUSTOM_DIVIDEND_PERCENT']} %")
    if 'CUSTOM_PER' in report and report['CUSTOM_PER'] != '-':
        print(f"|| PER estimé: {report['CUSTOM_PER']} ({analysis.per_text(report['CUSTOM_PER'])})")
    if 'CUSTOM_PEG' in report and report['CUSTOM_PEG'] != '-':
        print(f"|| PEG estimé: {report['CUSTOM_PEG']} ({analysis.peg_text(report['CUSTOM_PEG'])})")
    print('--')
    if 'DIV_ANNEE_PRECEDENTE' in report:
        print(f"|| Dividende Année précédente: {report['DIV_ANNEE_PRECEDENTE']['v']} {report['M_CUR']['v']}")
    if 'DIV_ANNEE_PRECEDENTE' in report and 'CUSTOM_DIVIDEND_ANNEE_PRECEDENTE_PERCENT' in report:
        print(f"||                           : {report['CUSTOM_DIVIDEND_ANNEE_PRECEDENTE_PERCENT']} %")

def print_report(report, header=True):
    """
    Prints the report
    """
    if report is None:
        print('Nothing found...')
        return
    print(f"ISIN: {report['ISIN']['v']}")
    if header:
        display_header(report)
    display_body(report)
    print('==============')
