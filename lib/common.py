#!/usr/bin/env python3
"""
Common library

Copyright (c) 2020-2023 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from codecs import getencoder
import json
import re

# Own library
# pylint: disable=E0401
from lib import cache

# Debug
# from pdb import set_trace as st

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
    url = decode_rot('uggcf://yrfrpubfcek.fbyhgvbaf.jrost.pu/zqc-nhgu/yrfrpubf-ncv/dhbgrf/_zhygvfrnepu?d') + \
        f'={input_str}&fields=DISPLAY_NAME,ISIN,MARKET,MIC,MARKET:description&size=5'
    content = json.loads(cache.get(url))
    result = []
    if content:
        if not 'categories' in content:
            return result
        full_result = content['categories'][0]['hits']
        for res in full_result:
            sub_result = {}
            sub_result['titre'] = res['fields']['DISPLAY_NAME']['v'].upper()
            sub_result['ISIN'] = res['fields']['ISIN']['v'].upper()
            sub_result['mic'] = res['fields']['MIC']['v'].upper()
            sub_result['pays'] = res['fields']['MARKET']['description'].upper()
            result.append(sub_result)
    return result
