#!/usr/bin/env python3
"""
Reporting library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import re

# Third party library imports
from bs4 import BeautifulSoup

# Own library
# pylint: disable=E0401
import lib.cache as cache
import lib.common as common
import lib.history as history

# 'Capitalisation' isin removed
INFOS_BOURSIERE = ['Dividendes', 'PER', 'Rendement', 'Detachement', 'Prochain rdv']

def extract_infos_boursiere(data):
    """
    Extracts dictionnary from list
    """
    report = dict()
    splitted_data = common.clean_data(data.get_text().replace('\n', ' '), json_load=False).split()
    for i, key in enumerate(splitted_data):
        if key == 'Dividendes' \
            and i < len(splitted_data) \
            and splitted_data[i+1] not in INFOS_BOURSIERE:
            report[key] = splitted_data[i+1].replace(',', '.')
        elif key == 'PER' \
            and i < len(splitted_data) \
            and splitted_data[i+1] not in INFOS_BOURSIERE:
            if splitted_data[i+1].replace(',', '.') == '-':
                report[key] = '0'
            else:
                report[key] = splitted_data[i+1].replace(',', '.')
        elif key == 'Rendement' \
            and i < len(splitted_data) \
            and splitted_data[i+1] not in INFOS_BOURSIERE:
            report[key] = splitted_data[i+1].replace(',', '.')
        elif key == 'Détachement' \
            and i < len(splitted_data) \
            and splitted_data[i+1] not in INFOS_BOURSIERE:
            report['Detachement'] = splitted_data[i+1]
        elif key == 'rdv' \
            and i < len(splitted_data) \
            and splitted_data[i+1] not in INFOS_BOURSIERE:
            report['Prochain rdv'] = splitted_data[i+1]
    return report

def parse_profit(soup, report):
    """
    Parse the html output and returns an approximation of the profit development
    """
    profit = 0
    for raw_data in soup.find_all('tr', 'c-table__row'):
        data = common.clean_data(raw_data.get_text(), json_load=False).split()
        name = ''
        end_name = False
        for char in data:
            if re.search('[0-9]', char):
                char = re.sub('[0-9].*$', '', char)
                end_name = True
            if char == 'CIE':
                char = 'COMPAGNIE'
            name += char
            if end_name:
                break
            name += ' '
        if name.upper() in report['cours']['cotation']['name'].upper():
            if float(data[-4]) == 0:
                return profit
            profit = 100 * (float(data[-2]) / float(data[-4]) - 1)
    return profit

def compute_benefices(report, parameters):
    """
    Get necessary informations and returns an approximation of the profit development
    """
    indice = '1eCPNP'
    if parameters['indice'] != 'cac40':
        indice = '1eCCK5'
    count = 1
    continue_req = True
    while continue_req:
        url = common.decode_rot(
            'uggcf://jjj.obhefbenzn.pbz/obhefr/npgvbaf/' +
            'cnyznerf/qvivqraqrf/cntr-{}?'.format(count) +
            'znexrg={}&inevngvba=6'.format(indice))
        content = cache.get(url)
        continue_req = content != ''
        if continue_req:
            profit = parse_profit(BeautifulSoup(content, 'html.parser'), report)
            if profit != 0:
                return profit
        count += 1
    return 0

def compute_peg(profit, infos_boursiere):
    """
    Returns an approximation of the PEG
    """
    if not 'PER' in infos_boursiere:
        return 0
    per = float(infos_boursiere['PER'].split()[0])
    if profit <= 0:
        return 0
    return round(per/profit, 1)

def simplify_report(report, parameters):
    """
    Returns a simplified version of the report
    """
    simple_report = dict()
    simple_report['isin'] = report['isin']
    simple_report['url'] = report['url']

    if report['cours'] is not None:
        simple_report['nom'] = report['cours']['cotation']['name']
    if 'sector' in report and 'sub_sector' in report:
        simple_report['secteur'] = '{} / {}'.format(report['sector'], report['sub_sector'])
    if report['cours'] is not None:
        simple_report['valorisation'] = report['cours']['cotation']['valorisation'].\
            split()[0].replace(',', '.')
        simple_report['valorisation_1an'] = report['cours']['cotation']['variationYear'].\
            replace(',', '.')
    if 'infos_boursiere' in report:
        for info in report['infos_boursiere']:
            simple_report[info] = report['infos_boursiere'][info]
    if parameters['history']['dividendes'] and 'dividendes' in report['history']:
        simple_report['dividendes_history'] = report['history']['dividendes']
    if parameters['history']['per'] and 'per' in report['history']:
        simple_report['per_history'] = report['history']['per']
    if parameters['history']['peg'] and 'peg' in report['history']:
        simple_report['peg_history'] = report['history']['peg']
    return simple_report

def get_report(parameters):
    """
    Returns a report of all metadata from the input ISIN
    """
    report = dict()
    report['isin'] = parameters['isin']
    url = common.decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          common.decode_rot('/fgernzvat/pbhef/trgPbhef?') + \
          'code={}&place={}&codif=ISIN'.format(parameters['isin'], parameters['mic'])
    content = cache.get(url, verify=False)
    report['cours'] = None
    if content:
        report['cours'] = common.clean_data(content)

    url = common.decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          common.decode_rot('/fgernzvat/pbhef/oybpf/trgUrnqreSvpur?') + \
          'code={}&place={}&codif=ISIN'.format(parameters['isin'], parameters['mic'])
    content = cache.get(url, verify=False)
    header_fiche = None
    report['url'] = None
    if content:
        header_fiche = common.clean_data(content)
        report['url'] = common.clean_url(header_fiche['headerFiche']['tweetHeaderFiche'])

    report['infos_boursiere'] = dict()
    if report['url'] is not None:
        content = cache.get(report['url'])
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            for tab in soup.find_all('table'):
                if 'Dividendes' in tab.get_text():
                    report['infos_boursiere'] = extract_infos_boursiere(tab)
            sector = soup.find('a', id='sectorLink')
            if sector is not None:
                report['sector'] = common.clean_data(
                    sector.get_text(),
                    json_load=False)
            sub_sector = soup.find('a', id='subSectorLink')
            if sub_sector is not None:
                report['sub_sector'] = common.clean_data(
                    sub_sector.get_text(),
                    json_load=False)
            report['infos_boursiere']['PEG'] = compute_peg(
                compute_benefices(report, parameters),
                report['infos_boursiere'])

    report['history'] = dict()
    if parameters['history']['dividendes']:
        report['history']['dividendes'] = history.dividendes(
            parameters, report['infos_boursiere'])

    if parameters['history']['per']:
        report['history']['per'] = history.per(
            parameters, simplify_report(report, parameters))

    if parameters['history']['peg']:
        report['history']['peg'] = history.peg(
            parameters, simplify_report(report, parameters), report['infos_boursiere']['PEG'])

    return report
