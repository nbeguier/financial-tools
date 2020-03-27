# Financial tools

[![Build Status](https://travis-ci.org/nbeguier/financial-tools.svg?branch=master)](https://travis-ci.org/nbeguier/financial-tools) [![Python 3.4|3.8](https://img.shields.io/badge/python-3.4|3.8-green.svg)](https://www.python.org/) [![License](https://img.shields.io/github/license/nbeguier/financial-tools?color=blue)](https://github.com/nbeguier/financial-tools/blob/master/LICENSE)

Set of financial tools to manipulate ISIN

## Prerequities

```
pip3 install -r requirements.txt

cp settings.py.sample settings.py
```

## Usage


### ISIN

This function returns all metadata related to the input ISIN. You could also specify the place, this is 'XPAR' by default.

```
usage: isin.py [-h] [--version] [--verbose] [-i ISIN] [-n NOM]
               [-m MARKET_ID_CODE] [--no-header] [--no-footer]
               [--dividendes-history] [--per-history] [--peg-history]
               [--is-healthy]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --verbose             Affiche plus d'informations (=False)
  -i ISIN, --isin ISIN  Code ISIN
  -n NOM, --nom NOM     Nom de l'action
  -m MARKET_ID_CODE, --market-id-code MARKET_ID_CODE
                        Code d'identification de marché (=XPAR)
  --no-header           Cache les informations de bases (=False)
  --no-footer           Cache les URLs de fin (=False)
  --dividendes-history  Affiche plus d'informations sur les dividendes
                        (=False)
  --per-history         Affiche la valeur théorique du PER (=False)
  --peg-history         Affiche la valeur théorique du PEG (=False)
  --is-healthy          Affiche l'état de santé de l'action (=False)
```

```
# Affiche les infos de FR0000120073 (AIR LIQUIDE)
$ ./isin.py -i FR0000120073
ISIN: FR0000120073
Nom: AIR LIQUIDE
Secteur: MATERIAUX DE BASE / Chimie de base
Valorisation: 139.250 EUR
Variation 1 an: 10.34 %
|| Dividendes: 2.70 EUR
|| PER: 28.6 (bulle spéculative)
|| PEG: 4.9 (croissance annoncée trop faible)
|| Rendement: 1.94 %
|| Détachement: 20/05/19
|| Prochain rdv: 24/04/20
|| Tendance court terme: 4.0/5
|| Tendance moyen terme: 3.0/5
==============
Les Echos: https://investir.lesechos.fr/cours/action-air-liquide,xpar,ai,fr0000120073,isin.html
Boursorama: https://www.boursorama.com/cours/1rPAI/
Fortuneo: https://bourse.fortuneo.fr/actions/cours-air-liquide-AI-FR0000120073-23
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120073
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============


# Affiche les infos de IT0001046553 (CARRARO), XMIL = Borsa Italiana S.P.A.
$ ./isin.py -i IT0001046553 -m XMIL
ISIN: IT0001046553
Nom: CARRARO
Valorisation: 1.826 EUR
Variation 1 an: -17.75 %
==============
Les Echos: https://investir.lesechos.fr/cours/action-carraro,xmil,carr,it0001046553,isin.html
Boursorama: https://www.boursorama.com/cours/1gCARR/
==============


# Affiche les infos de l'ISIN XPAR le plus proche (AIR LIQUIDE)
$ ./isin.py -n "air liqui"
ISIN: FR0000120073
Nom: AIR LIQUIDE
Secteur: MATERIAUX DE BASE / Chimie de base
Valorisation: 139.250 EUR
Variation 1 an: 10.34 %
|| Dividendes: 2.70 EUR
|| PER: 28.6 (bulle spéculative)
|| PEG: 4.9 (croissance annoncée trop faible)
|| Rendement: 1.94 %
|| Détachement: 20/05/19
|| Tendance court terme: 4.0/5
|| Tendance moyen terme: 3.0/5
==============
Les Echos: https://investir.lesechos.fr/cours/action-air-liquide,xpar,ai,fr0000120073,isin.html
Boursorama: https://www.boursorama.com/cours/1rPAI/
Fortuneo: https://bourse.fortuneo.fr/actions/cours-air-liquide-AI-FR0000120073-23
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120073
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============


# Affiche plus d'informations sur les dividendes d'Air Liquide
$ ./isin.py --dividendes-history -i FR0000120073
ISIN: FR0000120073
Nom: AIR LIQUIDE
Secteur: MATERIAUX DE BASE / Chimie de base
Valorisation: 139.250 EUR
Variation 1 an: 10.34 %
|| Dividendes: 2.70 EUR
|| PER: 28.6 (bulle spéculative)
|| PEG: 4.9 (croissance annoncée trop faible)
|| Rendement: 1.94 %
|| Détachement: 20/05/19
|| Prochain rdv: 24/04/20
|| Tendance court terme: 4.0/5
|| Tendance moyen terme: 3.0/5
[Dividendes History] [2018] Rendement: 2.65 %
[Dividendes History] [2018] Valorisation: 101.73 EUR
[Dividendes History] [2019/05/20] Valorisation: 105.23 EUR
[Dividendes History] [2018/05/02] Valorisation: 98.23 EUR
==============
Les Echos: https://investir.lesechos.fr/cours/action-air-liquide,xpar,ai,fr0000120073,isin.html
Boursorama: https://www.boursorama.com/cours/1rPAI/
Fortuneo: https://bourse.fortuneo.fr/actions/cours-air-liquide-AI-FR0000120073-23
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120073
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============


# Affiche le maximum d'informations sur l'action d'Air Liquide
$ ./isin.py --peg-history --per-history --dividendes-history -n "air liquide"
ISIN: FR0000120073
Nom: AIR LIQUIDE
Secteur: MATERIAUX DE BASE / Chimie de base
Valorisation: 139.250 EUR
Variation 1 an: 10.34 %
|| Dividendes: 2.70 EUR
|| PER: 28.6 (bulle spéculative)
|| PEG: 4.9 (croissance annoncée trop faible)
|| Rendement: 1.94 %
|| Détachement: 20/05/19
|| Prochain rdv: 24/04/20
|| Tendance court terme: 4.0/5
|| Tendance moyen terme: 3.0/5
[Dividendes History] [2018] Rendement: 2.65 %
[Dividendes History] [2018] Valorisation: 101.73 EUR
[Dividendes History] [2019/05/20] Valorisation: 105.23 EUR
[Dividendes History] [2018/05/02] Valorisation: 98.23 EUR
[PER History] [Inconnu] PER 10 (action sous-évaluée): 48.69 EUR
[PER History] [2017/02/09] PER 17 (ration bon): 82.77 EUR
[PER History] [2019/12/11] PER 25 (action surévaluée): 121.72 EUR
[PEG History] [Inconnu] PEG 0.5 (croissance annoncée extrème): 14.21 EUR
[PEG History] [Inconnu] PEG 1 (croissance annoncée forte): 28.42 EUR
[PEG History] [Inconnu] PEG 2 (croissance annoncée ok): 56.84 EUR
[PEG History] [2017/09/08] PEG 3 (croissance annoncée faible): 85.26 EUR
[PEG History] [2019/06/04] PEG 3.6 (croissance annoncée trop faible): 102.31 EUR
==============
Les Echos: https://investir.lesechos.fr/cours/action-air-liquide,xpar,ai,fr0000120073,isin.html
Boursorama: https://www.boursorama.com/cours/1rPAI/
Fortuneo: https://bourse.fortuneo.fr/actions/cours-air-liquide-AI-FR0000120073-23
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120073
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============
```

### GET ISIN

This command returns a list of probable ISIN matchine the input string.

```
autocomplete.py STRING
```

```
$ ./autocomplete.py "carr"
[
    {
        "ISIN": "FR0000120172",
        "pays": "fr",
        "place": "XPAR",
        "titre": "CARREFOUR",
    },
    {
        "ISIN": "US1439051079",
        "pays": "us",
        "place": "XNYS",
        "titre": "CARRIAGE SERVICES INC",
    },
    {
        "ISIN": "US1445771033",
        "pays": "us",
        "place": "XNAS",
        "titre": "CARRIZO OIL & GAS INC",
    },
    {
        "ISIN": "US14574X1046",
        "pays": "us",
        "place": "XNAS",
        "titre": "CARROLS RESTAURANT GROUP INC",
    },
    {
        "ISIN": "IT0001046553",
        "pays": "it",
        "place": "XMIL",
        "titre": "CARRARO",
    }
]

```

### REPORTER

This function save, display and compare reports of a set of ISIN.

```
usage: reporter.py [-h] [--version] {save,load,diff} ...

positional arguments:
  {save,load,diff}  commands
    save            Save command
    load            Load command
    diff            Diff command

optional arguments:
  -h, --help        show this help message and exit
  --version         show program's version number and exit
```

```
$ ./reporter.py diff data/2020_02_23.txt data/2020_02_24.txt
==============
ISIN: FR0000120073
Nom: AIR LIQUIDE
Evolution valorisation: -3.95 %
Evolution valorisation: 139.250 -> 133.750 EUR
Tendance court terme: 3.0/5 -> 4.0/5
Tendance moyen terme: 2.25/5 -> 3.0/5
==============
ISIN: FR0000120628
Nom: AXA
Evolution valorisation: -3.25 %
Evolution valorisation: 24.130 -> 23.345 EUR
Tendance court terme: 2.75/5 -> 2.5/5
Tendance moyen terme: 4.25/5 -> 4.0/5
==============
ISIN: FR0000120172
Nom: CARREFOUR
Evolution valorisation: -2.54 %
Evolution valorisation: 16.130 -> 15.720 EUR
[Reminder] Prochain rdv: 27/02/20
Tendance court terme: 5.0/5
Tendance moyen terme: 2.0/5 -> 3.5/5
==============
ISIN: FR0000053324
Nom: COMPAGNIE DES ALPES (CDA)
Evolution valorisation: -8.95 %
Evolution valorisation: 29.050 -> 26.450 EUR
Tendance court terme: 2.0/5
Tendance moyen terme: 3.5/5
==============
ISIN: FR0013451333
Nom: FDJ
Evolution valorisation: -3.18 %
Evolution valorisation: 30.345 -> 29.380 EUR
Tendance court terme: 3.0/5
Tendance moyen terme: 1.5/5
==============
ISIN: FR0011869312
Nom: LYXOR UCITS ETF PEA MSCI AC ASIA PACIFIC EX JAPAN C-EUR
Evolution valorisation: -3.63 %
Evolution valorisation: 15.941 -> 15.363 EUR
Tendance court terme: -/5
Tendance moyen terme: -/5
==============
ISIN: FR0011882364
Nom: LYXOR UCITS ETF PEA WORLD WATER C-EUR
Evolution valorisation: -3.22 %
Evolution valorisation: 21.094 -> 20.414 EUR
Tendance court terme: -/5
Tendance moyen terme: -/5
==============
ISIN: FR0000121485
Nom: KERING
Evolution valorisation: -4.72 %
Evolution valorisation: 561.600 -> 535.100 EUR
Tendance court terme: 5.0/5
Tendance moyen terme: 5.0/5 -> 4.25/5
==============
```

### DASHBOARD

```
$ ./dashboard.py
Nom          Cours
-----------  -------
KERING       511,700
AIR LIQUIDE  127,800
AXA          21,855
```
