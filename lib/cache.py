#!/usr/bin/env python3
"""
Cache library

Copyright (c) 2020-2024 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from base64 import b64decode
from codecs import getencoder
from datetime import datetime
from hashlib import sha512
import json
import os
from pathlib import Path
from random import randint
import re
import time

# Third party library imports
from requests import exceptions, Session
import urllib3

# Own library
# pylint: disable=E0401,E1101
# pylint: disable=fixme,unused-argument
import settings

# Debug
# from pdb import set_trace as st

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SESSION = Session()

# TTL = 60 # 1 minute
TTL = 21600 # 6 hours

def decode_rot(encoded_str):
    """
    Returns the ROT-13 of the input string
    """
    enc = getencoder('rot-13')
    return enc(encoded_str)[0]

def gen_user_agent():
    """
    Returns random User-Agent
    """
    return f'Mozilla/5.{randint(1, 100)} (Macintosh; Intel Mac OS X 10_15_{randint(1, 100)}) ' + \
        f'AppleWebKit/605.1.{randint(1, 100)} ' + \
        f'(KHTML, like Gecko) Version/17.{randint(1, 100)} ' + \
        f'Safari/605.1.{randint(1, 100)}'

def get_token():
    """
    Returns new token
    """
    token_path = Path('/tmp/financial_token.jwt')
    if token_path.exists():
        token = token_path.open('r', encoding='utf-8').read()
        if len(token.split('.')) <= 1:
            print('Error retrieving token... (jwt invalid). Removing token.')
            token_path.unlink()
            return ''
        try:
            if datetime.timestamp(datetime.now()) < json.loads(b64decode(token.split('.')[1]+'=='))['exp']:
                return token
        except:
            print('Error retrieving token... (exp not found). Removing token.')
            token_path.unlink()
            return ''
    content = SESSION.get(
        decode_rot('uggcf://vairfgve.yrfrpubf.se/pbhef/npgvbaf/xrevat-xre-se0000121485-kcne'),
        headers={'User-Agent': gen_user_agent(), 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate'})
    if content.status_code != 200:
        print('Error retrieving token... (page not found)')
        return ''
    result = re.findall('_TOKEN__="[a-zA-Z0-9\.=\-\_]+"', content.text)[0].split('"')
    if len(result) <= 1 or not result[1].startswith('ey'):
        print('Error retrieving token... (token not found)')
        return ''
    token = result[1]
    token_path.open('w', encoding='utf-8').write(token)
    return token

def gen_headers():
    """
    Returns headers
    """
    return {'Authorization': f'Bearer {get_token()}',
        'User-Agent': gen_user_agent()}

HEADERS = gen_headers()

def get_hash(string):
    """
    Returns the hash value of the string
    """
    sha = sha512()
    sha.update(string.encode())
    return sha.hexdigest()

def is_expired(hash_key):
    """
    Returns True if the content in cache is expired
    """
    return int(time.time()) - os.path.getctime('cache/{}'.format(hash_key)) > TTL

def is_in_cache(url):
    """
    Return True is the url is in cache
    """
    url_hash = get_hash(url)
    if not os.path.exists('cache'):
        os.mkdir('cache')
        return False
    if not os.path.exists('cache/{}'.format(url_hash)):
        return False
    if is_expired(url_hash):
        return False
    return True

def purge_cache(cache_path):
    """
    Remove cache is present
    """
    if os.path.exists(cache_path):
        os.remove(cache_path)

def save(url, content):
    """
    Save the content in the cache
    """
    cache_path = 'cache/{}'.format(get_hash(url))
    if not os.path.exists('cache'):
        os.mkdir('cache')
    try:
        with open(cache_path, 'w') as url_file:
            url_file.write(content)
    except UnicodeEncodeError:
        purge_cache(cache_path)

def load(url):
    """
    Returns the url's content from the cache
    """
    cache_path = 'cache/{}'.format(get_hash(url))
    try:
        with open(cache_path, 'r') as url_file:
            content = url_file.read()
    except UnicodeDecodeError:
        purge_cache(cache_path)
        content = get(url, verify=False, disable_cache=True)
    return content

def get(url, verify=True, disable_cache=False, token=''):
    """
    Requests the url is not in cache
    """
    if token:
        HEADERS['Authorization'] = f'Bearer {token}'
    try:
        enable_cache = settings.ENABLE_CACHE and not disable_cache
    except AttributeError:
        enable_cache = not disable_cache
    if is_in_cache(url) and enable_cache:
        return load(url)
    try:
        req = SESSION.get(url, verify=verify, allow_redirects=False, headers=HEADERS)
    except exceptions.ConnectionError:
        return ''
    if req.ok and req.status_code == 200:
        if enable_cache:
            save(url, req.text)
        return req.text
    return ''

def post(url, payload, verify=True, disable_cache=False):
    """
    Requests the url is not in cache
    """
    # TODO: implement cache
    HEADERS.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    try:
        req = SESSION.post(
            url,
            data=payload,
            verify=verify,
            allow_redirects=False,
            headers=HEADERS)
    except exceptions.ConnectionError:
        return ''
    if req.ok and req.status_code == 200:
        return req.text
    return ''
