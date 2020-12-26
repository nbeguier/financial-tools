#!/usr/bin/env python3
"""
Common library

Copyright (c) 2020-2021 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from codecs import getencoder
import json
import re

# Own library
# pylint: disable=E0401
import lib.cache as cache

# Debug
# from pdb import set_trace as st

def clean_url(raw_url):
    """
    Returns a clean URL from garbage
    """
    return 'https' + raw_url.split(' https')[1].split('#')[0]

def clean_data(raw_data, json_load=True):
    """
    Returns cleaned data
    """
    # Remove html
    # pylint: disable=W1401
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
    content = cache.get(url)
    if content:
        result = list()
        if not 'valeurs' in clean_data(content)['results']:
            return result
        full_result = clean_data(content)['results']['valeurs']
        for res in full_result:
            sub_result = dict()
            sub_result['titre'] = res['titre']
            for arg in res['url'].split(','):
                if re.search('[a-z][a-z][0-9][0-9]', arg):
                    sub_result['ISIN'] = arg.upper()
                if re.search('x[a-z][a-z][a-z]', arg):
                    sub_result['mic'] = arg.upper()
            sub_result['pays'] = res['pays']
            result.append(sub_result)
    return result
