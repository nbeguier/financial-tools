# Financial tools

## Prerequities

```
pip3 install -r requirements.txt
```

## Usage

### GET ISIN

This command returns a list of probable ISIN matchine the input string.

```
get_isin.py STRING
```

```
$ ./get_isin.py carr
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

### ISIN

This function returns all metadata related to the input ISIN. You could also specify the place, this is 'XPAR' by default.

```
usage: isin.py [-h] [--version] [-i ISIN] [-p PLACE] [-s SEARCH]
               [--extra-dividendes] [--extra-peg] [--extra-profit] [--extras]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i ISIN, --isin ISIN  Code ISIN
  -p PLACE, --place PLACE
                        Code d'identification de marché (=XPAR)
  -s SEARCH, --search SEARCH
                        Recherche l'ISIN le plus probable
  --extra-dividendes    Affiche plus d'informations sur les dividendes
                        (=False)
  --extra-peg           Affiche la valeur théorique du PEG (=False)
  --extra-profit        Affiche la valeur théorique de l'évolution des
                        bénéfices (=False)
  --extras              Affiche toutes les informations supplémentaires
                        (=False)
```

```
$ ./isin.py -i FR0000120172
ISIN: FR0000120172
Nom: CARREFOUR
Secteur: SERVICES AUX CONSOMMATEURS / Détaillants et grossistes - Alimentation
Valorisation: 15.855 EUR
Variation 1 an: 6.05 %
|| Dividendes: 0.46 EUR
|| PER: 13.4 (ration bon)
|| Rendement: 2.90 %
|| Détachement: 20/06/19
|| Prochain rdv: 27/02/20
==============
Les Echos: https://investir.lesechos.fr/cours/action-carrefour,xpar,ca,fr0000120172,isin.html
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120172
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============


$ ./isin.py -i IT0001046553 -p XMIL
ISIN: IT0001046553
Nom: CARRARO
Valorisation: 1.828 EUR
Variation 1 an: -17.66 %
==============
Les Echos: https://investir.lesechos.fr/cours/action-carraro,xmil,carr,it0001046553,isin.html
==============


$ ./isin.py -s carr
ISIN: FR0000120172
Nom: CARREFOUR
Secteur: SERVICES AUX CONSOMMATEURS / Détaillants et grossistes - Alimentation
Valorisation: 15.855 EUR
Variation 1 an: 6.05 %
|| Dividendes: 0.46 EUR
|| PER: 13.4 (ration bon)
|| Rendement: 2.90 %
|| Détachement: 20/06/19
|| Prochain rdv: 27/02/20
==============
Les Echos: https://investir.lesechos.fr/cours/action-carrefour,xpar,ca,fr0000120172,isin.html
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120172
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============


$ ./isin.py --extra-dividendes -i FR0000120172
ISIN: FR0000120172
Nom: CARREFOUR
Secteur: SERVICES AUX CONSOMMATEURS / Détaillants et grossistes - Alimentation
Valorisation: 15.855 EUR
Variation 1 an: 6.05 %
|| Dividendes: 0.46 EUR
|| PER: 13.4 (ration bon)
|| Rendement: 2.90 %
|| Détachement: 20/06/19
|| Prochain rdv: 27/02/20
>> [2018] Rendement: 2.86 %
>> [2018] Valorisation: 16.09 EUR
>> [2019/06/20] Valorisation: 16.8 EUR
>> [2018/06/01] Valorisation: 15.38 EUR
==============
Les Echos: https://investir.lesechos.fr/cours/action-carrefour,xpar,ca,fr0000120172,isin.html
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120172
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============


$ ./isin.py --extras -s "air liquide"
ISIN: FR0000120073
Nom: AIR LIQUIDE
Secteur: MATERIAUX DE BASE / Chimie de base
Valorisation: 138.800 EUR
Variation 1 an: 9.98 %
|| Dividendes: 2.70 EUR
|| PER: 28.5 (bulle spéculative)
|| Rendement: 1.95 %
|| Détachement: 20/05/19
|| Prochain rdv: 24/04/20
>> [2018] Rendement: 2.65 %
>> [2018] Valorisation: 101.73 EUR
>> [2019/05/20] Valorisation: 105.23 EUR
>> [2018/05/02] Valorisation: 98.23 EUR
>> Evolution bénéfices: 7.64 %
>> PEG: 3.7
==============
Les Echos: https://investir.lesechos.fr/cours/action-air-liquide,xpar,ai,fr0000120073,isin.html
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120073
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============
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
$ ./reporter.py diff data/2020_02_11.txt data/2020_02_15.txt
ISIN: FR0000121485
Nom: KERING
Evolution valorisation: +3.11 %
Evolution valorisation: 561.900 -> 579.400
Evolution PER: -1.0
Evolution PER: 23.8 -> 22.8
Evolution PEG: -0.1
Evolution PEG: 2.6 -> 2.5
==============
ISIN: FR0000120073
Nom: AIR LIQUIDE
Evolution valorisation: +0.76 %
Evolution valorisation: 137.750 -> 138.800
Evolution PER: +3.4
Evolution PER: 25.1 -> 28.5
Evolution PEG: +0.4
Evolution PEG: 3.3 -> 3.7
Nouveau rdv: 24/04/20
==============
ISIN: FR0000120628
Nom: AXA
Evolution valorisation: +1.41 %
Evolution valorisation: 25.105 -> 25.460
Evolution PER: +0.3
Evolution PER: 9.5 -> 9.8
Evolution PEG: +0.1
Evolution PEG: 1.5 -> 1.6
Evolution benefices: +0.02 points
Evolution benefices: 6.21 -> 6.23
==============
```

