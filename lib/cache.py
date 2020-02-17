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
from requests import Session
import urllib3

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

def save(url, content):
    """
    Save the content in the cache
    """
    url_hash = get_hash(url)
    if not os.path.exists('cache'):
        os.mkdir('cache')
    with open('cache/{}'.format(url_hash), 'w') as url_file:
        url_file.write(content)

def load(url):
    """
    Returns the url's content from the cache
    """
    url_hash = get_hash(url)
    with open('cache/{}'.format(url_hash), 'r') as url_file:
        content = url_file.read()
    return content

def get(url, verify=True):
    """
    Requests the url is not in cache
    """
    if is_in_cache(url):
        return load(url)
    req = SESSION.get(url, verify=verify, allow_redirects=False)
    if req.ok and req.status_code == 200:
        save(url, req.text)
        return req.text
    return ''
