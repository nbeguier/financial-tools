#!/usr/bin/env python3
"""
Common library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from codecs import getencoder
import json
from random import randint
import re

# Third party library imports
from requests import Session

SESSION = Session()

def gen_headers():
    """
    Returns random User-Agent
    """
    return {'User-Agent': \
        'Mozilla/5.{a} (Macintosh; Intel Mac OS X 10_15_{a}) '.format(a=randint(1, 100)) +
        'AppleWebKit/537.{} '.format(randint(1, 100)) +
        '(KHTML, like Gecko) Chrome/80.{a}.3987.{a} '.format(a=randint(1, 100)) +
        'Safari/537.{}'.format(randint(1, 100))}


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
                      replace('&#039', "'").\
                      replace('\xa0', '')
    if json_load:
        cleaned_data = json.loads(cleaned_data)
    return cleaned_data

def decode_rot(encoded_str):
    """
    Returns the ROT-13 of the input string
    """
    enc = getencoder('rot-13')
    return enc(encoded_str)[0]

def autocomplete(input_str):
    """
    Returns a list of probable results
    """
    url = decode_rot('uggcf://vairfgve.yrfrpubf.se') + \
          decode_rot('/nhgbpbzcyrgr/nhgbpbzcyrgr.cuc?') + \
          'input={}'.format(input_str)
    req = SESSION.get(url)
    if req.ok:
        result = list()
        if not 'valeurs' in clean_data(req.text)['results']:
            return result
        full_result = clean_data(req.text)['results']['valeurs']
        for res in full_result:
            sub_result = dict()
            sub_result['titre'] = res['titre']
            for arg in res['url'].split(','):
                if re.search('[a-z][a-z][0-9][0-9]', arg):
                    sub_result['ISIN'] = arg.upper()
                if re.search('x[a-z][a-z][a-z]', arg):
                    sub_result['place'] = arg.upper()
            sub_result['pays'] = res['pays']
            result.append(sub_result)
    return result
