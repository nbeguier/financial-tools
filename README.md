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
Secteur: Chemicals
Valorisation: 176.7 EUR
Variation 1 an: -3.29 %
|| Dividendes: 3.3 EUR
||           : 1.9 %
|| Croissance BNPA: 5 % -> 6 % -> 7 %
|| Croissance CA: -2 % -> 0 % -> 2 %
|| PER prévisionnel: 26.75 (valorisation très élevée)
|| PEG prévisionnel: 3.63 (valorisation élevée vs croissance)
|| PER / perf. 1 an: -8.12 (performance 1 an négative, ratio non valorisable)
|| Orientation: éviter de renforcer (PER très élevé, PEG élevé, croissance bénéficiaire modérée)
--
|| Dividende Année précédente: 3.7 EUR
||                           : 2.1 %
|| PER Année précédente: 28.72 (valorisation très élevée)
|| PEG Année précédente: 4.78 (valorisation élevée vs croissance)
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
Secteur: Chemicals
Valorisation: 176.7 EUR
Variation 1 an: -3.29 %
|| Dividendes: 3.3 EUR
||           : 1.9 %
|| Croissance BNPA: 5 % -> 6 % -> 7 %
|| Croissance CA: -2 % -> 0 % -> 2 %
|| PER prévisionnel: 26.75 (valorisation très élevée)
|| PEG prévisionnel: 3.63 (valorisation élevée vs croissance)
|| PER / perf. 1 an: -8.12 (performance 1 an négative, ratio non valorisable)
|| Orientation: éviter de renforcer (PER très élevé, PEG élevé, croissance bénéficiaire modérée)
--
|| Dividende Année précédente: 3.7 EUR
||                           : 2.1 %
|| PER Année précédente: 28.72 (valorisation très élevée)
|| PEG Année précédente: 4.78 (valorisation élevée vs croissance)
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
        "mic": "",
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
        "mic": "XNAS",
        "pays": "NASDAQ BASIC, NYSE LISTED ISSUES",
        "titre": "CARRIER"
    },
    {
        "ISIN": "US14448C1045",
        "mic": "XADF",
        "pays": "NYSE-CTA FINRA ALTERNATIVE DISPLAY FACILITY (ADF)",
        "titre": "CARRIER"
    },
    {
        "ISIN": "US14448C1045",
        "mic": "XNIM",
        "pays": "CTA NASDAQ OMX STOCK EXCHANGE",
        "titre": "CARRIER"
    }
]
```

### REPORTER

This function save, display and compare reports of a set of ISIN.

```
$ python reporter.py --help
usage: reporter.py [-h] [--version] {save,load,diff,streak,buy} ...

positional arguments:
  {save,load,diff,streak,buy}
                        commands
    save            Save command
    load            Load command
    diff            Diff command
    streak          Streak command
    buy             Buy command

options:
  -h, --help        show this help message and exit
  --version         show program's version number and exit
```

```
$ python reporter.py save -o data/
# Wait one day...
$ python reporter.py save -o data/


$ python reporter.py load data/2026_05_08.txt
ISIN: FR0000120073
Nom: Air Liquide
Secteur: Chemicals
Valorisation: 176.7 EUR
Variation 1 an: -3.29 %
|| Dividendes: 3.3 EUR
||           : 1.9 %
|| Croissance BNPA: 5 % -> 6 % -> 7 %
|| Croissance CA: -2 % -> 0 % -> 2 %
|| PER prévisionnel: 26.75 (valorisation très élevée)
|| PEG prévisionnel: 3.63 (valorisation élevée vs croissance)
|| PER / perf. 1 an: -8.12 (performance 1 an négative, ratio non valorisable)
|| Orientation: éviter de renforcer (PER très élevé, PEG élevé, croissance bénéficiaire modérée)
--
|| Dividende Année précédente: 3.7 EUR
||                           : 2.1 %
|| PER Année précédente: 28.72 (valorisation très élevée)
|| PEG Année précédente: 4.78 (valorisation élevée vs croissance)
# etc...


$ python reporter.py diff data/2026_04_08.txt data/2026_05_08.txt
==============
Air Liquide (FR0000120073)
Evolution valorisation: -3.67 %
Evolution valorisation: 183.44 -> 176.7 EUR
Evolution PER: +0.7
Evolution PER: 26.049036 -> 26.752854 
==============
# etc...
```

```
$ python reporter.py streak data/ --html
<html><body>
<h3>Air Liquide: 3 days in a row !</h3>
</body></html>
```

```
$ python reporter.py buy data/ --html
<html><body>
<h3>Cie des Alpes: surpondérer (rendement intéressant, PER bas, croissance bénéficiaire attendue)</h3>
</body></html>
```

### DASHBOARD

```
$ python dashboard.py 
Nom                                                                       Cours    Variation  Orientation
----------------------------------------------------------------------  -------  -----------  --------------------------------------
Lyxor PEA Eau (MSCI Water) UCITS ETF FCP                                 24.741    -0.241926  conserver
Cie des Alpes                                                            14.18     -0.421348  renforcer prudemment
Air Liquide                                                             142.32     -1.99697   éviter de renforcer
FDJ                                                                      37.68     -2.35812   surveiller avant achat
Kering                                                                  559.5      -3.40124   surveiller le retournement
Lyxor PEA Asie Pacifique (MSCI AC Asia Pacific Ex Japan) UCITS ETF FCP   16.892    -0.856908  conserver
Carrefour                                                                16.295    -2.22022   conserver
AXA                                                                      28.425    -0.97544   conserver pour rendement
CD Projekt                                                               28.71     -4.01204   conserver
Vinci                                                                   105.08     -0.699301  renforcer prudemment
```

```
$ python dashboard.py --csv
24,741;14,18;142,32;37,68;559,5;16,892;16,295;28,425;28,71;105,08;
```

# License
Licensed under the [MIT License](https://github.com/nbeguier/financial-tools/blob/master/LICENSE).

# Copyright
Copyright 2020-202§ Nicolas Beguier; ([nbeguier](https://beguier.eu/nicolas/) - nicolas_beguier[at]hotmail[dot]com)
