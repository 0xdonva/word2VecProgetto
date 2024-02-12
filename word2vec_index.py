from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from whoosh import index
from whoosh import qparser
from whoosh.qparser import MultifieldParser
from whoosh_index import stampa, ranking
from nltk.tokenize import word_tokenize

import nltk
nltk.download('punkt')


# Carica il modello Word2Vec preaddestrato (sostituisci 'GoogleNews-vectors-negative300.bin' con il tuo modello)
word2vec_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

def word2vec_score(query_tokens, document_text):
    """
    Calcola il punteggio Word2Vec per un documento in base alla similarità tra i token della query e il testo del documento.
    """
    score = 0
    for token in query_tokens:
        if token in word2vec_model:
            for word in document_text.split():
                if word in word2vec_model:
                    score += word2vec_model.similarity(token, word)
    return score

def word2vec_ranking(results_imdb, query_tokens):
    """
    Applica il modello di ranking Word2Vec ai risultati della ricerca.
    """
    results = []

    # Calcola il punteggio Word2Vec per ciascun documento nei risultati
    for film_imdb in results_imdb:
        document_text = film_imdb.fields()['DESCRIPTION']  # Estrai il testo del documento
        score = word2vec_score(query_tokens, document_text)  # Calcola il punteggio Word2Vec
        results.append({'film': film_imdb.fields(), 'score': score})

    # Ordina i risultati in base al punteggio Word2Vec (dal più alto al più basso)
    results.sort(key=lambda x: x['score'], reverse=True)

    return results

# Funzione per eseguire una ricerca avanzata utilizzando Word2Vec
def cerca_avanzata(query_t, ix_imdb):
    searcher_imdb = None  # Inizializza searcher_imdb al di fuori del blocco try

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

        # Tokenizzazione della query
        query_tokens = word_tokenize(query_t)

        # Trova parole simili utilizzando Word2Vec per espandere la query
        similar_words = []
        for token in query_tokens:
            if token in word2vec_model:
                similar_words.extend([word for word, _ in word2vec_model.most_similar(token)])

        # Costruzione della query avanzata unendo la query originale e le parole simili trovate
        advanced_query = ' '.join(query_tokens + similar_words)

        # Parsing della query avanzata
        q = qp.parse(advanced_query)
        query_tokens = query_t.split()  # Tokenizza la query

        searcher_imdb = ix_imdb.searcher()
        results_imdb = searcher_imdb.search(q)

        # Utilizza il modello di ranking Word2Vec per ordinare i risultati
        results = word2vec_ranking(results_imdb, query_tokens)

        # Stampa dei risultati
        stampa(results)

    finally:
        # Chiude il searcher solo se è stato creato correttamente
        if searcher_imdb:
            searcher_imdb.close()