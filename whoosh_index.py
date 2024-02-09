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



schema = Schema(TITLE=TEXT(stored=True, field_boost=2.0),
                DESCRIPTIONIMDB=TEXT(stored=True, field_boost=1.5),
                DIRECTORS=TEXT(stored=True),
                ACTORS=TEXT(stored=True),
                URLROTTEN=TEXT(stored=False),
                URLIMDB=TEXT(stored=False),
                YEAR=TEXT(stored=True))

schema2 = Schema(TITLE=TEXT(stored=True, field_boost=2.0),
                DESCRIPTION=TEXT(stored=True, field_boost=1.5),
                DIRECTORS=TEXT(stored=True),
                ACTORS=TEXT(stored=True),
                URL=TEXT(stored=True),
                YEAR=TEXT(stored=True))


def creaindex(name):
    if not os.path.exists(name):
        os.mkdir(name)
    return index.create_in(name, schema2)


#Dati 2 risultati che rappresentano lo stesso film viene generato un unico film, fondendo i dati dei 2 risultati in un unica entità
def entity(film_imdb):
    dict_film_imdb = film_imdb.fields()

    dict_film = {
        'TITLE': dict_film_imdb['TITLE'],
        'DESCRIPTION_IMDB': dict_film_imdb['DESCRIPTION'],
        'URL_IMDB': dict_film_imdb['URL'],
        'DIRECTORS': dict_film_imdb['DIRECTORS'],
        'ACTORS': dict_film_imdb['ACTORS'],
        'YEAR': dict_film_imdb['YEAR'],
        'SCORE': film_imdb.score
    }

    return dict_film


def ranking(results_imdb):
    results = list()

    if not results_imdb: 
        return results

    for film_imdb in results_imdb:
        dict_film = film_imdb.fields()
        dict_film['SCORE'] = film_imdb.score
        results.append(dict_film)

    results = sorted(results, key=lambda sc:sc['SCORE'], reverse=True)  # Ordina i risultati in base allo score

    for i in range(len(results)):
        results[i]['RANK'] = i

    return results


def stampa(results):
    for hit in results:
        pprint(hit)
        print()
    

def cerca(query_t, ix_imdb):
    try:
        fieldboosts = {
            'TITLE': 3,
            'DESCRIPTION': 1,
        }

        qp = MultifieldParser(["TITLE", "DESCRIPTION"], ix_imdb.schema, fieldboosts=fieldboosts, group=qparser.OrGroup)
        qp.add_plugin(qparser.GtLtPlugin())
        qp.add_plugin(qparser.FuzzyTermPlugin())
        qp.remove_plugin_class(qparser.PhrasePlugin)
        qp.add_plugin(qparser.SequencePlugin())

        q = qp.parse(query_t)

        # Parse della query utente usando l'indice IMDb
        searcher_imdb = ix_imdb.searcher()
        results_imdb = searcher_imdb.search(q, limit=5)

        # Utilizza la funzione fusion_ranking solo per IMDb
        results = ranking(results_imdb)

        # Stampa dei risultati
        stampa(results)

    finally:
        searcher_imdb.close()

def scriviindex(ix, name_file):
    writer = ix.writer()

    for file_path in glob.glob(name_file + "/*.pkl"):
        with open(file_path, 'rb') as file:
            FILM_DATA = pickle.load(file)
            writer.add_document(
                TITLE=FILM_DATA['TITLE'],
                DESCRIPTION=FILM_DATA['DESCRIPTION'],
                URL=FILM_DATA['URL'],
                YEAR=FILM_DATA['YEAR'],
                DIRECTORS=FILM_DATA['DIRECTORS'],
                ACTORS=FILM_DATA['ACTORS']
            )

    writer.commit()


