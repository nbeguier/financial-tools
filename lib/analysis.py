#!/usr/bin/env python3
"""
Analysis library

Copyright (c) 2020-2023 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Debug
# from pdb import set_trace as st

def _to_float(value):
    """
    Returns value as float, or None if it cannot be interpreted.
    """
    if value in ('-', None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def per_text(per_value):
    """
    Returns the analysis of the PER value
    """
    per = _to_float(per_value)
    if per is None:
        return 'inconnu'
    if per <= 0:
        return 'PER non significatif'
    if per <= 10:
        return 'valorisation basse'
    if per <= 17:
        return 'valorisation modérée'
    if per <= 25:
        return 'valorisation élevée'
    return 'valorisation très élevée'

def peg_text(peg_value):
    """
    Returns the analysis of the PEG value
    """
    peg = _to_float(peg_value)
    if peg_value == 'infini':
        return 'croissance nulle, PEG non significatif'
    if peg is None:
        return 'inconnu'
    if peg == 0:
        return 'PEG non significatif'
    if peg < 0:
        return 'croissance négative, PEG non significatif'
    if peg <= 0.5:
        return 'PEG bas, vérifier la durabilité de la croissance'
    if peg <= 1:
        return 'valorisation raisonnable vs croissance'
    if peg <= 2:
        return 'prime de valorisation vs croissance'
    return 'valorisation élevée vs croissance'

def price_performance_ratio_text(ratio_value):
    """
    Returns the analysis of the PER divided by the 1-year share-price performance.
    """
    ratio = _to_float(ratio_value)
    if ratio_value == 'infini':
        return 'performance 1 an nulle, ratio non significatif'
    if ratio is None:
        return 'inconnu'
    if ratio < 0:
        return 'performance 1 an négative, ratio non valorisable'
    return 'indicateur maison, à comparer dans le temps'
