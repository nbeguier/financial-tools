#!/usr/bin/env python3
"""
Dashboard

Copyright (c) 2020-2023 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import sys

# Third party library imports
from tabulate import tabulate

# Own library
from lib import reporting
try:
    import settings
except ImportError:
    print('You need to specify a settings.py file.')
    print('$ cp settings.py.sample settings.py')
    sys.exit(1)

# Debug
# from pdb import set_trace as st

VERSION = '3.1.0'

def main():
    """
    Main function
    """
    listing = []
    for isin in settings.ISIN_DASHBOARD:
        market = 'XPAR'
        if ',' in isin:
            market = isin.split(',')[1]
            isin = isin.split(',', maxsplit=1)[0]
        isin_data = reporting.get_cours(isin, market, disable_cache=True)
        if not isin_data:
            listing.append([])
            continue
        listing.append([
            isin_data['DISPLAY_NAME']['v'],
            isin_data['LVAL_NORM']['v'],
            isin_data['NC2_PR_NORM']['v'],
        ])
    print(tabulate(listing, [
        'Nom',
        'Cours',
        'Variation',
    ]))

if __name__ == '__main__':
    main()
