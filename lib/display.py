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
        print('|| PER: {} ({})'.format(report['PER'], analysis.per_text(report['PER'])))
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
        print('>> PEG: {} ({})'.format(
            report['peg'], analysis.peg_text(report['peg'])))
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

def print_per(pers):
    """
    Prints PER informations
    """
    for per in pers:
        if pers[per]['current']:
            print('PER {} actuel: {} EUR'.format(
                round(per, 1),
                round(pers[per]['value'], 2)))
        else:
            print('[{}] PER {} ({}): {} EUR'.format(
                pers[per]['date'],
                per,
                analysis.per_text(per),
                round(pers[per]['value'], 2)))

def print_peg(pegs):
    """
    Prints PEG informations
    """
    for peg in pegs:
        if pegs[peg]['current']:
            print('PEG {} actuel: {} EUR'.format(
                round(peg, 1),
                round(pegs[peg]['value'], 2)))
        else:
            print('[{}] PEG {} ({}): {} EUR'.format(
                pegs[peg]['date'],
                peg,
                analysis.peg_text(peg),
                round(pegs[peg]['value'], 2)))
