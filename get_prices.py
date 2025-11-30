import time as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def database_prezzi():

    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    dati_prodotti = []

    URL2 = "https://osservaprezzi.mise.gov.it/prezzi/livelli/beni-e-servizi-di-largo-consumo/archivio-rilevazioni-beni-e-servizi-di-largo-consumo"

    categorie = []

    ortaggi_URL = "501"
    categorie.append(ortaggi_URL)
    frutta_URL = "558"
    categorie.append(frutta_URL)
    agrumi_URL = "590"
    categorie.append(agrumi_URL)
    frutta_guscio_URL = "2136"
    categorie.append(frutta_guscio_URL)
    carne_bovina_URL = "721"
    categorie.append(carne_bovina_URL)
    carne_suina_salumi_URL = "754"
    categorie.append(carne_suina_salumi_URL)
    avicoli_uova_URL = "789"
    categorie.append(avicoli_uova_URL)
    ovicaprini_URL = "821"
    categorie.append(ovicaprini_URL)
    latte_bovino_URL = "684"
    categorie.append(latte_bovino_URL)
    olio_oliva_URL = "652"
    categorie.append(olio_oliva_URL)
    cereali_URL = "853"
    categorie.append(cereali_URL)
    semi_oleosi_URL = "928"
    categorie.append(semi_oleosi_URL)

    for categoria in categorie:

        URL = f"https://www.ismeamercati.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/{categoria}"

        try:
            driver.get(URL)

            try:
                wait = WebDriverWait(driver, 5)
                rifiuta_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'eu-privacy-button-close')))
                rifiuta_cookies.click()
            except:
                pass

            tabella = driver.find_element(By.TAG_NAME, 'tbody')
            dati = tabella.find_elements(By.TAG_NAME, 'tr')

            for elemento in dati:
                prodotto = elemento.text.split()
                nome = prodotto[0]
                index = 1
                while prodotto[index].isalpha():
                    nome = nome + " " + prodotto[index]
                    index += 1
                if prodotto[-3] == "vivo" or prodotto[-3] == "unitÃ" or prodotto[-3] == "kg":
                    unita = prodotto[-4].replace("€/","")
                    prezzo = float(prodotto[-5].replace(",","."))
                    if unita == "Kg/peso":
                        unita = "Kg"
                    elif unita == "100":
                        prezzo = round((float(prodotto[-5].replace(",",".")) / 100), 2)
                        unita = 1
                    dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita})
                else:
                    unita = prodotto[-3].replace("€/","")
                    if unita == "100":
                        prezzo = round((float(prodotto[-4].replace(",",".")) / 100), 2)
                        unita = 1
                    elif unita == "T":
                        prezzo = round((float(prodotto[-4].replace(",",".")) / 1000), 2)
                        unita = "Kg"
                    elif unita == "Capolino":
                        prezzo = float(prodotto[-4].replace(",","."))
                        unita == 1
                    else:
                        prezzo = float(prodotto[-4].replace(",","."))
                    dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita})

        except Exception as e:
            print(f"Errore primo scraping: {e}")

    try:
        driver.get(URL2)
        t.sleep(2)
        driver.fullscreen_window()
        driver.set_window_size(1920, 1080)

        tabella = driver.find_element(By.TAG_NAME, 'tbody')
        dati = tabella.find_elements(By.TAG_NAME, 'tr')

        for elemento in dati:
            prodotto = elemento.text.split()
            prezzo = float(prodotto[-2])
            nome = prodotto[0]
            index = 1
            while prodotto[index].isalpha():
                nome = nome + " " + prodotto[index]
                index += 1
            if prodotto[index].startswith("("):
                quantita = prodotto[index].replace("(","")
                index += 1
                unita = prodotto[index].replace(")","")
            if quantita == "1000" and unita == "Gr":
                unita = "Kg"
            elif quantita == "300" and unita == "Gr":
                prezzo = round(((prezzo / 3) * 10), 2)
                unita = "Kg"
            elif quantita == "100" and unita == "Cl":
                unita = "L"
            elif quantita == "125" and unita == "Gr":
                prezzo = prezzo * 8
                unita = "Kg"
            elif quantita == "1000" and unita == "Ml":
                unita = "L"
            elif quantita == "100" and unita == "Gr":
                prezzo = prezzo * 10
                unita = "Kg"
            elif quantita == "900" and unita == "Cl":
                prezzo = round(((prezzo / 9) * 10), 2)
                unita = "L"
            elif quantita == "75" and unita == "Cl":
                prezzo = round(((prezzo / 3) * 4), 2)
                unita = "L"

            dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita})
                                   
    except Exception as e:
        print(f"Errore secondo scraping: {e}")

    finally:
        driver.quit()

    return dati_prodotti

print(database_prezzi())