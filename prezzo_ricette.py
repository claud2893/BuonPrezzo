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

#def prezzo_ricette():

options = Options()
#    options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

try:
    with open("dati_prodotti.json", "r", encoding="utf-8") as f:
        dati_prodotti = json.load(f)
except:
    print("Sto creando un nuovo database prezzi.")    
    dati_prodotti = database_prezzi()

nomi_database = [prodotto["nome"] for prodotto in dati_prodotti]

#    URL = input("Incolla di seguito l'URL della ricetta: ")
URL = "https://ricette.giallozafferano.it/Strauben-frittelle-tirolesi.html"

try:
    wait = WebDriverWait(driver, 8)
    driver.get(URL)
    t.sleep(3)

    try:
        rifiuta_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'amecp_button-rifiuta')))
        rifiuta_cookies.click()
    except:
        pass

    ingredienti = driver.find_element(By.CLASS_NAME, 'gz-ingredients')
    lista_ingredienti = ingredienti.find_elements(By.CLASS_NAME, 'gz-ingredient')
    mancanti = 0
    nomi_mancanti = []
    prezzo_ricetta = 0
    for elemento in lista_ingredienti:
        parti_nome = elemento.find_element(By.TAG_NAME,'a').text.split()
        nome = ""
        for parte in parti_nome:
            if parte == parti_nome[-1]:
                nome += parte
            else:
                nome += parte + " "
        parti_quantita = elemento.find_element(By.TAG_NAME, 'span').text.split()
        quantita = ""
        unita = ""
        for parte in parti_quantita:
            if parte.isalpha():
                unita = parte
            elif parte.isdigit():
                quantita = float(parte)
        if unita == "medie":
            unita = 1

        match, score, idx = process.extractOne(
            nome,
            nomi_database,
            scorer=fuzz.token_sort_ratio)
        
        if score < 50:
            mancanti += 1
            nomi_mancanti.append(nome)
            prezzo_ingrediente = 0
        else:
            prodotto_database = dati_prodotti[idx]

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

        prezzo_ricetta += prezzo_ingrediente

    if prezzo_ricetta == 0:
        print("Non è stato possibile trovare i prezzi nel database.")
    else:
        print(f"Il prezzo approssimativo della ricetta è {prezzo_ricetta}")
        if mancanti > 0:
            print(f"Il calcolo non è completo: non è stato possibile calcolare il prezzo di {mancanti} ingredienti. Ecco quali sono:")
            for nome_mancante in nomi_mancanti:
                print(f"- {nome_mancante}")

except Exception as e:
    print(f"Errore: {e}")

