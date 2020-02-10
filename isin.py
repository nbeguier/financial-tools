#!/usr/bin/env python3
"""
ISIN

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from argparse import ArgumentParser
from codecs import getencoder
import json
from random import randint
import re
import sys

# Third party library imports
from bs4 import BeautifulSoup
from requests import Session
import urllib3

# Own library
from get_isin import autocomplete

# Debug
# from pdb import set_trace as st

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERSION = '1.1.1'
SESSION = Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.{a} (Macintosh; Intel Mac OS X 10_15_{a}) '.format(a=randint(1, 100)) +
                  'AppleWebKit/537.{} '.format(randint(1, 100)) +
                  '(KHTML, like Gecko) Chrome/80.{a}.3987.{a} '.format(a=randint(1, 100)) +
                  'Safari/537.{}'.format(randint(1, 100)),
}

def clean_data(raw_data, json_load=True):
    """
    Returns cleaned data
    """
    # Remove html
    cleaned_data = re.sub('<[a-zA-Z0-9\.\\\/\"\'=\ ]+>', '', raw_data)
    cleaned_data = cleaned_data.\
                      replace(';', '').\
                      replace('\\n', '').\
                      replace('\\t', '').\
                      replace('\n', '').\
                      replace('\t', '').\
                      replace('&euro', '').\
                      replace('\xa0', '')
    if json_load:
        cleaned_data = json.loads(cleaned_data)
    return cleaned_data

def clean_url(raw_url):
    """
    Returns a clean URL from garbage
    """
    return 'https' + raw_url.split(' https')[1].split('#')[0]

def decode_rot(encoded_str):
    """
    Returns the ROT-13 of the input string
    """
    enc = getencoder('rot-13')
    return enc(encoded_str)[0]

def extract_infos_boursiere(data):
    """
    Extracts dictionnary from list
    """
    report = dict()
    # keys = ['Dividendes', 'PER', 'Rendement', 'Capitalisation', 'Détachement', 'Prochain rdv']
    keys = ['Dividendes', 'PER', 'Rendement', 'Détachement', 'Prochain rdv']
    splitted_data = clean_data(data.get_text().replace('\n', ' '), json_load=False).split()
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

def get_report(parameters):
    """
    Returns a report of all metadata from the input ISIN
    """
    report = dict()
    url = decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          decode_rot('/fgernzvat/pbhef/trgPbhef?') + \
          'code={}&place={}&codif=ISIN'.format(parameters['isin'], parameters['place'])
    req = SESSION.get(url, verify=False)
    report['cours'] = None
    if req.ok:
        report['cours'] = clean_data(req.text)

    url = decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          decode_rot('/fgernzvat/pbhef/oybpf/trgUrnqreSvpur?') + \
          'code={}&place={}&codif=ISIN'.format(parameters['isin'], parameters['place'])
    req = SESSION.get(url, verify=False)
    header_fiche = None
    report['url'] = None
    if req.ok:
        header_fiche = clean_data(req.text)
        report['url'] = clean_url(header_fiche['headerFiche']['tweetHeaderFiche'])

    if report['url'] is not None:
        req = SESSION.get(report['url'])
        if req.ok:
            soup = BeautifulSoup(req.text, 'html.parser')
            for tab in soup.find_all('table'):
                if 'Dividendes' in tab.get_text():
                    report['infos_boursiere'] = extract_infos_boursiere(tab)
            sector = soup.find('a', id='sectorLink')
            if sector is not None:
                report['sector'] = clean_data(sector.get_text(),
                                              json_load=False)
            sub_sector = soup.find('a', id='subSectorLink')
            if sub_sector is not None:
                report['sub_sector'] = clean_data(sub_sector.get_text(),
                                                  json_load=False)

    report['extra'] = dict()
    if parameters['extra']['dividendes']:
        report['extra']['dividendes'] = dict()
        report['extra']['dividendes']['last_rendement'] = 'Unknown'
        report['extra']['dividendes']['last_val'] = 'Unknown'
        report['extra']['dividendes']['latest_val'] = 'Unknown'
        report['extra']['dividendes']['average_val'] = 'Unknown'
        report['extra']['dividendes']['last_detach'] = 'Unknown'
        report['extra']['dividendes']['latest_detach'] = 'Unknown'
        report['extra']['dividendes']['last_year'] = 'Unknown'
        url = decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg/SQF/uvfgbel.kzy?' +
                         'ragvgl=rpubf&ivrj=NYY&pbqvsvpngvba=VFVA&rkpunatr=KCNE&' +
                         'nqqQnlYnfgCevpr=snyfr&nqwhfgrq=gehr&onfr100=snyfr&' +
                         'frffJvguAbDhbg=snyfr&crevbq=3L&tenahynevgl=&aoFrff=&' +
                         'vafgeGbPzc=haqrsvarq&vaqvpngbeYvfg=&pbzchgrIne=gehr&' +
                         'bhgchg=pfiUvfgb&') + \
              'code={}'.format(parameters['isin'])
        req = SESSION.get(url, verify=False)
        if req.ok and 'infos_boursiere' in report and \
            report['infos_boursiere']['Détachement'] != '-':
            matching_date = report['infos_boursiere']['Détachement'].split('/')
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
                dividendes = float(report['infos_boursiere']['Dividendes'].split()[0])
                average_val = (open_value+latest_open_value)/2
                rendement = 100 * dividendes / average_val
                report['extra']['dividendes']['last_rendement'] = round(rendement, 2)
                report['extra']['dividendes']['last_val'] = round(open_value, 2)
                report['extra']['dividendes']['latest_val'] = round(latest_open_value, 2)
                report['extra']['dividendes']['average_val'] = round(average_val, 2)
                report['extra']['dividendes']['last_detach'] = matching_date
                report['extra']['dividendes']['latest_detach'] = latest_matching_date
                report['extra']['dividendes']['last_year'] = latest_matching_date.split('/')[0]

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
    ARGS = PARSER.parse_args()

    PARAMS = dict()
    PARAMS['isin'] = ARGS.isin
    PARAMS['place'] = ARGS.place
    PARAMS['extra'] = dict()
    PARAMS['extra']['dividendes'] = ARGS.extra_dividendes
    if ARGS.search is not None:
        RESULT = autocomplete(ARGS.search)
        if not RESULT:
            print('No result for this name')
            sys.exit(1)
        else:
            PARAMS['isin'] = RESULT[0]['ISIN']

    main(PARAMS)
