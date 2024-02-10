from pprint import pprint
import re
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import os, os.path
import glob
import pickle
from whoosh import index
from whoosh import qparser
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

# Definizione dello schema per l'indice degli IMDb
schema2 = Schema(
    TITLE=TEXT(stored=True, field_boost=2.0),
    DESCRIPTION=TEXT(stored=True, field_boost=1.5),
    DIRECTORS=TEXT(stored=True),
    ACTORS=TEXT(stored=True),
    URL=TEXT(stored=True),
    YEAR=TEXT(stored=True)
)

# Funzione per creare un nuovo indice Whoosh per IMDb
def creaindex(name):
    # Se la directory dell'indice non esiste, la crea
    if not os.path.exists(name):
        os.mkdir(name)
    # Crea l'indice Whoosh con lo schema definito
    return index.create_in(name, schema2)

# Funzione per creare un'unica entità film a partire da un risultato di IMDb
def entity(film_imdb):
    # Estrae i campi del film IMDb
    dict_film_imdb = film_imdb.fields()

    # Costruisce un dizionario contenente i dati del film IMDb
    dict_film = {
        'TITLE': dict_film_imdb['TITLE'],
        'DESCRIPTION_IMDB': dict_film_imdb['DESCRIPTION'],
        'URL_IMDB': dict_film_imdb['URL'],
        'DIRECTORS': dict_film_imdb['DIRECTORS'],
        'ACTORS': dict_film_imdb['ACTORS'],
        'YEAR': dict_film_imdb['YEAR'],
        'SCORE': film_imdb.score  # Aggiunge lo score del film IMDb
    }

    return dict_film

# Funzione per ordinare e indicizzare i risultati IMDb in base allo score
def ranking(results_imdb):
    results = []

    # Se non ci sono risultati, restituisci una lista vuota
    if not results_imdb: 
        return results

    # Estrae i dati di ciascun film IMDb e li aggiunge alla lista dei risultati
    for film_imdb in results_imdb:
        dict_film = film_imdb.fields()
        dict_film['SCORE'] = film_imdb.score  # Aggiunge lo score del film IMDb
        results.append(dict_film)

    # Ordina i risultati in base allo score in ordine decrescente
    results = sorted(results, key=lambda sc:sc['SCORE'], reverse=True)

    # Assegna un rank a ciascun film in base alla sua posizione nella lista ordinata
    for i in range(len(results)):
        results[i]['RANK'] = i

    return results


# Funzione per stampare i risultati della ricerca
def stampa(results):
    for hit in results:
        # Utilizza pprint per stampare in modo formattato il risultato
        pprint(hit)
        print()  # Stampa una riga vuota tra i risultati

# Funzione per eseguire una ricerca nell'indice IMDb
def cerca(query_t, ix_imdb):
    try:
        # Definizione dei boost per i campi della query
        fieldboosts = {
            'TITLE': 3,
            'DESCRIPTION': 1,
        }

        # Creazione del parser della query
        qp = MultifieldParser(["TITLE", "DESCRIPTION"], ix_imdb.schema, fieldboosts=fieldboosts, group=qparser.OrGroup)
        qp.add_plugin(qparser.GtLtPlugin())  # Aggiunta del plugin per supportare le query di confronto
        qp.add_plugin(qparser.FuzzyTermPlugin())  # Aggiunta del plugin per supportare le query fuzzy
        qp.remove_plugin_class(qparser.PhrasePlugin)  # Rimozione del plugin per le query di frase
        qp.add_plugin(qparser.SequencePlugin())  # Aggiunta del plugin per supportare le query di sequenza

        # Parsing della query utente
        q = qp.parse(query_t)

        # Esecuzione della ricerca usando l'indice IMDb
        searcher_imdb = ix_imdb.searcher()
        results_imdb = searcher_imdb.search(q, limit=5)  # Limita i risultati a 5

        # Utilizza la funzione ranking per ordinare i risultati per score
        results = ranking(results_imdb)

        # Stampa dei risultati
        stampa(results)

    finally:
        # Assicura che il searcher sia chiuso anche in caso di errore
        searcher_imdb.close()

# Funzione per scrivere i dati degli IMDb nell'indice
def scriviindex(ix, name_file):
    writer = ix.writer()

    # Itera su tutti i file nella cartella specificata
    for file_path in glob.glob(name_file + "/*.pkl"):
        # Apre il file binario contenente i dati del film
        with open(file_path, 'rb') as file:
            FILM_DATA = pickle.load(file)

            # Aggiunge un documento all'indice per ciascun file
            writer.add_document(
                TITLE=FILM_DATA['TITLE'],
                DESCRIPTION=FILM_DATA['DESCRIPTION'],
                URL=FILM_DATA['URL'],
                YEAR=FILM_DATA['YEAR'],
                DIRECTORS=FILM_DATA['DIRECTORS'],
                ACTORS=FILM_DATA['ACTORS']
            )

    # Esegue il commit delle modifiche all'indice
    writer.commit()


