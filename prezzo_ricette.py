import time as t
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import database_prezzi

#def prezzo_ricette():

options = Options()
#    options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

try:
    with open("dati_prodotti.json", "r", encoding="utf-8") as f:
        dati_prodotti = json.load(f)
except:
    dati_prodotti = database_prezzi()
    print("Sto creando un nuovo database prezzi.")

#    URL = input("Incolla di seguito l'URL della ricetta: ")
URL = "https://ricette.giallozafferano.it/Strauben-frittelle-tirolesi.html"

try:
    wait = WebDriverWait(driver, 8)
    driver.get(URL)
    t.sleep(5)

    try:
        rifiuta_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'amecp_button-rifiuta')))
        rifiuta_cookies.click()
    except:
        pass

    ingredienti = driver.find_element(By.CLASS_NAME, 'gz-ingredients')
    lista_ingredienti = ingredienti.find_elements(By.CLASS_NAME, 'gz-ingredient')
    for elemento in lista_ingredienti:
        nome = elemento.find_element(By.TAG_NAME,'a').text.split()
        quantita = elemento.find_element(By.TAG_NAME, 'span').text.split()

        print(f"{nome} {quantita}")


except Exception as e:
    print(f"Errore: {e}")

