# Companion / Stream Deck Integration

Integrazione automatica tra **Bitfocus Companion** e **Linux Show Player** per controllare i cue tramite Stream Deck (o altri controller).

## ✨ Caratteristiche

- **Auto-mappatura**: I pulsanti dello Stream Deck si mappano automaticamente ai cue
- **Zero configurazione manuale OSC**: Non serve configurare ogni singolo comando OSC
- **GO Button**: Pulsante dedicato per eseguire il prossimo cue
- **Setup 3 passi**: Configurazione rapida in meno di 2 minuti

## 🚀 Setup Rapido

### 1. Abilita integrazione in LSP

1. Apri **Linux Show Player**
2. Vai in **Impostazioni → Companion / Stream Deck**
3. Spunta **"Enable Companion / Stream Deck integration"**
4. Porta predefinita: **12321** (lasciala così)
5. Spunta **"Auto-map Stream Deck buttons to cues"**

### 2. Configura Companion

1. Apri **Companion** (scaricalo da https://bitfocus.io/companion se non lo hai)
2. Vai in **Settings → OSC**:
   - Enable **"OSC Listener"**
   - Porta: **12321** (deve coincidere con LSP)
3. Aggiungi connessione:
   - Type: **"Generic OSC"**
   - Target IP: **127.0.0.1** (se LSP è sullo stesso PC)
   - Target Port: **12321**

### 3. Configura i pulsanti dello Stream Deck

In Companion, per ogni pulsante che vuoi usare:

1. Aggiungi **Action → Generic OSC → Send message**
2. Path OSC da inviare:
   - **Pulsante GO**: `/location/1/0/0/press`
   - **Cue 0**: `/location/1/0/1/press`
   - **Cue 1**: `/location/1/0/2/press`
   - **Cue 2**: `/location/1/0/3/press`
   - etc.

**Formula generale**: `/location/1/<row>/<column>/press`

Dove:
- `row` = riga (0, 1, 2, ...)
- `column` = colonna (0, 1, 2, ...)
- Il pulsante 0,0 è riservato al GO
- Tutti gli altri si mappano automaticamente ai cue

## 📋 Mappatura Automatica

| Stream Deck | LSP |
|-------------|-----|
| Pulsante 0,0 | GO (prossimo cue) |
| Pulsante 0,1 | Cue 0 |
| Pulsante 0,2 | Cue 1 |
| Pulsante 0,3 | Cue 2 |
| Pulsante 1,0 | Cue 5 |
| ... | ... |

**Calcolo indice**: `cue_index = row * 5 + column - 1` (su Stream Deck standard 5x3)

## 🔧 Esempio Configurazione Companion

Per un setup completo con 15 pulsanti su Stream Deck:

```
Riga 0:
  [0,0] GO        → /location/1/0/0/press
  [0,1] Cue 0     → /location/1/0/1/press
  [0,2] Cue 1     → /location/1/0/2/press
  [0,3] Cue 2     → /location/1/0/3/press
  [0,4] Cue 3     → /location/1/0/4/press

Riga 1:
  [1,0] Cue 5     → /location/1/1/0/press
  [1,1] Cue 6     → /location/1/1/1/press
  ...

Riga 2:
  [2,0] Cue 10    → /location/1/2/0/press
  ...
```

## 🐛 Troubleshooting

### LSP non riceve comandi da Companion

1. **Verifica che l'integrazione sia abilitata** in LSP Settings
2. **Controlla la porta**: deve essere 12321 sia in LSP che in Companion OSC settings
3. **Firewall**: assicurati che la porta 12321 UDP sia aperta
4. **Test**: In LSP Settings → Companion, clicca **"Test Connection"**

### Companion non si connette

1. Verifica che LSP sia in esecuzione
2. Controlla Companion Log per errori OSC
3. Prova a inviare un comando manuale da Companion:
   ```
   /location/1/0/0/press
   ```
   Dovresti vedere un log in LSP console

### I cue non si eseguono

1. **Verifica mapping**: Il pulsante invia il path OSC corretto?
2. **Auto-map abilitato**: Spunta "Auto-map Stream Deck buttons to cues" in LSP
3. **Indice cue**: Assicurati che ci sia un cue all'indice corrispondente

## 🔌 Requisiti

- **Linux Show Player** ≥ 0.6.5
- **Bitfocus Companion** ≥ 3.0
- **python-osc** library (installato automaticamente)

## 📚 Comandi OSC Supportati

| Path OSC | Azione |
|----------|--------|
| `/location/<page>/<row>/<col>/press` | Premi e rilascia pulsante (esegui cue) |
| `/location/<page>/<row>/<col>/down` | Premi pulsante (start cue) |
| `/location/<page>/<row>/<col>/up` | Rilascia pulsante (stop cue se previsto) |

Per altri comandi OSC standard di Companion (cambio colore, testo, etc.), usa il plugin OSC nativo di LSP.

## 🎯 Vantaggi rispetto a OSC manuale

| Metodo | Passaggi | Manutenzione |
|--------|----------|--------------|
| **OSC Manuale** | ~50+ comandi OSC da configurare | Ogni volta che aggiungi un cue |
| **Companion Integration** | 3 passi + mapping pulsanti | Automatica |

## 💡 Tips & Tricks

### Usa pagine multiple su Companion
- Pagina 1: Cue principali
- Pagina 2: Cue di backup
- Pagina 3: Effetti speciali

Cambia il numero di pagina nel path:
```
/location/2/0/1/press  → Pagina 2, cue 0
```

### Feedback visivo
Configura i pulsanti di Companion con:
- **Colori** che riflettono lo stato del cue
- **Testi dinamici** con variabili custom

(Richiede configurazione avanzata in Companion)

## 📝 Note Tecniche

- **Protocollo**: OSC over UDP
- **Porta default**: 12321
- **Thread separato**: L'OSC listener gira in un thread dedicato per non bloccare LSP
- **Performance**: Latenza < 10ms su rete locale

## 🤝 Contributi

Questo modulo è parte del progetto Linux Show Player.
Per bug report o feature request: https://github.com/FrancescoCeruti/linux-show-player/issues

---

**Made with ❤️ for the stage production community**
