import requests
from bs4 import BeautifulSoup

def create_data_from_imdb(URL):
    # Imposta l'intestazione per la richiesta HTTP
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    
    # Effettua una richiesta HTTP alla pagina IMDb e ottiene il contenuto HTML
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    # Trova gli elementi HTML che contengono le informazioni del film
    job_elements = soup.find_all("div", class_="ipc-page-content-container")

    # Inizializza un dizionario per memorizzare i dati del film
    FILM_DATA = {}

    # Estrae i dati del film se trovati
    if job_elements:
        job_element = job_elements[1]

        # Estrai titolo e trama del film
        TITLE_ELEMENT = job_element.find("span", class_="hero__primary-text")
        OTHER_TITLE_ELEMENT = job_element.find("div", class_="sc-d8941411-1 fTeJrK")
        TRAMA_ELEMENT = job_element.find("span", class_="sc-466bb6c-2 chnFO")
        
        if TITLE_ELEMENT and TRAMA_ELEMENT:
            FILM_DATA["TITLE"] = OTHER_TITLE_ELEMENT.text.strip()[16:] if OTHER_TITLE_ELEMENT else TITLE_ELEMENT.text.strip()
            FILM_DATA["DESCRIPTION"] = TRAMA_ELEMENT.text.strip()

            # Estrai l'anno del film
            anno = job_element.find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt")
            FILM_YEAR = anno.find("a", class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color")
            FILM_DATA["YEAR"] = FILM_YEAR.text.strip() if FILM_YEAR else ""

            # Estrai i registi del film
            job_director = job_element.find("div", class_="ipc-metadata-list-item__content-container")
            FILM_DATA["DIRECTORS"] = [director.text.strip() for director in job_director.find_all("li")]

            # Estrai i generi del film
            FILM_DATA["GENRES"] = [gen.text.strip() for gen in soup.find("div", class_="ipc-chip-list__scroller").find_all("span", class_="ipc-chip__text")]

            # Estrai gli attori del film
            FILM_DATA["ACTORS"] = [act.text.strip() for act in soup.find("div", class_="ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid").find_all("a", class_="sc-bfec09a1-1 gCQkeh")]

            FILM_DATA["URL"] = URL

    return FILM_DATA

#print(create_data_from_imdb('https://www.imdb.com/title/tt7160372/?ref_=sr_t_14'))