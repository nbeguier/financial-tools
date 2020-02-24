#!/usr/bin/env python3
"""
Analysis library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Debug
# from pdb import set_trace as st

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

def peg_text(peg_value):
    """
    Retuns the analysis of the PEG value
    """
    if peg_value is None:
        return 'inconnu'
    result = 'croissance annoncée trop faible'
    if float(peg_value) <= 0:
        result = 'aucune croissance'
    elif float(peg_value) <= 0.5:
        result = 'croissance annoncée extrème'
    elif float(peg_value) <= 1.5:
        result = 'croissance annoncée forte'
    elif float(peg_value) <= 2.5:
        result = 'croissance annoncée ok'
    elif float(peg_value) <= 3.5:
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

def trend(simple_report):
    """
    Returns the trend score on 5pts
        - 3pts : average of trend
        - 2pts : average of potential
    """
    report = dict()
    report['short term'] = 0
    report['mid term'] = 0
    mapping = {
        'Hausse': 1,
        'Neutre': 0.5,
        'Baisse': 0,
        None: 0,
    }
    count_st_trend = 0
    count_mt_trend = 0
    for market in simple_report['trend']:
        if simple_report['trend'][market]['short term']:
            count_st_trend += 1
        if simple_report['trend'][market]['mid term']:
            count_mt_trend += 1
        report['short term'] += mapping[simple_report['trend'][market]['short term']]
        report['mid term'] += mapping[simple_report['trend'][market]['mid term']]
    if count_st_trend == 0 or count_mt_trend == 0:
        return {'short term': '-', 'mid term': '-'}
    report['short term'] = 3 * report['short term'] / count_st_trend
    report['mid term'] = 3 * report['mid term'] /count_mt_trend
    potential_value = 0
    potential_count = 0
    for market in simple_report['potential']:
        if simple_report['potential'][market]['value'] is not None:
            potential_count += 1
        if simple_report['potential'][market]['percentage'] > 1:
            potential_value += 1
        elif simple_report['potential'][market]['percentage'] > -1:
            potential_value += 0.5
    if potential_count == 0:
        report['short term'] = report['short term'] * 5/3
        report['mid term'] = report['mid term'] * 5/3
    else:
        report['short term'] += 2 * potential_value / potential_count
        report['mid term'] += 2 * potential_value / potential_count
    return report
