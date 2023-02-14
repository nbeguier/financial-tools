#!/usr/bin/env python3
"""
Analysis library

Copyright (c) 2020-2023 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Debug
# from pdb import set_trace as st

def compute_per(report):
    """
    Returns an average PER
    PER = Capitalisation boursiere / Resultat net
    ou
    PER = Prix d'un action / BNA
    """
    count = 0
    value_1 = 0
    if 'PER_ANNEE_ESTIMEE' in report:
        value_1 = report['PER_ANNEE_ESTIMEE']['v']
        count += 1
    value_2 = 0
    if 'listeAnnee' in report['EXTRA_DATA'] and len(report['EXTRA_DATA']['listeAnnee']) > 0 and 'per' in report['EXTRA_DATA']['listeAnnee'][0]:
        value_2 = report['EXTRA_DATA']['listeAnnee'][0]['per']
        count += 1
    value_3 = 0
    if 'LVAL_NORM' in report and 'BNPA_ANNEE_COURANTE' in report and report['BNPA_ANNEE_COURANTE']['v'] != 0:
        value_3 = report['LVAL_NORM']['v'] / report['BNPA_ANNEE_COURANTE']['v']
        count += 1
    if count == 0:
        return '-'
    return round((value_1 + value_2 + value_3) / count, 2)

def compute_peg(report):
    """
    Returns the PEG
    PEG = PER / taux de croissance du BNA (en %)
    """
    value_1 = '-'
    if 'CROISSANCE_BNPA_ANNEE_COURANTE' in report:
        croissance = report['CROISSANCE_BNPA_ANNEE_COURANTE']['v']
        if croissance == 0:
            value_1 = 0
        else:
            value_1 = round(report['CUSTOM_PER'] / croissance, 2)
    return value_1

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
