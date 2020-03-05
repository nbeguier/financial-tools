#!/usr/bin/env python3
"""
Reporting library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import json
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

def get_cours(isin, mic, disable_cache=False):
    """
    Returns core info from isin
    """
    url = common.decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          common.decode_rot('/fgernzvat/pbhef/trgPbhef?') + \
          'code={}&place={}&codif=ISIN'.format(isin, mic)
    content = cache.get(url, verify=False, disable_cache=disable_cache)
    cours = None
    if content:
        cours = common.clean_data(content)
    return cours

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
        # pylint: disable=W1401
        name = re.sub(' \(.*\)', '', name)
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


def get_url_echos(isin, mic):
    """
    Return Echos URL
    """
    url = common.decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          common.decode_rot('/fgernzvat/pbhef/oybpf/trgUrnqreSvpur?') + \
          'code={}&place={}&codif=ISIN'.format(isin, mic)
    content = cache.get(url, verify=False)
    if not content:
        return None
    header_fiche = common.clean_data(content)
    url_echos = common.clean_url(header_fiche['headerFiche']['tweetHeaderFiche'])
    return url_echos

def get_url_brsrm(isin):
    """
    Return Brsrm URL
    """
    base_url = common.decode_rot('uggcf://jjj.obhefbenzn.pbz')
    search_path = common.decode_rot('/erpurepur/nwnk?dhrel=')
    content = cache.get(base_url+search_path+isin)
    if not content:
        return None
    soup = BeautifulSoup(content, 'html.parser')
    path = soup.find('a', 'search__list__link')['href']
    return base_url+path

def get_url_frtn(isin):
    """
    Return Frtn URL
    """
    base_url = 'https://bourse.fortuneo.fr/api/search?term={}'.format(isin)
    content = cache.get(base_url)
    if not content:
        return None
    try:
        json_content = json.loads(content)
    except json.decoder.JSONDecodeError:
        return None
    try:
        url = json_content['searchResults']['market']['arkea']['items'][0]['url']
    except (KeyError, IndexError):
        return None
    return url

def get_potential(url_brsrm, url_frtn, cours):
    """
    Returns the potential for 3 month
    """
    report = dict()
    report['brsrm'] = dict()
    report['brsrm']['value'] = None
    report['brsrm']['percentage'] = 0
    report['frtn'] = dict()
    report['frtn']['value'] = None
    report['frtn']['percentage'] = 0
    if url_brsrm:
        content = cache.get(url_brsrm)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            for i in soup.find_all('p'):
                if 'Objectif de cours' in i.text:
                    value = i.find('span', 'u-text-bold')
                    if not value:
                        return report
                    report['brsrm']['value'] = common.clean_data(
                        value.text, json_load=False).split()[0]
                    if cours:
                        val = float(cours['cotation']['valorisation'].replace(',', '.'))
                        report['brsrm']['percentage'] = round(
                            (float(report['brsrm']['value']) / val - 1)*100, 1)
    if url_frtn:
        market = int(url_frtn.split('-')[-1])
        isin = url_frtn.split('-')[-2]
        avis_url = common.decode_rot('uggcf://obhefr.sbegharb.se/ncv/inyhr/nivf/SGA') + \
            '{market:06d}{isin}'.format(market=market, isin=isin)
        content = cache.get(avis_url)
        if content:
            try:
                json_content = json.loads(content)
                report['frtn']['value'] = json_content['consensus']['objectif']
                report['frtn']['percentage'] = round(
                    float(json_content['consensus']['potentiel'])*100, 1)
            except json.decoder.JSONDecodeError:
                pass
    return report

def get_trend(url_echos, url_frtn):
    """
    Returns trend short/mid term
    """
    report = dict()
    report['echos'] = dict()
    report['echos']['short term'] = None
    report['echos']['mid term'] = None
    report['frtn'] = dict()
    report['frtn']['short term'] = None
    report['frtn']['mid term'] = None
    report['bnp'] = dict()
    report['bnp']['short term'] = None
    report['bnp']['mid term'] = None
    # Echos
    if url_echos:
        url = url_echos.replace('/action-', '/recommandations-action-')
        content = cache.get(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            for i in soup.find_all('div', 'tendance hausse'):
                if 'court terme' in i.text:
                    report['echos']['short term'] = 'Hausse'
                if 'moyen terme' in i.text:
                    report['echos']['mid term'] = 'Hausse'
            for i in soup.find_all('div', 'tendance egal'):
                if 'court terme' in i.text:
                    report['echos']['short term'] = 'Neutre'
                if 'moyen terme' in i.text:
                    report['echos']['mid term'] = 'Neutre'
            for i in soup.find_all('div', 'tendance baisse'):
                if 'court terme' in i.text:
                    report['echos']['short term'] = 'Baisse'
                if 'moyen terme' in i.text:
                    report['echos']['mid term'] = 'Baisse'
    # Frtn
    if url_frtn:
        market = int(url_frtn.split('-')[-1])
        isin = url_frtn.split('-')[-2]
        trend_url = common.decode_rot('uggcf://obhefr.sbegharb.se/ncv/inyhr/geraqf/NPGVBAF/SGA') + \
            '{market:06d}{isin}'.format(market=market, isin=isin)
        content = cache.get(trend_url)
        if content and content != 'null':
            try:
                json_content = json.loads(content)
                mapping = {
                    'POSITIVE': 'Hausse',
                    'NEUTRE': 'Neutre',
                    'NEGATIVE': 'Baisse',
                }
                if 'opinionCT' in json_content and json_content['opinionCT'] in mapping:
                    report['frtn']['short term'] = mapping[json_content['opinionCT']]
                if 'opinionMT' in json_content and json_content['opinionMT'] in mapping:
                    report['frtn']['mid term'] = mapping[json_content['opinionMT']]
            except json.decoder.JSONDecodeError:
                pass
    # BNP
    trend_url = common.decode_rot('uggcf://ppvjro.oaccnevonf.pbz/ri/se/terraonax/-;'+ \
        'rifvq=fHXKzv85nNLdRgeWB8AO-0TPC4JTJ7FDJO63tOwt.aqyc-ppvjro-nf07')
    payload = common.decode_rot('%24cneg=oacc.znexrgqngn.fancfubgObql&%24rirag=ybnq') + \
        common.decode_rot('&znaqngbelSvryqf%5O%5Q=frphevglGlcr&znaqngbelSvryqf%5O%5Q=vq') + \
        common.decode_rot('&znaqngbelSvryqf%5O%5Q=bevtvanyFrphevgl&znaqngbelSvryqf%5O%5Q') + \
        common.decode_rot('=rkpunatrPbqr&cersvk=ppv.znexrgqngn.fancfubg&oy=terraonax&br=se') + \
        '&id='+ isin + common.decode_rot('&frphevglGlcr=fgbpxf&zvo_hfre_ybttva=snyfr')
    content = cache.post(trend_url, payload)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        mapping = {
            'termArrow2': 'Hausse',
            'termArrow1': 'Hausse',
            'termArrow0': 'Neutre',
            'termArrow-1': 'Baisse',
            'termArrow-2': 'Baisse',
            'termArrown.c.': None,
        }
        try:
            table = soup.find('table', 'analysisTeaserTable').find('tr', 'even-row')
            report['bnp']['short term'] = mapping[table.find_all('div')[0]['class'][0]]
            report['bnp']['mid term'] = mapping[table.find_all('div')[1]['class'][0]]
        except (IndexError, AttributeError):
            pass
    return report

def get_dividend(infos_boursiere, url_brsrm, url_frtn):
    """
    Compute the next dividend value
    """
    report = dict()
    report['echos'] = dict()
    report['echos']['percent'] = None
    report['brsrm'] = dict()
    report['brsrm']['percent'] = None
    report['frtn'] = dict()
    report['frtn']['percent'] = None
    report['average_percent'] = 0

    if infos_boursiere and 'Rendement' in infos_boursiere:
        report['echos']['percent'] = float(infos_boursiere['Rendement'])

    if url_brsrm:
        content = cache.get(url_brsrm)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            for div_relative in soup.find_all('div', 'u-relative'):
                if 'Rendement' not in div_relative.text:
                    continue
                if len(div_relative.find_all('td')) < 6:
                    continue
                report['brsrm']['percent'] = float(
                    common.clean_data(div_relative.find_all('td')[6].\
                    text, json_load=False).split()[0].split('%')[0])

    if url_frtn:
        market = int(url_frtn.split('-')[-1])
        isin = url_frtn.split('-')[-2]
        avis_url = common.decode_rot('uggcf://obhefr.sbegharb.se/ncv/inyhr/nivf/SGA') + \
            '{market:06d}{isin}'.format(market=market, isin=isin)
        content = cache.get(avis_url)
        if content:
            try:
                json_content = json.loads(content)
                if len(json_content['consensus']['listeAnnee']) > 1:
                    report['frtn']['percent'] = round(float(
                        json_content['consensus']['listeAnnee'][1]['rendement'])*100, 2)
            except json.decoder.JSONDecodeError:
                pass

    count = 0
    for url in report:
        if isinstance(report[url], dict) and 'percent' in report[url] and report[url]['percent']:
            report['average_percent'] += float(report[url]['percent'])
            count += 1
    if count != 0:
        report['average_percent'] = round(report['average_percent']/count, 2)
    else:
        report['average_percent'] = '-'
    return report

def simplify_report(report, parameters):
    """
    Returns a simplified version of the report
    """
    simple_report = dict()
    simple_report['isin'] = report['isin']
    simple_report['potential'] = report['potential']
    simple_report['url_echos'] = report['url_echos']
    simple_report['url_brsrm'] = report['url_brsrm']
    simple_report['url_frtn'] = report['url_frtn']
    simple_report['trend'] = report['trend']
    simple_report['dividend'] = report['dividend']

    if report['cours'] is not None:
        simple_report['nom'] = report['cours']['cotation']['name']
    if 'sector' in report and 'sub_sector' in report:
        simple_report['secteur'] = '{} / {}'.format(report['sector'], report['sub_sector'])
    if report['cours'] is not None:
        simple_report['valorisation'] = report['cours']['cotation']['valorisation'].\
            split()[0].replace(',', '.')
        simple_report['valorisation_1an'] = report['cours']['cotation']['variationYear'].\
            replace(',', '.')
    for info in INFOS_BOURSIERE:
        simple_report[info] = None
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

    report['cours'] = get_cours(parameters['isin'], parameters['mic'])

    report['url_echos'] = get_url_echos(parameters['isin'], parameters['mic'])
    report['url_brsrm'] = get_url_brsrm(parameters['isin'])
    report['url_frtn'] = get_url_frtn(parameters['isin'])

    report['infos_boursiere'] = dict()
    if report['url_echos'] is not None:
        content = cache.get(report['url_echos'])
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
    report['trend'] = get_trend(report['url_echos'], report['url_frtn'])
    report['potential'] = get_potential(report['url_brsrm'], report['url_frtn'], report['cours'])
    report['dividend'] = get_dividend(report['infos_boursiere'], report['url_brsrm'], report['url_frtn'])

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
