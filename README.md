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
isin.py ISIN [PLACE]
```

```
$ ./isin.py FR0000120172
ISIN: FR0000120172
Nom: CARREFOUR
Secteur: SERVICES AUX CONSOMMATEURS / Détaillants et grossistes - Alimentation
Valorisation: 15,525 EUR
Variation 1 an: 3,85 %
|| Dividendes: 0,46 EUR
|| Rendement: 2,96 %
|| Détachement: 20/06/19
|| Prochain rdv: 27/02/20
Recapitulatif dividendes: https://www.bnains.org/archives/action.php?codeISIN=FR0000120172
Palmares CAC40 dividendes: https://www.boursorama.com/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6


$ ./isin.py IT0001046553 XMIL
ISIN: IT0001046553
Nom: CARRARO
Valorisation: 1,850 EUR
Variation 1 an: -16,67 %
```
