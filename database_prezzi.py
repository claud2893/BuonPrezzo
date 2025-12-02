import time as t
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


def database_prezzi():
    """Funzione di costruzione del database con nome del prodotto, prezzo, unità."""
    
    # Inizializzazione del browser in modalità headless (per i siti per i quali è possibile impiegarla)
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # Elenco finale che costituirà il database al termine delle operaizoni
    dati_prodotti = []

    # Variabili dell'URL di Ismea mercati da impiegare nelle operazioni di scraping
    categorie = ["501", "558", "590", "2136", "721", "754", "789", "821", "684", "652", "928"]

    # Definizioni delle operazioni da avviare su ciascuna categoria del sito da cui effettuare lo scraping
    for categoria in categorie:

        # Base dell'URL da raggiungere per lo scraping
        URL = f"https://www.ismeamercati.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/{categoria}"

        # Inizializzazione dell'operazione di navigazione del browser con visualizzazione dei dettagli in caso di errore
        try:
            driver.get(URL)

            # Chiusura dell'area di messaggio relativa ai cookies qualora presente
            try:
                wait = WebDriverWait(driver, 5)
                rifiuta_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'eu-privacy-button-close')))
                rifiuta_cookies.click()
            except:
                pass

            # Denominazione degli elementi HTML di base necessari alle operazioni di scraping
            tabella = driver.find_element(By.TAG_NAME, 'tbody')
            dati = tabella.find_elements(By.TAG_NAME, 'tr')

            # Operazioni da effettuare su ciascun elemento trasformato in una stringa alfanumerica
            # Scomposizione della stringa per estrarre i dati necessari
            for elemento in dati:
                prodotto = elemento.text.split()

                # Definizione della variabile "nome" per ciascun prodotto (individuata dalla sua composizione in lettere)
                nome = prodotto[0]
                index = 1
                while prodotto[index].isalpha():
                    nome = nome + " " + prodotto[index]
                    index += 1

                # Normalizzazione delle unità e definizione del prezzo a partire dalla struttura della stringa in ciascuna casistica
                if prodotto[-3] == "vivo" or prodotto[-3] == "unitÃ" or prodotto[-3] == "kg":
                    unita = prodotto[-4].replace("€/","")
                    prezzo = float(prodotto[-5].replace(",","."))
                    if unita == "Kg/peso":
                        unita = "kg"
                    elif unita == "100":
                        prezzo = round((float(prodotto[-5].replace(",",".")) / 100), 2)
                        unita = 1
                else:
                    unita = prodotto[-3].replace("€/","")
                    if unita == "100":
                        prezzo = round((float(prodotto[-4].replace(",",".")) / 100), 2)
                        unita = 1
                    elif unita == "Capolino":
                        prezzo = float(prodotto[-4].replace(",","."))
                        unita = 1
                    else:
                        prezzo = float(prodotto[-4].replace(",","."))
                
                # Aggiunta del prodotto all'elenco finale del database con ulteriore passaggio di normalizzazione dell'unita (se espressa in lettere)
                try:
                    dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita.lower()})
                except:
                    dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita})

        except Exception as e:
            print(f"Errore primo scraping: {e}")

    # Definizione del secondo URL (Osservatorio Prezzi del Ministero) sul quale effettuare scraping
    URL2 = "https://osservaprezzi.mise.gov.it/prezzi/livelli/beni-e-servizi-di-largo-consumo/archivio-rilevazioni-beni-e-servizi-di-largo-consumo"

    # Inizializzazione dell'operazione di navigazione del browser con visualizzazione dei dettagli in caso di errore
    try:
        driver.get(URL2)
        t.sleep(2)
        driver.fullscreen_window()
        driver.set_window_size(1920, 1080)

        # Denominazione degli elementi HTML di base necessari alle operazioni di scraping
        tabella = driver.find_element(By.TAG_NAME, 'tbody')
        dati = tabella.find_elements(By.TAG_NAME, 'tr')

        # Operazioni da effettuare su ciascun elemento trasformato in una stringa alfanumerica
        # Scomposizione della stringa per estrarre i dati necessari
        for elemento in dati:
            prodotto = elemento.text.split()

            # Definizione del prezzo (penultimo elemento della stringa)
            prezzo = float(prodotto[-2])
            
            # Definizione della variabile "nome" per ciascun prodotto (individuata dalla sua composizione in lettere)
            nome = prodotto[0]
            index = 1
            while prodotto[index].isalpha():
                nome = nome + " " + prodotto[index]
                index += 1
            
            # Definizione delle variabili "unità" e "quantità" (contenute fra parentesi) e loro normalizzazione per il database secondo le varie casistiche
            if prodotto[index].startswith("("):
                quantita = prodotto[index].replace("(","")
                index += 1
                unita = prodotto[index].replace(")","")
            if quantita == "1000" and unita == "Gr":
                unita = "kg"
            elif quantita == "300" and unita == "Gr":
                prezzo = round(((prezzo / 3) * 10), 2)
                unita = "kg"
            elif quantita == "100" and unita == "Cl":
                unita = "l"
            elif quantita == "125" and unita == "Gr":
                prezzo = prezzo * 8
                unita = "kg"
            elif quantita == "1000" and unita == "Ml":
                unita = "l"
            elif quantita == "100" and unita == "Gr":
                prezzo = prezzo * 10
                unita = "kg"
            elif quantita == "900" and unita == "Cl":
                prezzo = round(((prezzo / 9) * 10), 2)
                unita = "l"
            elif quantita == "75" and unita == "Cl":
                prezzo = round(((prezzo / 3) * 4), 2)
                unita = "l"

            # Aggiunta del prodotto all'elenco finale del database con ulteriore passaggio di normalizzazione dell'unita
            dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita.lower()})

    except Exception as e:
        print(f"Errore secondo scraping: {e}")

    # Inizializzazione di un secondo browser (no headless mode)
    options2 = Options()
    driver2 = webdriver.Chrome(options=options2)

    # Variabili dell'URL di Pam a Casa da impiegare nelle operazioni di scraping
    sezioni = [
        "liquori-e-distillati_5405",
        "birra_5402",
        "aperitivi_5401",
        "riso_5383",
        "pasta-secca_5382",
        "pasta-fresca_5381",
        "lievito_5380",
        "yogurt_5375",
        "uova_5374",
        "latte_5368",
        "burro-e-altri-derivati_5373",
        "salumi_5370",
        "formaggi_5372",
        "pesce_5371",
        "carne_5361",
        "verdura_5367",
        "legumi-semi-e-cereali_5366",
        "frutta_5365",
        "farina_5379",
        "succhi-e-bibite_5408",
        "vino_5410",
    ]

    # Definizioni delle operazioni da avviare su ciascuna categoria del sito da cui effettuare lo scraping
    for sezione in sezioni:

        # Base dell'URL da raggiungere per lo scraping
        URL3 = f"https://pamacasa.pampanorama.it/{sezione}"

        # Inizializzazione dell'operazione di navigazione del browser con visualizzazione dei dettagli in caso di errore
        try:
            driver2.get(URL3)

            # Chiusura dell'area di messaggio relativa ai cookies qualora presente
            try:
                wait = WebDriverWait(driver2, 5)
                rifiuta_cookies = wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "iubenda-cs-cwa-button"))
                )
                rifiuta_cookies.click()
                t.sleep(5)
            except:
                pass

            # Denominazione degli elementi web di base necessari alle operazioni di scraping
            lista = driver2.find_element(By.ID, "product-grid")
            items = lista.find_elements(By.CLASS_NAME, "list-item")

            # Comando di scrolling fino a fine pagina per 10 volte (utile per il caricamento di tutti i prodotti nella pagina)
            index = 0
            while index < 10:
                driver2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                index += 1
                t.sleep(0.5)

            # Ciclo di scraping circoscritto al numero di prodotti nella pagina per evitare errori di loop infiniti
            item_index = 0
            while True:
                
                # Inizializzazione dell'operazione di scraping con gestione degli errori possibili
                try:

                    # Reiterazione dell'identificazione elementi web (in caso di refresh)
                    lista = driver2.find_element(By.ID, "product-grid")
                    items = lista.find_elements(By.CLASS_NAME, "list-item")
                    
                    # Condizione di interruzione del loop in caso di superamento del numero di prodotti presenti nella pagina (no loop infiniti)
                    if item_index >= len(items):
                        break
                    
                    # Identificazione elementi web per l'estrazione di dati su ciascun prodotto (per indice)
                    for i in range(item_index, len(items)):

                        # Definizione della variabile "nome"
                        nome = items[i].find_element(By.TAG_NAME, "h3").text.title()
                        
                        field = items[i].find_elements(By.CLASS_NAME, "product-meta")
                        infos = field[1].text.split()

                        # Definizione della variabile "prezzo"
                        prezzo = float(infos[0].replace(",", "."))
                        
                        # Definizione della variabile "unità"
                        unita = infos[-1]
                        
                        # Normalizzazione della variabile "unità" per l'inserimento nel database
                        if unita == "litro":
                            unita = "l"

                        # Aggiunta prodotto al database
                        dati_prodotti.append(
                            {"nome": nome, "prezzo": prezzo, "unità": unita}
                        )

                    # Ridefinizione variabile per la chiusura del loop una volta terminata la lista dei prodotti
                    item_index = len(items)

                except StaleElementReferenceException:
                    t.sleep(2)
                    continue
                except Exception as scraping_error:
                    print(f"Errore durante la lettura articoli: {scraping_error}")
                    break

        except Exception as e:
            print(f"Errore terzo scraping: {e}")

        # Chiusura del browser e ridefinizione delle impostazioni (utili per il riavvio)
        finally:
            driver2.quit()
            driver2 = webdriver.Chrome(options=options2)

    # Salvataggio del database in json
    with open("dati_prodotti.json", "w", encoding="utf-8") as f:
        json.dump(dati_prodotti, f,indent=4, ensure_ascii=False)

    # Restituzione del database al richiamo della funzione
    return dati_prodotti

