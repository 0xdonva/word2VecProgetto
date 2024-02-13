# word2VecProgetto
####  Sommario
- [ Riepilogo ](#riepilogo)
- [ Avvio ](#avvio)
  - [ Esecuzione standard ](#esecuzione-standard)
  - [ Esecuzione avanzata ](#esecuzione-avanzata)
  - [ Esecuzione benchmark ](#esecuzione-benchmark)
- [ Spiegazione benchmark ](#spiegazione-benchmark)

## Riepilogo
Questo progetto indicizza 250 film presenti sul sito [ IMDb ](https://www.imdb.com/).
Esistono due tipi di ricerca:
* **Normale**: è un motore di ricerca full-text sul titolo o la descrizione o entrambe. Si possono utilizzare anche le regex, operatori insiemistici e i campi per effettuare ricerche più mirate.
* **Avanzato**: è un motore di ricerca che utilizza un modello vettoriale di parole inglesi per ricercare le parole e quelle simili.

## Avvio
Per far funzionare il motore di ricerca si devono eseguire dei passaggi preliminari.
Innanzitutto bisogna utilizzare un ambiente virtuale:
```bash
$ pipenv shell
$ pipenv install
```
Successivamente bisogna scaricare il database di film:
```bash
$ python main.py download
```
In questo caso verranno salvati i dati di 250 film e il tempo medio registrato è di una ventina di minuti.

### Esecuzione standard
Una volta eseguiti i passaggi precedenti, per eseguire il motore di ricerca in versione standard basta digitare:
```bash
$ python main.py
```

### Esecuzione avanzata
Una volta eseguiti i passaggi precedenti, per eseguire il motore di ricerca in versione standard basta digitare:
```bash
$ python main.py advanced
```

###  Esecuzione benchmark
Per eseguire le query del benchmark eseguire l'istruzione:

```bash
$ python main.py benchmark
```

## Spiegazione benchmark
Delle dieci query di benchmark, la prima, terza, quinta e settima sono effettuate con il motore di ricerca normale mentre la seconda, quarta, sesta e ottava sono le stesse query spiegate prima ma sul motore di ricerca avanzato per far vedere i diversi risultati.
Mentre la nona e decima query sono effettuate sul motore di ricerca normale per dimostrare le possibili tipologie di query.