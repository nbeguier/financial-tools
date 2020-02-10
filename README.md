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
               [--extra-dividendes]

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
```

```
$ ./isin.py -i FR0000120172
ISIN: FR0000120172
Nom: CARREFOUR
Secteur: SERVICES AUX CONSOMMATEURS / Détaillants et grossistes - Alimentation
Valorisation: 15,455 EUR
Variation 1 an: 3,38 %
|| Dividendes: 0.46 EUR
|| Rendement: 2.98 %
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
Valorisation: 1,850 EUR
Variation 1 an: -16,67 %
==============
Les Echos: https://investir.lesechos.fr/cours/action-carraro,xmil,carr,it0001046553,isin.html
==============


$ ./isin.py -s carr
ISIN: FR0000120172
Nom: CARREFOUR
Secteur: SERVICES AUX CONSOMMATEURS / Détaillants et grossistes - Alimentation
Valorisation: 15,435 EUR
Variation 1 an: 3,24 %
|| Dividendes: 0.46 EUR
|| Rendement: 2.98 %
|| Détachement: 20/06/19
|| Prochain rdv: 27/02/20
==============
Les Echos: https://investir.lesechos.fr/cours/action-carrefour,xpar,ca,fr0000120172,isin.html
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120172
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6
==============


./isin.py -i FR0000120172 --extra-dividendes
ISIN: FR0000120172
Nom: CARREFOUR
Secteur: SERVICES AUX CONSOMMATEURS / Détaillants et grossistes - Alimentation
Valorisation: 15,455 EUR
Variation 1 an: 3,38 %
|| Dividendes: 0.46 EUR
|| Rendement: 2.98 %
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
```
