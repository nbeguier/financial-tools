#!/usr/bin/env python3
"""
Cache library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
from hashlib import sha512
import os
from random import randint
import time

# Third party library imports
from requests import exceptions, Session
import urllib3

# Own library
# pylint: disable=E0401,E1101
import settings

# Debug
# from pdb import set_trace as st

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SESSION = Session()

# TTL = 60 # 1 minute
TTL = 21600 # 6 hours

def gen_headers():
    """
    Returns random User-Agent
    """
    return {'User-Agent': \
        'Mozilla/5.{a} (Macintosh; Intel Mac OS X 10_15_{a}) '.format(a=randint(1, 100)) +
        'AppleWebKit/537.{} '.format(randint(1, 100)) +
        '(KHTML, like Gecko) Chrome/80.{a}.3987.{a} '.format(a=randint(1, 100)) +
        'Safari/537.{}'.format(randint(1, 100))}

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

def get(url, verify=True, disable_cache=False):
    """
    Requests the url is not in cache
    """
    try:
        enable_cache = settings.ENABLE_CACHE and not disable_cache
    except AttributeError:
        enable_cache = not disable_cache
    if is_in_cache(url) and enable_cache:
        return load(url)
    try:
        req = SESSION.get(url, verify=verify, allow_redirects=False)
    except exceptions.ConnectionError:
        return ''
    if req.ok and req.status_code == 200:
        if enable_cache:
            save(url, req.text)
        return req.text
    return ''
