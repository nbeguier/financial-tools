#!/usr/bin/env python3
"""
Analysis library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

def per_text(per_value):
    """
    Retuns the analysis of the PER value
    """
    result = 'bulle spéculative'
    if float(per_value) <= 0:
        result = 'action sans bénéfices'
    elif float(per_value) <= 10:
        result = 'action sous-évaluée'
    elif float(per_value) <= 17:
        result = 'ration bon'
    elif float(per_value) <= 25:
        result = 'action surévaluée'
    return result

def peg_text(per_value):
    """
    Retuns the analysis of the PEG value
    """
    result = 'croissance annoncée trop faible'
    if float(per_value) <= 0:
        result = 'aucune croissance'
    elif float(per_value) <= 0.5:
        result = 'croissance annoncée extrème'
    elif float(per_value) <= 1.5:
        result = 'croissance annoncée forte'
    elif float(per_value) <= 2.5:
        result = 'croissance annoncée ok'
    elif float(per_value) <= 3.5:
        result = 'croissance annoncée faible'
    return result

def per_by_value(current_per, current_val):
    """
    Returns for each PER stage the share value
    """
    result = dict()
    result[current_per] = dict()
    result[10] = dict()
    result[17] = dict()
    result[25] = dict()
    result[current_per]['value'] = current_val
    result[current_per]['current'] = True
    result[10]['value'] = current_val * 10 / current_per
    result[10]['current'] = False
    result[17]['value'] = current_val * 17 / current_per
    result[17]['current'] = False
    result[25]['value'] = current_val * 25 / current_per
    result[25]['current'] = False
    return result

def peg_by_value(current_peg, current_val):
    """
    Returns for each PEG stage the share value
    """
    result = dict()
    result[current_peg] = dict()
    result[0.5] = dict()
    result[1] = dict()
    result[2] = dict()
    result[3] = dict()
    result[3.6] = dict()
    result[current_peg]['value'] = current_val
    result[current_peg]['current'] = True
    result[0.5]['value'] = 0.5 * current_val / current_peg
    result[0.5]['current'] = False
    result[1]['value'] = 1 * current_val / current_peg
    result[1]['current'] = False
    result[2]['value'] = 2 * current_val / current_peg
    result[2]['current'] = False
    result[3]['value'] = 3 * current_val / current_peg
    result[3]['current'] = False
    result[3.6]['value'] = 3.6 * current_val / current_peg
    result[3.6]['current'] = False
    return result
