#!/usr/bin/env python3
"""
Analysis library

Copyright (c) 2020-2022 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Debug
# from pdb import set_trace as st

def per_text(per_value):
    """
    Retuns the analysis of the PER value
    """
    if per_value == '-':
        return 'inconnu'
    result = 'croissance annoncée extraordinaire'
    if float(per_value) <= 0:
        result = 'aucune croissance annoncée'
    elif float(per_value) <= 10:
        result = 'croissance annoncée raisonable'
    elif float(per_value) <= 17:
        result = 'croissance annoncée forte'
    elif float(per_value) <= 25:
        result = 'croissance annoncée énorme'
    return result

def peg_text(peg_value):
    """
    Retuns the analysis of the PEG value
    """
    if peg_value == '-':
        return 'inconnu'
    if peg_value == 'infini':
        return 'bulle spéculative'
    result = 'bulle spéculative'
    if float(peg_value) <= 0:
        result = 'action sans bénéfices'
    elif float(peg_value) <= 0.5:
        result = 'action sous-évaluée'
    elif float(peg_value) <= 1:
        result = 'ration bon'
    elif float(peg_value) <= 2.5:
        result = 'action surévaluée'
    elif float(peg_value) <= 3.5:
        result = 'bulle spéculative'
    return result
