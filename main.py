import sys
from download_imdb import download_data_from_imdb
from whoosh_index import *
from word2vec_index import cerca_avanzata

def main():
    # Imposta il valore di default per il flag di estensione
    ext = True

    # Se è presente il flag 'download' tra gli argomenti della riga di comando, scarica i dati da IMDb
    if 'download' in sys.argv:
        # SCARICA DATI DEI FILM DAL SITO www.imdb.com
        download_data_from_imdb("https://www.imdb.com/search/title/?title_type=feature&count=250")

    # CREA L'INDICE
    ix_imdb = creaindex("indexdir_imdb")
    scriviindex(ix_imdb, "file_imdb")  # Scrive i dati nell'indice IMDb

    # Se è presente il flag 'benchmark' tra gli argomenti della riga di comando, esegui il benchmark
    if 'benchmark' in sys.argv:
        try:
            f = open("benchmark.txt")
            for riga in f.readlines():
                if "Query:" in riga:
                    print(riga)
                    cerca(riga[7:], ix_imdb)  # Esegue la ricerca con la query specificata nel benchmark
                    print()
                    print()
        except:
            pass

    # Se è presente il flag 'advanced' tra gli argomenti della riga di comando, esegui la ricerca avanzata
    elif 'advanced' in sys.argv:
        while ext:
            frase = input("inserisci testo da ricercare:")
            if frase != "-q":  # Se l'input non è "-q", esegui la ricerca avanzata
                cerca_avanzata(frase, ix_imdb)
            else:
                ext = False  # Se l'input è "-q", interrompi il ciclo e termina il programma

    # Se non è presente alcun flag specifico, esegui la ricerca standard
    else:
        while ext:
            frase = input("inserisci testo da ricercare:")
            if frase != "-q":  # Se l'input non è "-q", esegui la ricerca standard
                cerca(frase, ix_imdb)
            else:
                ext = False  # Se l'input è "-q", interrompi il ciclo e termina il programma

# Esegui la funzione main se questo script è eseguito come programma principale
if __name__ == '__main__':
    main()