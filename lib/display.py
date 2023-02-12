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
    if 'CUSTOM_DIVIDEND_PERCENT' in report:
        print(f"||           : {report['CUSTOM_DIVIDEND_PERCENT']} %")
    if 'CROISSANCE_BNPA_ANNEEN2' in report:
        print(f"|| Croissance BNPA: {round(report['CROISSANCE_BNPA_ANNEEN2']['v'])} % -> {round(report['CROISSANCE_BNPA_ANNEE_PRECEDENTE']['v'])} % -> {round(report['CROISSANCE_BNPA_ANNEE_COURANTE']['v'])} %")
    if 'CROISSANCE_CA_ANNEEN2' in report:
        print(f"|| Croissance CA: {round(report['CROISSANCE_CA_ANNEEN2']['v'])} % -> {round(report['CROISSANCE_CA_ANNEE_PRECEDENTE']['v'])} % -> {round(report['CROISSANCE_CA_ANNEE_COURANTE']['v'])} %")
    if 'PER_ANNEE_ESTIMEE' in report:
        print(f"|| PER prévisionel: {round(report['PER_ANNEE_ESTIMEE']['v'], 2)} ({analysis.per_text(report['PER_ANNEE_ESTIMEE']['v'])})")
    if report['CUSTOM_PEG'] != '-':
        print(f"|| PEG prévisionel: {report['CUSTOM_PEG']} ({analysis.peg_text(report['CUSTOM_PEG'])})")
    if report['CUSTOM_PEG_MAISON'] != '-':
        print(f"|| PEG réaliste: {report['CUSTOM_PEG_MAISON']} ({analysis.peg_text(report['CUSTOM_PEG_MAISON'])})")
    print('--')
    if 'DIV_ANNEE_PRECEDENTE' in report:
        print(f"|| Dividende Année précédente: {report['DIV_ANNEE_PRECEDENTE']['v']} {report['M_CUR']['v']}")
    if 'CUSTOM_DIVIDEND_ANNEE_PRECEDENTE_PERCENT' in report:
        print(f"||                           : {report['CUSTOM_DIVIDEND_ANNEE_PRECEDENTE_PERCENT']} %")
    if 'PER_ANNEE_PRECEDENTE' in report:
        print(f"|| PER Année précédente: {round(report['PER_ANNEE_PRECEDENTE']['v'], 2)} ({analysis.per_text(report['PER_ANNEE_PRECEDENTE']['v'])})")
    if report['CUSTOM_PEG_ANNEE_PRECEDENTE'] != '-':
        print(f"|| PEG Année précédente: {report['CUSTOM_PEG_ANNEE_PRECEDENTE']} ({analysis.peg_text(report['CUSTOM_PEG_ANNEE_PRECEDENTE'])})")

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
