from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from whoosh import index
from whoosh import qparser
from whoosh.qparser import MultifieldParser
from whoosh_index import stampa, ranking
from nltk.tokenize import word_tokenize

import nltk
nltk.download('punkt')


# Carica il modello Word2Vec preaddestrato (sostituisci 'mymodel.bin' con il tuo modello)
word2vec_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

def cerca_avanzata(query_t, ix_imdb):
    searcher_imdb = None  # Inizializza searcher_imdb al di fuori del blocco try

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

        query_tokens = word_tokenize(query_t)

        similar_words = []
        for token in query_tokens:
            if token in word2vec_model:
                similar_words.extend([word for word, _ in word2vec_model.most_similar(token)])

        advanced_query = ' '.join(query_tokens + similar_words)

        q = qp.parse(advanced_query)

        searcher_imdb = ix_imdb.searcher()  # Assegna searcher_imdb all'interno del blocco try

        results_imdb = searcher_imdb.search(q, limit=5)

        results = ranking(results_imdb)

        stampa(results)

    finally:
        if searcher_imdb:
            searcher_imdb.close()