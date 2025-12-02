import time as t
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def database_prezzi():

    options = Options()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    dati_prodotti = []

    # categorie = ["501", "558", "590", "2136", "721", "754", "789", "821", "684", "652", "928"]

    # for categoria in categorie:

    #     URL = f"https://www.ismeamercati.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/{categoria}"

    #     try:
    #         driver.get(URL)

    #         try:
    #             wait = WebDriverWait(driver, 5)
    #             rifiuta_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'eu-privacy-button-close')))
    #             rifiuta_cookies.click()
    #         except:
    #             pass

    #         tabella = driver.find_element(By.TAG_NAME, 'tbody')
    #         dati = tabella.find_elements(By.TAG_NAME, 'tr')

    #         for elemento in dati:
    #             prodotto = elemento.text.split()
    #             nome = prodotto[0]
    #             index = 1
    #             while prodotto[index].isalpha():
    #                 nome = nome + " " + prodotto[index]
    #                 index += 1
    #             if prodotto[-3] == "vivo" or prodotto[-3] == "unitÃ" or prodotto[-3] == "kg":
    #                 unita = prodotto[-4].replace("€/","")
    #                 prezzo = float(prodotto[-5].replace(",","."))
    #                 if unita == "Kg/peso":
    #                     unita = "kg"
    #                 elif unita == "100":
    #                     prezzo = round((float(prodotto[-5].replace(",",".")) / 100), 2)
    #                     unita = 1
    #             else:
    #                 unita = prodotto[-3].replace("€/","")
    #                 if unita == "100":
    #                     prezzo = round((float(prodotto[-4].replace(",",".")) / 100), 2)
    #                     unita = 1
    #                 elif unita == "Capolino":
    #                     prezzo = float(prodotto[-4].replace(",","."))
    #                     unita = 1
    #                 else:
    #                     prezzo = float(prodotto[-4].replace(",","."))
    #             try:
    #                 dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita.lower()})
    #             except:
    #                 dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita})

    #     except Exception as e:
    #         print(f"Errore primo scraping: {e}")

    # URL2 = "https://osservaprezzi.mise.gov.it/prezzi/livelli/beni-e-servizi-di-largo-consumo/archivio-rilevazioni-beni-e-servizi-di-largo-consumo"

    # try:
    #     driver.get(URL2)
    #     t.sleep(2)
    #     driver.fullscreen_window()
    #     driver.set_window_size(1920, 1080)

    #     tabella = driver.find_element(By.TAG_NAME, 'tbody')
    #     dati = tabella.find_elements(By.TAG_NAME, 'tr')

    #     for elemento in dati:
    #         prodotto = elemento.text.split()
    #         prezzo = float(prodotto[-2])
    #         nome = prodotto[0]
    #         index = 1
    #         while prodotto[index].isalpha():
    #             nome = nome + " " + prodotto[index]
    #             index += 1
    #         if prodotto[index].startswith("("):
    #             quantita = prodotto[index].replace("(","")
    #             index += 1
    #             unita = prodotto[index].replace(")","")
    #         if quantita == "1000" and unita == "Gr":
    #             unita = "kg"
    #         elif quantita == "300" and unita == "Gr":
    #             prezzo = round(((prezzo / 3) * 10), 2)
    #             unita = "kg"
    #         elif quantita == "100" and unita == "Cl":
    #             unita = "l"
    #         elif quantita == "125" and unita == "Gr":
    #             prezzo = prezzo * 8
    #             unita = "kg"
    #         elif quantita == "1000" and unita == "Ml":
    #             unita = "l"
    #         elif quantita == "100" and unita == "Gr":
    #             prezzo = prezzo * 10
    #             unita = "kg"
    #         elif quantita == "900" and unita == "Cl":
    #             prezzo = round(((prezzo / 9) * 10), 2)
    #             unita = "l"
    #         elif quantita == "75" and unita == "Cl":
    #             prezzo = round(((prezzo / 3) * 4), 2)
    #             unita = "l"

    #         dati_prodotti.append({"nome" : nome, "prezzo" : prezzo, "unità" : unita.lower()})
                                   
    # except Exception as e:
    #     print(f"Errore secondo scraping: {e}")

    sezioni = ["liquori-e-distillati_5405", "birra_5402", "aperitivi_5401", "riso_5383", 
               "pasta-secca_5382", "pasta-fresca_5381", "lievito_5380", "yogurt_5375", 
               "uova_5374", "latte_5368", "burro-e-altri-derivati_5373", "salumi_5370", 
               "formaggi_5372", "pesce_5371", "carne_5361", "verdura_5367", 
               "legumi-semi-e-cereali_5366", "frutta_5365", "farina_5379", 
               "liquori-e-distillati_5405", "succhi-e-bibite_5408", "vino_5410"]

   
    for sezione in sezioni:
        
        URL3 = f"https://pamacasa.pampanorama.it/{sezione}"
        
        try:
            driver.get(URL3)
            
            try:
                wait = WebDriverWait(driver, 5)
                rifiuta_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'iubenda-cs-cwa-button')))
                rifiuta_cookies.click()
                t.sleep(5)
            except:
                pass

            footer = driver.find_element(By.LINK_TEXT, 'Accessibilità')
            lista = driver.find_element(By.ID, 'product-grid')
            items = lista.find_elements(By.CLASS_NAME, 'list-item')

            index = 0
            while index < 10:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")                
                index += 1
                t.sleep(0.5)


            # nome_ultimo = items.pop().find_element(By.TAG_NAME, 'h3').text 

            # print(f"Test: {nome_ultimo}")
            item_index = 0
            Error = False
            while True:
                try:
                    if item_index != 0 and Error:
                        for i in range(item_index, len(items)):
                            nome = items[i].find_element(By.TAG_NAME, 'h3').text.title()
                            field = items[i].find_elements(By.CLASS_NAME, 'product-meta')
                            infos = field[1].text.split()

                            prezzo = float(infos[0].replace(",","."))
                            unita = infos[-1]
                            if unita == "litro":
                                unita = "l"

                            item_index = index
                            print({"nome" : nome, "prezzo" : prezzo, "unità" : unita})
                    else:
                        for index, item in enumerate(items):
                            nome = item.find_element(By.TAG_NAME, 'h3').text.title()
                            field = item.find_elements(By.CLASS_NAME, 'product-meta')
                            infos = field[1].text.split()

                            prezzo = float(infos[0].replace(",","."))
                            unita = infos[-1]
                            if unita == "litro":
                                unita = "l"

                            item_index = index
                            print({"nome" : nome, "prezzo" : prezzo, "unità" : unita})
                except:
                    Error = True
                    t.sleep(2)
                    lista = driver.find_element(By.ID, 'product-grid')
                    items = lista.find_elements(By.CLASS_NAME, 'list-item')
                    continue
                if item_index == len(items):
                    break


        except Exception as e:
            print(f"Errore terzo scraping: {e}")

        finally:
            driver.quit()

    # with open("dati_prodotti.json", "w", encoding="utf-8") as f:
    #     json.dump(dati_prodotti, f,indent=4, ensure_ascii=False)

    return dati_prodotti

print(database_prezzi())
