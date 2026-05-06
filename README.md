# PyMarble

PyMarble è un puzzle game dinamico sviluppato con **Python** (PySide6) e **QML**. Il gioco sfida l'utente a rimuovere gruppi di sfere colorate adiacenti per accumulare il punteggio più alto. Più grande è il gruppo rimosso, maggiore sarà il punteggio ottenuto!


## 🎨 Caratteristiche
- **Interfaccia Moderna:** Design fluido basato su QML con sfere animate in 3D ed effetti di illuminazione.
- **Griglia Adattiva:** La griglia di gioco si ridimensiona in base alla finestra senza errori di allineamento.
- **Multilingua:** Supporto per Italiano e Inglese con cambio lingua istantaneo in tempo reale.
- **Persistenza:** Il gioco ricorda la tua lingua preferita salvandola in un file di configurazione locale (`config.json`).
- **Punteggio Dinamico:** Calcolo del punteggio basato sulla grandezza del blocco rimosso ($Score = (n-1)^2$).

## 🛠️ Tecnologie Utilizzate
- **Python 3.x**: Logica di gioco e backend.
- **PySide6 (Qt for Python)**: Framework per l'integrazione UI.
- **QML**: Linguaggio per interfacce reattive.
- **JSON**: Per la persistenza delle impostazioni.

## 🚀 Installazione e Avvio

### 1. Prerequisiti
Su **Arch Linux**, installa le dipendenze con:
```bash
sudo pacman -S python-pyside6 openssh

## ⚖️ Licenza

Questo progetto è rilasciato sotto la Licenza MIT.
