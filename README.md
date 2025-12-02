# BuonPrezzo

## Tool di calcolo del prezzo delle ricette (GialloZafferano)

BuonPrezzo è il risultato di un percorso didattico su automazione e programmazione in Python, ed è pensato, allo stesso modo, per finalità didattiche e di apprendimento.
Attraverso l'impiego della libreria di Selenium, BuonPrezzo costruisce un database attraverso lo scraping di tre siti web (Ismea mercati, Osservatorio Prezzi e Tariffe del Ministero delle Imprese e Pam a Casa).
I dati raccolti vengono salvati in un file json nella root, il quale viene poi impiegato per calcolare i prezzi della ricetta a partire dalla lista di ingredienti presente nel link della ricetta, individuata a sua volta da un'ulteriore operazione di scraping.
Il codice attualmente funziona solo per il sito di GialloZafferano. Basta avviare il file prezzo_ricette.py: il codice cerca automaticamente il file json se presente, in alternativa viene automaticamente avviata la funzione database_prezzi, che genera il file json richiesto.
L'operazione di creazione del database richiede una quantità di tempo variabile, dipendentemente dalla connessione e dall'hardware impiegato per avviare il codice. Successivamente alla lettura (ed eventualmente alla crezione) del database, il terminale chiede di incollare l'URL della ricetta della quale si vuole calcolare il costo (attualmente il codice funziona solo sulle ricette di GialloZafferano).
Proporzionalmente alla quantità necessaria espressa dalla lista ingredienti per ciascuno di esso, il codice calcola il prezzo della ricetta, e restituisce il numero e l'elenco degli ingredienti per i quali non è stato possibile calcolare il costo, dipendentemente dalla quantità non definita nella lista degli ingredienti o dalla sua assenza nel database.
Poichè la nomenclatura fra il database e la lista degli ingredienti non coincide mai del tutto, è stato impiegato uno strumento di calcolo della somiglianza fra queste due etichette attraverso l'assegnazione di un punteggio di coincidenza minima con la libreria RapidFuzz.
L'accuratezza del risultato è dunque variabile e dipendente, in gran parte dalla nomenclatura e dall'accuratezza della denominazione degli ingredienti e del database.

## Prospettive di sviluppo

Il codice è pensato come base di partenza per successivi sviluppi e future implementazioni. Fra le molte possibili ci sono:
- Costruzione di un'interfaccia grafica
- Release di file eseguibili
- Implementazione di più siti sui quali effettuare la ricerca
- Sostituzione della libreria RapidFuzz con un agente IA per il riconoscimento degli ingredienti nel database (necessaria un'API per l'impiego dei token)
- Riconoscimento della data di generazione dell'ultimo database e proposta di aggiornamento (o meccanismo automatico) qualora esso risultasse troppo retrodatato
- Salvataggio della cronologia di ricerca
