import requests
from bs4 import BeautifulSoup



def create_data_from_imdb(URL):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    page = requests.get(URL,headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="__next")
    job_elements = results.find_all("div", class_="ipc-page-content-container")
    FILM_DATA = dict()
    job_element = job_elements[1]

    # OTTENGO TITOLO E TRAMA (IL TITOLO LO PRENDO SOLAMENTE PER EVITARE CICLI NULLI, LO SETTO PIù AVANTI)
    TITLE_ELEMENT = job_element.find("span", class_="hero__primary-text")
    OTHER_TITLE_ELEMENT = job_element.find("div", class_="sc-d8941411-1 fTeJrK")
    TRAMA_ELEMENT = job_element.find("span", class_="sc-466bb6c-2 chnFO")
    if TITLE_ELEMENT != None and TRAMA_ELEMENT != None:
        if OTHER_TITLE_ELEMENT != None:
            comodo = OTHER_TITLE_ELEMENT.text.strip()
            FILM_DATA["TITLE"] = comodo[16:]
        else:
            FILM_DATA["TITLE"] = TITLE_ELEMENT.text.strip()
        FILM_DATA["DESCRIPTION"] = TRAMA_ELEMENT.text.strip()
        anno = job_element.find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt")
        FILM_YEAR = anno.find("a", class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color")
        try: FILM_DATA["YEAR"] = FILM_YEAR.text.strip()
        except: FILM_DATA["YEAR"] = ""
        job_director = job_element.find("div", class_="ipc-metadata-list-item__content-container")
        FILM_DATA["DIRECTORS"]=list()
        for director in job_director.find_all("li"):
            FILM_DATA["DIRECTORS"].append(director.text.strip())

        # OTTENGO GENERI
        FILM_DATA["GENRES"]=list()
        genres = results.find("div", class_="ipc-chip-list__scroller")
        for gen in genres.find_all("span", class_="ipc-chip__text"):
            FILM_DATA["GENRES"].append(gen.text.strip())

        # OTTENGO I DIRETTORI E GLI ATTORI
        FILM_DATA["ACTORS"] = list()
        actor = results.find("div", class_="ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid")
        for act in actor.find_all("a", class_="sc-bfec09a1-1 gCQkeh"):
            FILM_DATA["ACTORS"].append(act.text.strip())

        FILM_DATA["URL"] = URL

    return FILM_DATA

#print(create_data_from_imdb('https://www.imdb.com/title/tt7160372/?ref_=sr_t_14'))