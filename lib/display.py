#!/usr/bin/env python3
"""
Display library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Own library
# pylint: disable=E0401
import lib.analysis as analysis

def print_report(report, place='XPAR', display_urls=True):
    """
    Prints the report
    """
    print('ISIN: {}'.format(report['isin']))
    if 'nom' in report:
        print('Nom: {}'.format(report['nom']))
    if 'secteur' in report:
        print('Secteur: {}'.format(report['secteur']))
    if 'valorisation' in report:
        print('Valorisation: {} EUR'.format(report['valorisation']))
        print('Variation 1 an: {} %'.format(report['valorisation_1an']))
    if 'Dividendes' in report:
        print('|| Dividendes: {} EUR'.format(report['Dividendes']))
        print('|| PER: {} ({})'.format(report['PER'], analysis.per(report['PER'])))
        print('|| Rendement: {} %'.format(report['Rendement']))
        print('|| Détachement: {}'.format(report['Détachement']))
        print('|| Prochain rdv: {}'.format(report['Prochain rdv']))
    if 'dividendes' in report:
        print('>> [{}] Rendement: {} %'.format(
            report['dividendes']['last_year'],
            report['dividendes']['last_rendement']))
        print('>> [{}] Valorisation: {} EUR'.format(
            report['dividendes']['last_year'],
            report['dividendes']['average_val']))
        print('>> [{}] Valorisation: {} EUR'.format(
            report['dividendes']['last_detach'],
            report['dividendes']['last_val']))
        print('>> [{}] Valorisation: {} EUR'.format(
            report['dividendes']['latest_detach'],
            report['dividendes']['latest_val']))
    if 'benefices' in report:
        print('>> Evolution bénéfices: {} %'.format(report['benefices']))
    if 'peg' in report:
        print('>> PEG: {}'.format(report['peg']))
    if display_urls:
        print('==============')
        if report['url'] is not None:
            print('Les Echos: {}'.format(report['url']))
        if place == 'XPAR':
            print('Recapitulatif dividendes: https://www.bnains.org' +
                  '/archives/action.php?' +
                  'codeISIN={}'.format(report['isin']))
            print('Palmares CAC40 dividendes: https://www.boursorama.com' +
                  '/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6')
    print('==============')
