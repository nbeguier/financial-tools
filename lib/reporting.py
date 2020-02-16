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
from requests import Session
import urllib3

# Own library
# pylint: disable=E0401
import lib.common as common

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SESSION = Session()
HEADERS = common.gen_headers()

# 'Capitalisation' isin removed
INFOS_BOURSIERE = ['Dividendes', 'PER', 'Rendement', 'Détachement', 'Prochain rdv']

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
            report[key] = splitted_data[i+1].replace(',', '.')
        elif key == 'Rendement' \
            and i < len(splitted_data) \
            and splitted_data[i+1] not in INFOS_BOURSIERE:
            report[key] = splitted_data[i+1].replace(',', '.')
        elif key == 'Détachement' \
            and i < len(splitted_data) \
            and splitted_data[i+1] not in INFOS_BOURSIERE:
            report[key] = splitted_data[i+1]
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
        if re.sub('[0-9].*$', '', data[0]).upper() in report['cours']['cotation']['name'].upper():
            profit = 100 * (float(data[-2]) / float(data[-4]) - 1)
    return profit

def compute_extra_dividendes(parameters, infos_boursiere):
    """
    Returns extra info about dividendes
    """
    report = dict()
    report['last_rendement'] = 'Unknown'
    report['last_val'] = 'Unknown'
    report['latest_val'] = 'Unknown'
    report['average_val'] = 'Unknown'
    report['last_detach'] = 'Unknown'
    report['latest_detach'] = 'Unknown'
    report['last_year'] = 'Unknown'
    if 'Détachement' not in infos_boursiere:
        return report
    url = common.decode_rot(
        'uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg/SQF/uvfgbel.kzy?' +
        'ragvgl=rpubf&ivrj=NYY&pbqvsvpngvba=VFVA&rkpunatr=KCNE&' +
        'nqqQnlYnfgCevpr=snyfr&nqwhfgrq=gehr&onfr100=snyfr&' +
        'frffJvguAbDhbg=snyfr&crevbq=3L&tenahynevgl=&aoFrff=&' +
        'vafgeGbPzc=haqrsvarq&vaqvpngbeYvfg=&pbzchgrIne=gehr&' +
        'bhgchg=pfiUvfgb&') + 'code={}'.format(parameters['isin'])
    req = SESSION.get(url, verify=False)
    if req.ok and infos_boursiere['Détachement'] != '-':
        matching_date = infos_boursiere['Détachement'].split('/')
        latest_matching_date = '20{:02d}/{}/'.format(
            int(matching_date[2])-1, matching_date[1])
        matching_date = '20{}/{}/{}'.format(
            matching_date[2], matching_date[1], matching_date[0])
        open_value = None
        latest_open_value = None
        for line in req.text.split('\n'):
            date = line.split(';')[0]
            if date == matching_date:
                open_value = float(line.split(';')[1])
            elif latest_matching_date in date:
                latest_matching_date = date
                latest_open_value = float(line.split(';')[1])
        if open_value is not None and latest_open_value is not None:
            dividendes = float(infos_boursiere['Dividendes'].split()[0])
            average_val = (open_value+latest_open_value)/2
            rendement = 100 * dividendes / average_val
            report['last_rendement'] = round(rendement, 2)
            report['last_val'] = round(open_value, 2)
            report['latest_val'] = round(latest_open_value, 2)
            report['average_val'] = round(average_val, 2)
            report['last_detach'] = matching_date
            report['latest_detach'] = latest_matching_date
            report['last_year'] = latest_matching_date.split('/')[0]
    return report

def compute_extra_benefices(report):
    """
    Get necessary informations and returns an approximation of the profit development
    """
    profit = 0
    url_1 = common.decode_rot(
        'uggcf://jjj.obhefbenzn.pbz/obhefr/npgvbaf/cnyznerf/qvivqraqrf/cntr-1?' +
        'znexrg=1eCPNP&inevngvba=6')
    url_2 = common.decode_rot(
        'uggcf://jjj.obhefbenzn.pbz/obhefr/npgvbaf/cnyznerf/qvivqraqrf/cntr-2?' +
        'znexrg=1eCPNP&inevngvba=6')
    req = SESSION.get(url_1)
    if req.ok:
        profit += parse_profit(BeautifulSoup(req.text, 'html.parser'), report)
    req = SESSION.get(url_2)
    if req.ok:
        profit += parse_profit(BeautifulSoup(req.text, 'html.parser'), report)
    return round(profit, 2)

def compute_extra_peg(profit, infos_boursiere):
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
    if parameters['extra']['dividendes']:
        simple_report['dividendes'] = report['extra']['dividendes']
    if parameters['extra']['bénéfices']:
        simple_report['benefices'] = report['extra']['bénéfices']
    if parameters['extra']['peg']:
        simple_report['peg'] = report['extra']['peg']
    return simple_report

def get_report(parameters):
    """
    Returns a report of all metadata from the input ISIN
    """
    report = dict()
    url = common.decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          common.decode_rot('/fgernzvat/pbhef/trgPbhef?') + \
          'code={}&place={}&codif=ISIN'.format(parameters['isin'], parameters['place'])
    req = SESSION.get(url, verify=False)
    report['cours'] = None
    if req.ok:
        report['cours'] = common.clean_data(req.text)

    url = common.decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          common.decode_rot('/fgernzvat/pbhef/oybpf/trgUrnqreSvpur?') + \
          'code={}&place={}&codif=ISIN'.format(parameters['isin'], parameters['place'])
    req = SESSION.get(url, verify=False)
    header_fiche = None
    report['url'] = None
    if req.ok:
        header_fiche = common.clean_data(req.text)
        report['url'] = common.clean_url(header_fiche['headerFiche']['tweetHeaderFiche'])

    report['infos_boursiere'] = dict()
    if report['url'] is not None:
        req = SESSION.get(report['url'])
        if req.ok:
            soup = BeautifulSoup(req.text, 'html.parser')
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

    report['extra'] = dict()
    if parameters['extra']['dividendes']:
        report['extra']['dividendes'] = compute_extra_dividendes(
            parameters, report['infos_boursiere'])

    if parameters['extra']['bénéfices'] or parameters['extra']['peg']:
        report['extra']['bénéfices'] = compute_extra_benefices(report)

    if parameters['extra']['peg']:
        report['extra']['peg'] = compute_extra_peg(
            report['extra']['bénéfices'], report['infos_boursiere'])

    return report
