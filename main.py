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
        num = 1
        try:
            with open("benchmark.txt", "r") as f:
                description = None
                query = None
                for line in f:
                    if line.startswith("Descrizione:"):
                        description = line.strip()[13:]  # Ottiene la descrizione rimuovendo "Descrizione:" dall'inizio della riga
                    elif line.startswith("Query:"):
                        query = line.strip()[7:]  # Ottiene la query rimuovendo "Query:" dall'inizio della riga
                        print(description)
                        print("Query:", query)
                        print()
                        if num % 2 == 0 and num < 9:  # Verifica se il numero nella descrizione è pari
                            cerca_avanzata(query, ix_imdb)  # Esegue la ricerca avanzata con la query specificata nel benchmark
                        else:
                            cerca(query, ix_imdb)  # Esegue la ricerca standard con la query specificata nel benchmark
                        print()
                        num = num + 1
        except FileNotFoundError:
            print("File benchmark.txt non trovato.")
        except Exception as e:
            print("Si è verificato un errore durante l'elaborazione del file benchmark.txt:", e)

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