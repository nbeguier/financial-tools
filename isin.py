#!/usr/bin/env python3
"""
ISIN

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from codecs import getencoder
import json
from random import randint
import sys

# Third party library imports
from bs4 import BeautifulSoup
from requests import Session
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Debug
# from pdb import set_trace as st

VERSION = '1.0.0'
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
    cleaned_data = raw_data.\
                      replace(';', '').\
                      replace('\\n', '').\
                      replace('\\t', '').\
                      replace('\n', '').\
                      replace('\t', '').\
                      replace('&euro', '').\
                      replace('<strong>', '').\
                      replace('<strong class=\\"vert\\">', '').\
                      replace('<strong class=\\"rouge\\">', '').\
                      replace('<\\/strong>', '').\
                      replace('<span class=\\"vert\\">', '').\
                      replace('<span class=\\"rouge\\">', '').\
                      replace('<\\/span>', '').\
                      replace('<div class=\\"vert\\">', '').\
                      replace('<div class=\\"rouge\\">', '').\
                      replace('<\\/div>', '').\
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
    keys = ['Dividendes', 'Rendement', 'Détachement', 'Prochain rdv']
    splitted_data = clean_data(data.get_text().replace('\n', ' '), json_load=False).split()
    for i, key in enumerate(splitted_data):
        if key == 'Dividendes' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = '{} EUR'.format(splitted_data[i+1])
        elif key == 'Rendement' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = '{} %'.format(splitted_data[i+1])
        elif key == 'Rendement' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = '{} %'.format(splitted_data[i+1])
        elif key == 'Détachement' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report[key] = splitted_data[i+1]
        elif key == 'rdv' and i < len(splitted_data) and splitted_data[i+1] not in keys:
            report['Prochain rdv'] = splitted_data[i+1]
    return report

def get_report(isin, place):
    """
    Returns a report of all metadata from the input ISIN
    """
    report = dict()
    url = decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          decode_rot('/fgernzvat/pbhef/trgPbhef?') + \
          'code={}&place={}&codif=ISIN'.format(isin, place)
    req = SESSION.get(url, verify=False)
    report['cours'] = None
    if req.ok:
        report['cours'] = clean_data(req.text)

    url = decode_rot('uggcf://yrfrpubf-obhefr-sb-pqa.jyo.nj.ngbf.arg') + \
          decode_rot('/fgernzvat/pbhef/oybpf/trgUrnqreSvpur?') + \
          'code={}&place={}&codif=ISIN'.format(isin, place)
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
    return report

def print_report(place, report):
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
    if place == 'XPAR':
        print('Recapitulatif dividendes: https://www.bnains.org' +
              '/archives/action.php?' +
              'codeISIN={}'.format(report['isin']))
        print('Palmares CAC40 dividendes: https://www.boursorama.com' +
              '/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6')

def main():
    """
    Main function
    """
    isin = sys.argv[1]
    place = 'XPAR'
    if len(sys.argv) == 3:
        place = sys.argv[2]
    report = get_report(isin, place)
    report['isin'] = isin
    print_report(place, report)

if __name__ == '__main__':
    main()
