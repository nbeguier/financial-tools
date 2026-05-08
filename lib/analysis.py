#!/usr/bin/env python3
"""
Analysis library

Copyright (c) 2020-2026 Nicolas Beguier
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

def _report_float(report, key):
    """
    Returns a numeric report field value, or None when missing.
    """
    field = report.get(key)
    if not isinstance(field, dict):
        return None
    return _to_float(field.get('v'))

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

def _percent_text(value):
    """
    Formats a percent value for compact display.
    """
    if value is None:
        return None
    return f'{round(value, 1)} %'

def recent_momentum(report):
    """
    Returns a recent momentum signal from short-term price action and RSI.
    """
    perf_4w = _report_float(report, '4W_PERF_PR')
    perf_12w = _report_float(report, '12W_PERF_PR')
    rsi = _report_float(report, 'RSI14')
    price = _report_float(report, 'LVAL_NORM')
    mm50 = _report_float(report, 'MM50')

    details = []

    if perf_4w is not None:
        details.append(f'{_percent_text(perf_4w)} sur 4 sem.')
    if perf_12w is not None:
        details.append(f'{_percent_text(perf_12w)} sur 12 sem.')
    if rsi is not None:
        details.append(f'RSI {round(rsi)}')
    if price is not None and mm50 is not None:
        if price < mm50:
            details.append('sous MM50')
        elif price > mm50:
            details.append('au-dessus MM50')

    if not details:
        return {
            'level': 'inconnu',
            'text': 'inconnu',
        }

    if perf_4w is not None and perf_4w <= -8:
        level = 'très négatif'
    elif perf_12w is not None and perf_12w <= -12:
        level = 'très négatif'
    elif rsi is not None and rsi < 30:
        level = 'très négatif'
    elif perf_4w is not None and perf_4w < -3:
        level = 'négatif'
    elif perf_12w is not None and perf_12w < -5:
        level = 'négatif'
    elif rsi is not None and rsi < 40:
        level = 'négatif'
    elif price is not None and mm50 is not None and price < mm50:
        level = 'négatif'
    elif perf_4w is not None and perf_12w is not None and perf_4w > 0 and perf_12w > 0:
        if price is None or mm50 is None or price > mm50:
            level = 'positif'
        else:
            level = 'neutre'
    else:
        level = 'neutre'

    return {
        'level': level,
        'text': f'{level} ({", ".join(details[:3])})' if details else level,
    }

def global_text(report):
    """
    Returns a portfolio orientation from the available financial signals.
    """
    per = _report_float(report, 'PER_ANNEE_ESTIMEE')
    dividend = _to_float(report.get('CUSTOM_DIVIDEND_PERCENT'))
    peg = _to_float(report.get('CUSTOM_PEG'))
    perf = _report_float(report, '52W_PERF_PR')
    bnpa_growth = _report_float(report, 'CROISSANCE_BNPA_ANNEE_COURANTE')
    bnpa_previous = _report_float(report, 'CROISSANCE_BNPA_ANNEE_PRECEDENTE')
    revenue_growth = _report_float(report, 'CROISSANCE_CA_ANNEE_COURANTE')
    momentum = recent_momentum(report)
    momentum_level = momentum['level']

    positives = []
    warnings = []
    score = 0

    if dividend is not None:
        if dividend >= 8:
            score += 1
            positives.append('rendement très élevé')
            warnings.append('vérifier la soutenabilité du dividende')
        elif dividend >= 4:
            score += 1
            positives.append('rendement intéressant')

    if per is not None:
        if per <= 0:
            score -= 1
            warnings.append('PER non significatif')
        elif per <= 10:
            score += 2
            positives.append('PER bas')
        elif per <= 17:
            score += 1
            positives.append('valorisation raisonnable')
        elif per > 25:
            score -= 2
            warnings.append('PER très élevé')
        elif per > 20:
            score -= 1
            warnings.append('valorisation élevée')

    if bnpa_growth is not None:
        if bnpa_growth < 0:
            score -= 2
            warnings.append('bénéfices attendus en baisse')
        elif bnpa_growth > 100:
            warnings.append('rebond de bénéfices atypique')
        elif bnpa_growth >= 10:
            score += 2
            positives.append('croissance bénéficiaire attendue')
        elif bnpa_growth >= 3:
            score += 1
            positives.append('croissance bénéficiaire modérée')

    if bnpa_previous is not None and bnpa_previous < -30 and bnpa_growth is not None and bnpa_growth > 0:
        warnings.append('rebond après forte baisse')

    if revenue_growth is not None:
        if revenue_growth < 0:
            score -= 1
            warnings.append('chiffre d’affaires attendu en baisse')
        elif revenue_growth <= 2:
            warnings.append('croissance du chiffre d’affaires faible')
        elif revenue_growth >= 5:
            score += 1
            positives.append('croissance du chiffre d’affaires')

    if peg is not None:
        if peg < 0:
            score -= 1
            warnings.append('PEG non significatif')
        elif peg > 2:
            score -= 1
            warnings.append('PEG élevé')
        elif 0 < peg <= 1.2:
            score += 1
            positives.append('PEG raisonnable')

    if perf is not None:
        if perf <= -20:
            score -= 1
            warnings.append('cours en forte baisse sur 1 an')
        elif perf < -5:
            score -= 1
            warnings.append('momentum négatif')
        elif perf >= 30:
            score += 1
            positives.append('fort rebond du cours')

    if momentum_level == 'très négatif':
        warnings.append('momentum récent très négatif')
    elif momentum_level == 'négatif':
        warnings.append('momentum récent négatif')
    elif momentum_level == 'positif':
        positives.append('momentum récent positif')

    if dividend is not None and dividend >= 8 and perf is not None and perf <= -20:
        orientation = 'surveiller avant achat'
    elif dividend is not None and dividend >= 4 and bnpa_growth is not None and bnpa_growth < 0:
        orientation = 'conserver pour rendement'
    elif bnpa_growth is not None and bnpa_growth > 100:
        orientation = 'surveiller le retournement'
    elif per is not None and per > 25 and (peg is None or peg > 2):
        orientation = 'éviter de renforcer'
    elif score >= 4 and momentum_level in ('négatif', 'très négatif'):
        orientation = 'surpondérer prudemment'
    elif score >= 4 and not warnings:
        orientation = 'surpondérer'
    elif score >= 2:
        orientation = 'renforcer prudemment'
    elif score >= 0:
        orientation = 'conserver'
    elif score <= -2:
        orientation = 'alléger ou éviter'
    else:
        orientation = 'surveiller'

    reasons = []
    for reason in warnings + positives:
        if reason not in reasons:
            reasons.append(reason)
    if not reasons:
        return orientation
    return f'{orientation} ({", ".join(reasons[:3])})'
