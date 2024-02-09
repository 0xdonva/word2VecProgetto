import sys
from download_imdb import download_data_from_imdb
from whoosh_index import *
from word2vec_index import cerca_avanzata

def main():
    ext = True

    if 'download' in sys.argv:
        #SCARICA DATI DEI FILM DAL SITO www.imdb.com
        download_data_from_imdb("https://www.imdb.com/search/title/?title_type=feature&count=250")

    #CREA L'INDICE
    ix_imdb=creaindex("indexdir_imdb")

    scriviindex(ix_imdb, "file_imdb")

    if 'benchmark' in sys.argv:
        try:
            f = open("benchmark.txt")
            for riga in f.readlines():
                if "Query:" in riga:
                    print(riga)
                    cerca(riga[7:], ix_imdb)
                    print()
                    print()
        except:
            pass
    elif 'advanced' in sys.argv:
        while ext:
            frase=input("inserisci testo da ricercare:")
            if frase != "-q":
                cerca_avanzata(frase, ix_imdb)
            else:
                ext = False
    else:
        while ext:
            frase=input("inserisci testo da ricercare:")
            if frase != "-q":
                cerca(frase, ix_imdb)
            else:
                ext = False
         

if __name__ == '__main__':
    main()