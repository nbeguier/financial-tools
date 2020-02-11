#!/usr/bin/env python3
"""
ISIN

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
import re
import sys

# Third party library imports
from bs4 import BeautifulSoup
from requests import Session
import urllib3

# Own library
import common

# Debug
# from pdb import set_trace as st

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERSION = '1.2.1'
SESSION = Session()
HEADERS = common.gen_headers()

def clean_url(raw_url):
    """
    Returns a clean URL from garbage
    """
    return 'https' + raw_url.split(' https')[1].split('#')[0]

def extract_infos_boursiere(data):
    """
    Extracts dictionnary from list
    """
    report = dict()
    # keys = ['Dividendes', 'PER', 'Rendement', 'Capitalisation', 'Détachement', 'Prochain rdv']
    keys = ['Dividendes', 'PER', 'Rendement', 'Détachement', 'Prochain rdv']
    splitted_data = common.clean_data(data.get_text().replace('\n', ' '), json_load=False).split()
    for i, key in enumerate(splitted_data):
        if key == 'Dividendes' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = '{} EUR'.format(splitted_data[i+1].replace(',', '.'))
        elif key == 'PER' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = '{}'.format(splitted_data[i+1].replace(',', '.'))
            if float(report[key]) <= 10:
                report[key] += ' (action sous-évaluée)'
            elif float(report[key]) <= 17:
                report[key] += ' (ration bon)'
            elif float(report[key]) <= 25:
                report[key] += ' (action surévaluée)'
            else:
                report[key] += ' (bulle spéculative)'
        elif key == 'Rendement' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = '{} %'.format(splitted_data[i+1].replace(',', '.'))
        elif key == 'Détachement' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = splitted_data[i+1]
        elif key == 'rdv' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report['Prochain rdv'] = splitted_data[i+1]
    return report

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
    if profit == 0:
        return 0
    return round(per/profit, 1)

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
        report['url'] = clean_url(header_fiche['headerFiche']['tweetHeaderFiche'])

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

def print_report(parameters, report):
    """
    Prints the report
    """
    print('ISIN: {}'.format(report['isin']))
    if report['cours'] is not None:
        print('Nom: {}'.format(report['cours']['cotation']['name']))
    if 'sector' in report and 'sub_sector' in report:
        print('Secteur: {} / {}'.format(report['sector'], report['sub_sector']))
    if report['cours'] is not None:
        print('Valorisation: {}EUR'.format(report['cours']['cotation']['valorisation']))
        print('Variation 1 an: {} %'.format(report['cours']['cotation']['variationYear']))
    if 'infos_boursiere' in report:
        for info in report['infos_boursiere']:
            print('|| {}: {}'.format(info, report['infos_boursiere'][info]))
    if parameters['extra']['dividendes']:
        print('>> [{}] Rendement: {} %'.format(
            report['extra']['dividendes']['last_year'],
            report['extra']['dividendes']['last_rendement']))
        print('>> [{}] Valorisation: {} EUR'.format(
            report['extra']['dividendes']['last_year'],
            report['extra']['dividendes']['average_val']))
        print('>> [{}] Valorisation: {} EUR'.format(
            report['extra']['dividendes']['last_detach'],
            report['extra']['dividendes']['last_val']))
        print('>> [{}] Valorisation: {} EUR'.format(
            report['extra']['dividendes']['latest_detach'],
            report['extra']['dividendes']['latest_val']))
    if parameters['extra']['bénéfices']:
        print('>> Evolution bénéfices: {} %'.format(report['extra']['bénéfices']))
    if parameters['extra']['peg']:
        print('>> PEG: {}'.format(report['extra']['peg']))
    print('==============')
    if report['url'] is not None:
        print('Les Echos: {}'.format(report['url']))
    if parameters['place'] == 'XPAR':
        print('Recapitulatif dividendes: https://www.bnains.org' +
              '/archives/action.php?' +
              'codeISIN={}'.format(report['isin']))
        print('Palmares CAC40 dividendes: https://www.boursorama.com' +
              '/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6')
    print('==============')

def main(parameters):
    """
    Main function
    """
    report = get_report(parameters)
    report['isin'] = parameters['isin']
    print_report(parameters, report)

if __name__ == '__main__':
    PARSER = ArgumentParser()

    PARSER.add_argument('--version', action='version', version=VERSION)
    PARSER.add_argument('-i', '--isin', action='store',\
        help='Code ISIN')
    PARSER.add_argument('-p', '--place', action='store',\
        help="Code d'identification de marché (=XPAR)", default='XPAR')
    PARSER.add_argument('-s', '--search', action='store',\
        help="Recherche l'ISIN le plus probable")
    PARSER.add_argument('--extra-dividendes', action='store_true',\
        help="Affiche plus d'informations sur les dividendes (=False)", default=False)
    PARSER.add_argument('--extra-peg', action='store_true',\
        help="Affiche la valeur théorique du PEG (=False)", default=False)
    PARSER.add_argument('--extra-profit', action='store_true',\
        help="Affiche la valeur théorique de l'évolution des bénéfices (=False)", default=False)
    PARSER.add_argument('--extras', action='store_true',\
        help="Affiche toutes les informations supplémentaires (=False)", default=False)
    ARGS = PARSER.parse_args()

    PARAMS = dict()
    PARAMS['isin'] = ARGS.isin
    PARAMS['place'] = ARGS.place
    PARAMS['extra'] = dict()
    PARAMS['extra']['dividendes'] = ARGS.extra_dividendes or ARGS.extras
    PARAMS['extra']['bénéfices'] = ARGS.extra_profit or ARGS.extra_peg or ARGS.extras
    PARAMS['extra']['peg'] = ARGS.extra_peg or ARGS.extras
    if not ARGS.isin and not ARGS.search:
        PARSER.print_help()
        sys.exit(1)
    elif ARGS.search is not None:
        RESULT = common.autocomplete(ARGS.search)
        if not RESULT:
            print('No result for this name')
            sys.exit(1)
        else:
            PARAMS['isin'] = RESULT[0]['ISIN']

    main(PARAMS)
