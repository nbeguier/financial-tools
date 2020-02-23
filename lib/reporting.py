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

# Debug
# from pdb import set_trace as st

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

def compute_benefices(report):
    """
    Get necessary informations and returns an approximation of the profit development
    """
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
    return None

def compute_peg(profit, infos_boursiere):
    """
    Returns an approximation of the PEG
    """
    if not 'PER' in infos_boursiere:
        return 0
    if profit is None:
        return None
    per = float(infos_boursiere['PER'].split()[0])
    if profit <= 0:
        return 0
    return round(per/profit, 1)

def get_brsrm(isin):
    """
    Return Brsrm
    """
    base_url = common.decode_rot('uggcf://jjj.obhefbenzn.pbz')
    search_path = common.decode_rot('/erpurepur/nwnk?dhrel=')
    content = cache.get(base_url+search_path+isin)
    if not content:
        return None
    soup = BeautifulSoup(content, 'html.parser')
    path = soup.find('a', 'search__list__link')['href']
    return base_url+path

def get_potential(url_brsrm):
    """
    Returns the potential for 3 month
    """
    if not url_brsrm:
        return None
    content = cache.get(url_brsrm)
    if not content:
        return None
    soup = BeautifulSoup(content, 'html.parser')
    potential = None
    for i in soup.find_all('p'):
        if 'Objectif de cours' in i.text:
            value = i.find('span', 'u-text-bold')
            if not value:
                return None
            potential = common.clean_data(value.text, json_load=False).split()[0]
    return potential

def get_trend(base_url):
    """
    Returns trend short/mid term
    """
    report = dict()
    report['short term'] = None
    report['mid term'] = None
    if not base_url:
        return report
    url = base_url.replace('/action-', '/recommandations-action-')
    content = cache.get(url)
    if not content:
        return report
    soup = BeautifulSoup(content, 'html.parser')
    for i in soup.find_all('div', 'tendance hausse'):
        if 'court terme' in i.text:
            report['short term'] = 'Hausse'
        if 'moyen terme' in i.text:
            report['mid term'] = 'Hausse'
    for i in soup.find_all('div', 'tendance egal'):
        if 'court terme' in i.text:
            report['short term'] = 'Egal'
        if 'moyen terme' in i.text:
            report['mid term'] = 'Egal'
    for i in soup.find_all('div', 'tendance baisse'):
        if 'court terme' in i.text:
            report['short term'] = 'Baisse'
        if 'moyen terme' in i.text:
            report['mid term'] = 'Baisse'
    return report

def simplify_report(report, parameters):
    """
    Returns a simplified version of the report
    """
    simple_report = dict()
    simple_report['isin'] = report['isin']
    simple_report['url'] = report['url']
    simple_report['potential'] = report['potential']
    simple_report['url_brsrm'] = report['url_brsrm']
    simple_report['trend'] = report['trend']

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
                compute_benefices(report),
                report['infos_boursiere'])
    report['trend'] = get_trend(report['url'])
    report['url_brsrm'] = get_brsrm(parameters['isin'])
    report['potential'] = get_potential(report['url_brsrm'])

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
