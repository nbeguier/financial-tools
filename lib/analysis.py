#!/usr/bin/env python3
"""
Analysis library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

def per(per_value):
    """
    Retuns the analysis of the PER value
    """
    result = 'bulle spéculative'
    if float(per_value) <= 10:
        result = 'action sous-évaluée'
    elif float(per_value) <= 17:
        result = 'ration bon'
    elif float(per_value) <= 25:
        result = 'action surévaluée'
    return result
