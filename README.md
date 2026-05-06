# PyMarble

PyMarble è un puzzle game dinamico sviluppato con **Python** (PySide6) e **QML**. Il gioco sfida l'utente a rimuovere gruppi di sfere colorate adiacenti per accumulare il punteggio più alto. Più grande è il gruppo rimosso, maggiore sarà il punteggio ottenuto!



## 🎨 Caratteristiche
- **Interfaccia Moderna:** Design fluido basato su QML con sfere animate in 3D ed effetti di illuminazione.
- **Griglia Adattiva:** La griglia di gioco si ridimensiona in base alla finestra senza errori di allineamento (grazie al calcolo preciso delle celle).
- **Multilingua:** Supporto per Italiano e Inglese con cambio lingua istantaneo direttamente dalla DropDown list.
- **Persistenza:** Il gioco ricorda la tua lingua preferita salvandola automaticamente in un file di configurazione locale (`config.json`).
- **Punteggio Dinamico:** Calcolo del punteggio basato sulla grandezza del blocco rimosso secondo la formula: $Score = (n-1)^2$.

## 🛠️ Tecnologie Utilizzate
- **Python 3.x**: Logica di gioco e gestione del backend.
- **PySide6 (Qt for Python)**: Framework per l'integrazione tra Python e l'interfaccia Qt.
- **QML**: Linguaggio dichiarativo per UI moderne, reattive e animate.
- **JSON**: Utilizzato per la persistenza delle impostazioni utente.

## 🚀 Installazione e Avvio

### 1. Prerequisiti
Assicurati di avere Python installato. Su **Arch Linux**, puoi installare le dipendenze necessarie con:

```bash
sudo pacman -S python-pyside6
