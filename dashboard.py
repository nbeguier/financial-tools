#!/usr/bin/env python3
"""
Dashboard

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import sys

# Third party library imports
from tabulate import tabulate

# Own library
import lib.reporting as reporting
try:
    import settings
except ImportError:
    print('You need to specify a settings.py file.')
    print('$ cp settings.py.sample settings.py')
    sys.exit(1)

# Debug
# from pdb import set_trace as st

VERSION = '1.0.0'

def main():
    """
    Main function
    """
    listing = list()
    for isin in settings.ISIN_DASHBOARD:
        isin_data = reporting.get_cours(isin, 'XPAR', disable_cache=True)
        if not isin_data:
            listing.append(list())
            continue
        listing.append([isin_data['cotation']['name'], isin_data['cotation']['valorisation']])

    print(tabulate(listing, [
        'Nom',
        'Cours']))

if __name__ == '__main__':
    main()
