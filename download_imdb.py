import requests
import pickle
from bs4 import BeautifulSoup
from pathlib import Path
from imdb import create_data_from_imdb

def download_data_from_imdb(URL):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    page = requests.get(URL,headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    #results = soup.find(id="__next")
    results = soup.find("div", class_="ipc-page-grid__item ipc-page-grid__item--span-2")
    job_elements = results.find_all("div", class_="sc-f24f1c5c-4 eZiMbd dli-parent")
    
    FILM_DATA = dict()
    URL_FILM_BASE="https://www.imdb.com/"
    
    #CREA LA CARTELLA DOVE METTERA' I FILE (SE NON ESISTE)
    Path("file_imdb").mkdir(parents=True, exist_ok=True)
    
    for job_element in job_elements:
        URL_FILM = job_element.find("a").get('href')
        
        try:
            #CREA IL DIZIONARIO DI UN FILM
            FILM_DATA=create_data_from_imdb(URL_FILM_BASE+URL_FILM)

            #CREA IL FILE BINARIO E SALVA IL DIZIONARIO CON I DATI DEL FILM
            file = open('file_imdb/'+FILM_DATA['TITLE']+'.pkl','wb')
            pickle.dump(FILM_DATA, file)
            file.close()

            # PER LEGGERE IL FILE BINARIO
            '''file2 = open('file_imdb/'+FILM_DATA['TITLE']+'.pkl','rb')
            FILM_DATA=pickle.load(file2)
            file2.close()'''
        
        
            
        except Exception as e:
            print("LINK: "+URL_FILM+" non valido")