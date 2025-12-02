import time as t
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rapidfuzz import process, fuzz

from database_prezzi import database_prezzi

def prezzo_ricette():
    """Funzione di calcolo del prezzo della ricetta a partire da una lista ingredienti e da un database di prezzi per prodotto"""

    # Inizializzazione del browser in modalità headless
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # Lettura del database (se esitente) o sua creazione
    try:
        with open("dati_prodotti.json", "r", encoding="utf-8") as f:
            dati_prodotti = json.load(f)
            print("Database preesistente caricato.")
    except:
        print("Sto creando un nuovo database prezzi.")    
        dati_prodotti = database_prezzi()

    # Elenco dei nomi dei prodotti nel database (utile per individuare l'ingrendiente con la miglior corrispondenza)
    nomi_database = [prodotto["nome"] for prodotto in dati_prodotti]

    # Richiesta dell'URL della ricetta per la quale effettuare il calcolo
    URL = input("Incolla di seguito l'URL della ricetta da GialloZafferano: ")

    # Inizializzazione dell'operazione di navigazione del browser con visualizzazione dei dettagli in caso di errore
    try:
        wait = WebDriverWait(driver, 8)
        driver.get(URL)
        t.sleep(3)

        # Chiusura dell'area di messaggio relativa ai cookies qualora presente
        try:
            rifiuta_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'amecp_button-rifiuta')))
            rifiuta_cookies.click()
        except:
            pass
        
        # Denominazione degli elementi HTML di base necessari all'individuazione della lista ingredienti
        ingredienti = driver.find_element(By.CLASS_NAME, 'gz-ingredients')
        lista_ingredienti = ingredienti.find_elements(By.CLASS_NAME, 'gz-ingredient')
        
        # Inizializzazione delle variabili del prezzo della ricetta e di eventuali ingredienti mancanti
        mancanti = 0
        nomi_mancanti = []
        prezzo_ricetta = 0

        # Inizializzazione del processo di individuazione degli elementi nella lista ingredienti
        for elemento in lista_ingredienti:
            parti_nome = elemento.find_element(By.TAG_NAME,'a').text.split()
            
            # Ricostruzione della stringa per la variabile "nome"
            nome = ""
            for parte in parti_nome:
                if parte == parti_nome[-1]:
                    nome += parte
                else:
                    nome += parte + " "

            # Definizione delle variabili "unità" e "quantità" nel corrispondente elemento HTML
            parti_quantita = elemento.find_element(By.TAG_NAME, 'span').text.split()
            quantita = ""
            unita = ""
            for parte in parti_quantita:
                if parte.isalpha():
                    unita = parte
                elif parte.isdigit():
                    quantita = float(parte)
            
            # Normalizzazione della variabile "unità"
            if unita == "medie":
                unita = 1

            # Assegnazione del punteggio di aderenza fra il nome ingrediente e il nome del prodotto nel database
            match, score, idx = process.extractOne(
                nome,
                nomi_database,
                scorer=fuzz.token_sort_ratio)
            
            # Passaggio del prodotto con punteggio maggiore ed eventuale scarto in caso di aderenza insufficiente
            if score < 55:
                mancanti += 1
                nomi_mancanti.append(nome)
                prezzo_ingrediente = 0
            else:
                prodotto_database = dati_prodotti[idx]

                # Calcolo del prezzo di ciascun ingrediente se individuabile in base alla quantità espressa dalla lista ingredienti
                if unita == prodotto_database["unità"]:
                    prezzo_ingrediente = quantita * prodotto_database["prezzo"]
                elif unita == "g" and prodotto_database["unità"] == "kg":
                    prezzo_ingrediente = round(((prodotto_database["prezzo"] / 1000) * quantita), 2)
                elif unita == "ml" and prodotto_database["unità"] == "l":
                    prezzo_ingrediente = round(((prodotto_database["prezzo"] / 1000) * quantita), 2)
                elif unita == "cl" and prodotto_database["unità"] == "l":
                    prezzo_ingrediente = round(((prodotto_database["prezzo"] / 100) * quantita), 2)
                else:
                    mancanti += 1
                    nomi_mancanti.append(nome)
                    prezzo_ingrediente = 0

            # Addizione dei prezzi degli ingredienti per definire il prezzo della ricetta
            prezzo_ricetta += prezzo_ingrediente

        # Formulazione dell'output al termine del calcolo sulla base dei risultati ottenuti
        if prezzo_ricetta == 0:
            print("Non è stato possibile trovare i prezzi nel database.")
        else:
            print(f"Il prezzo approssimativo della ricetta è {prezzo_ricetta}")
            if mancanti > 0:
                print(f"Il calcolo non è completo: non è stato possibile calcolare il prezzo di {mancanti} ingredienti. Ecco quali:")
                for nome_mancante in nomi_mancanti:
                    print(f"- {nome_mancante}")

    except Exception as e:
        print(f"Errore: {e}")

# Inizializzazione della funzione
if __name__ == "__main__":
    prezzo_ricette()