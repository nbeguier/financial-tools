#!/usr/bin/env python3
"""
Reporting library

Copyright (c) 2020-2022 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Own library
# pylint: disable=E0401
from lib import cache, common

# Debug
# from pdb import set_trace as st

def get_cours(isin, mic, disable_cache=False):
    """
    Returns core info from isin
    """
    url = common.decode_rot('uggcf://yrfrpubfcek.fbyhgvbaf.jrost.pu/zqc-nhgu/yrfrpubf-ncv/') + \
        f'quotes/{isin}-{mic}?keytype=ISIN_MIC&fields=DISPLAY_NAME,EVENT3,ISIN,LISTING_ID,M_CUR,M_PRICINGQUOT:id,M_SYMB,MARKET,MIC,SC_GROUPED,MARKET:id,MARKET:description,SEC:id,SEC:description,SRD,TAXFR_PEA_APP,TAXFR_PEA,12W_AVVOL,HIGH,LOW,LVAL_NORM,MCAP_TK,NC2_PR_NORM,OPEN,CLOSE_ADJ_NORM,VOL,CAPEX_RATIO,TUR,INTEREST,DENOM,MATURITY,EUSIPA:description,ISSUEDATE,EXERRATIO,STRIKE,COMPFULLNAME,1W_PERF_PR,4W_PERF_PR,12W_PERF_PR,26W_PERF_PR,52W_PERF_PR,YTD_PERF_PR,3Y_PERF_PR,5Y_PERF_PR,HILIMIT,LOLIMIT,MM100,MM20,MM50,RESISTANCE_1,RSI14,SUPPORT_1,O_SHS,ANDISTR,YLDEQ,DIVIDEND,PER_1,CA_ANNEE_COURANTE,ANC_PAR_ACTION_ANNEE_PRECEDENTE,BNPA_ANNEE_COURANTE,BNPA_ANNEE_N2,BNPA_ANNEE_PRECEDENTE,CA_ANNEE_N2,CA_ANNEE_PRECEDENTE,CAPI_CA_ANNEE_COURANTE,CAPI_CA_ANNEE_PRECEDENTE,CAPI_CA_ANNEE_SUIVANTE,CONSEIL_CONSENSUS_ACHAT,CONSEIL_CONSENSUS_NEUTRE,CONSEIL_CONSENSUS_VENTE,CROISSANCE_BNPA_ANNEE_COURANTE,CROISSANCE_BNPA_ANNEE_PRECEDENTE,CROISSANCE_BNPA_ANNEE_SUIVANTE,CROISSANCE_BNPA_ANNEEN2,CROISSANCE_BNPA_MOYEN_3_ANS,CROISSANCE_CA_ANNEE_COURANTE,CROISSANCE_CA_ANNEE_PRECEDENTE,CROISSANCE_CA_ANNEE_SUIVANTE,CROISSANCE_CA_MOYEN_3_ANS,CROISSANCE_CA_ANNEEN2,DECOTE_SURCOTE,DIV_ANNEE_COURANTE,DIV_ANNEE_PRECEDENTE,ENDETTEMENT_NET_FP,ENDETTEMENT_NET,FONDS_PROPRES,PER_ANNEE_ESTIMEE,PER_ANNEE_PRECEDENTE,PER_ANNEE_SUIVANTE,RDT_NET_ANNEE_COURANTE,SCAN_NOTE_BNPA,SCAN_NOTE_CA,SCAN_NOTE_GLOBALE,SCAN_NOTE_PERF,SCAN_NOTE_RDT,SCAN_NOTE_SOLIDITE_BILAN,SCAN_RANK_BNPA,SCAN_RANK_CA,SCAN_RANK_GLOBALE,SCAN_RANK_PERF,SCAN_RANK_RDT,SCAN_RANK_SOLIDITE_BILAN,VESUR_CA_ANNEE_COURANTE'
    content = cache.get(url, disable_cache=disable_cache)
    cours = None
    if content:
        cours = common.clean_data(content)['fields']
    return cours

def get_report(parameters):
    """
    Returns a report of all metadata from the input ISIN
    """
    report = get_cours(parameters['isin'], parameters['mic'])

    if report is None:
        return None
    report['CUSTOM_DIVIDEND_PERCENT'] = '-'
    if 'DIVIDEND' in report and 'LVAL_NORM' in report:
        dividend = report['DIVIDEND']['v']
        cur_value = report['LVAL_NORM']['v']
        report['CUSTOM_DIVIDEND_PERCENT'] = '-'
        if cur_value != 0:
            report['CUSTOM_DIVIDEND_PERCENT'] = round(100*dividend/cur_value, 1)

    report['CUSTOM_DIVIDEND_ANNEE_PRECEDENTE_PERCENT'] = '-'
    if 'DIV_ANNEE_PRECEDENTE' in report and 'LVAL_NORM' in report:
        dividend = report['DIV_ANNEE_PRECEDENTE']['v']
        cur_value = report['LVAL_NORM']['v']
        report['CUSTOM_DIVIDEND_ANNEE_PRECEDENTE_PERCENT'] = '-'
        if cur_value != 0:
            report['CUSTOM_DIVIDEND_ANNEE_PRECEDENTE_PERCENT'] = round(100*dividend/cur_value, 1)

    report['CUSTOM_PEG'] = '-'
    if 'CROISSANCE_BNPA_ANNEE_COURANTE' in report and 'PER_ANNEE_ESTIMEE' in report:
        croissance = report['CROISSANCE_BNPA_ANNEE_COURANTE']['v']
        per = report['PER_ANNEE_ESTIMEE']['v']
        report['CUSTOM_PEG'] = 'infini'
        if croissance != 0:
            report['CUSTOM_PEG'] = round(per/croissance, 1)

    report['CUSTOM_PEG_ANNEE_PRECEDENTE'] = '-'
    if 'CROISSANCE_BNPA_ANNEE_PRECEDENTE' in report and 'PER_ANNEE_PRECEDENTE' in report:
        croissance = report['CROISSANCE_BNPA_ANNEE_PRECEDENTE']['v']
        per = report['PER_ANNEE_PRECEDENTE']['v']
        report['CUSTOM_PEG_ANNEE_PRECEDENTE'] = 'infini'
        if croissance != 0:
            report['CUSTOM_PEG_ANNEE_PRECEDENTE'] = round(per/croissance, 1)

    report['CUSTOM_PEG_MAISON'] = '-'
    if '52W_PERF_PR' in report and 'PER_ANNEE_ESTIMEE' in report:
        croissance = report['52W_PERF_PR']['v']
        per = report['PER_ANNEE_ESTIMEE']['v']
        report['CUSTOM_PEG_MAISON'] = 'infini'
        if croissance != 0:
            report['CUSTOM_PEG_MAISON'] = round(per/croissance, 1)

    return report
