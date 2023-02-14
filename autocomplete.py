#!/usr/bin/env python3
"""
Autocomplete

Copyright (c) 2020-2023 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import json
import sys

# Third party library imports

# Own library
from lib import common

# Debug
# from pdb import set_trace as st

VERSION = '3.1.0'

def print_autocomplete(input_str):
    """
    Returns a list of result matching the input string
    """
    result = common.autocomplete(input_str)
    print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))

def main():
    """
    Main function
    """
    input_str = sys.argv[1]
    print_autocomplete(input_str)

if __name__ == '__main__':
    main()
