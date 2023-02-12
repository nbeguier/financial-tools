# Financial tools

[![Build Status](https://travis-ci.com/nbeguier/financial-tools.svg?branch=master)](https://travis-ci.com/nbeguier/financial-tools) [![Python 3.5|3.9](https://img.shields.io/badge/python-3.5|3.9-green.svg)](https://www.python.org/) [![License](https://img.shields.io/github/license/nbeguier/financial-tools?color=blue)](https://github.com/nbeguier/financial-tools/blob/master/LICENSE)

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
$ python isin.py --help
usage: isin.py [-h] [--version] [-i ISIN] [-n NOM] [-m MARKET_ID_CODE] [--no-header]

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i ISIN, --isin ISIN  Code ISIN
  -n NOM, --nom NOM     Nom de l'action
  -m MARKET_ID_CODE, --market-id-code MARKET_ID_CODE
                        Code d'identification de marché (=XPAR)
  --no-header           Cache les informations de bases (=False)
```

```
# Affiche les infos de FR0000120073 (AIR LIQUIDE)
$ python isin.py -i FR0000120073
ISIN: FR0000120073
Nom: Air Liquide
Secteur: Chimie
Valorisation: 142.32 EUR
Variation 1 an: 8.96 %
|| Dividendes: 2.9 EUR
||           : 2.0 %
|| Croissance BNPA: 0 % -> 10 % -> 18 %
|| Croissance CA: -7 % -> 14 % -> 28 %
|| PER prévisionel: 24.99 (croissance annoncée énorme)
|| PEG prévisionel: 1.4 (action surévaluée)
|| PEG réaliste: 2.8 (bulle spéculative)
--
|| Dividende Année précédente: 2.9 EUR
||                           : 2.0 %
|| PER Année précédente: 29.36 (croissance annoncée extraordinaire)
|| PEG Année précédente: 3.0 (bulle spéculative)
==============

# Affiche les infos de XS2215041513 (3.75 Carraro26Nts-S), HMTF
$ python isin.py -i XS2215041513 -m HMTF
ISIN: XS2215041513
Nom: 3.75 Carraro26Nts-S
Secteur: Financial, investment & other diversified comp.
Valorisation: 98.88 EUR
Variation 1 an: -1.53 %
--
==============


# Affiche les infos de l'ISIN XPAR le plus proche (AIR LIQUIDE)
$ python isin.py -n "air liqui"
ISIN: FR0000120073
Nom: Air Liquide
Secteur: Chimie
Valorisation: 142.32 EUR
Variation 1 an: 8.96 %
|| Dividendes: 2.9 EUR
||           : 2.0 %
|| Croissance BNPA: 0 % -> 10 % -> 18 %
|| Croissance CA: -7 % -> 14 % -> 28 %
|| PER prévisionel: 24.99 (croissance annoncée énorme)
|| PEG prévisionel: 1.4 (action surévaluée)
|| PEG réaliste: 2.8 (bulle spéculative)
--
|| Dividende Année précédente: 2.9 EUR
||                           : 2.0 %
|| PER Année précédente: 29.36 (croissance annoncée extraordinaire)
|| PEG Année précédente: 3.0 (bulle spéculative)
==============
```

### GET ISIN

This command returns a list of probable ISIN matchine the input string.

```
$ python autocomplete.py <STRING>
```

```
$ python autocomplete.py "carr"
[
    {
        "ISIN": "US14448C1045",
        "mic": "XNYS",
        "pays": "NYSE US COMPOSITE",
        "titre": "CARRIER"
    },
    {
        "ISIN": "US14448C1045",
        "mic": "XNYS",
        "pays": "NEW YORK STOCK EXCHANGE, INC",
        "titre": "CARRIER"
    },
    {
        "ISIN": "US14448C1045",
        "mic": "XADF",
        "pays": "NYSE-CTA FINRA ALTERNATIVE DISPLAY FACILITY (ADF)",
        "titre": "CARRIER"
    },
    {
        "ISIN": "FR0000120172",
        "mic": "XPAR",
        "pays": "EURONEXT - EURONEXT PARIS",
        "titre": "CARREFOUR"
    },
    {
        "ISIN": "US14448C1045",
        "mic": "XNAS",
        "pays": "CTA NASDAQ OMX STOCK EXCHANGE",
        "titre": "CARRIER"
    }
]

```

### REPORTER

This function save, display and compare reports of a set of ISIN.

```
$ python reporter.py --help
usage: reporter.py [-h] [--version] {save,load,diff} ...

positional arguments:
  {save,load,diff}  commands
    save            Save command
    load            Load command
    diff            Diff command

options:
  -h, --help        show this help message and exit
  --version         show program's version number and exit
```

```
$ python reporter.py save -o data/
# Wait one day...
$ python reporter.py save -o data/


$ python reporter.py load data/2023_02_12.txt
ISIN: FR0000121485
Nom: Kering
Secteur: Commerce de détail, grands magasins
Valorisation: 559.5 EUR
Variation 1 an: -9.73 %
|| Dividendes: 4.5 EUR
||           : 0.8 %
|| Croissance BNPA: -38 % -> 62 % -> 23 %
|| Croissance CA: -18 % -> 35 % -> 16 %
|| PER prévisionel: 19.05 (croissance annoncée énorme)
--
|| Dividende Année précédente: 12.0 EUR
|| PER Année précédente: 23.5 (croissance annoncée énorme)
==============
# etc...


$ python reporter.py diff data/2020_02_23.txt data/2020_02_24.txt
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
$ python dashboard.py 
Nom                                                                       Cours    Variation
----------------------------------------------------------------------  -------  -----------
Lyxor PEA Eau (MSCI Water) UCITS ETF FCP                                 24.741    -0.241926
Cie des Alpes                                                            14.18     -0.421348
Air Liquide                                                             142.32     -1.99697
FDJ                                                                      37.68     -2.35812
Kering                                                                  559.5      -3.40124
Lyxor PEA Asie Pacifique (MSCI AC Asia Pacific Ex Japan) UCITS ETF FCP   16.892    -0.856908
Carrefour                                                                16.295    -2.22022
AXA                                                                      28.425    -0.97544
CD Projekt                                                               28.71     -4.01204
Vinci                                                                   105.08     -0.699301
```

# License
Licensed under the [MIT License](https://github.com/nbeguier/financial-tools/blob/master/LICENSE).

# Copyright
Copyright 2020-2023 Nicolas Beguier; ([nbeguier](https://beguier.eu/nicolas/) - nicolas_beguier[at]hotmail[dot]com)
