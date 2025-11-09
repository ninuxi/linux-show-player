# Test del Pannello di Controllo QLab

## Come testare il nuovo pannello

### 1. Verifica visibilità
- [ ] Il pannello è visibile in basso con sfondo scuro
- [ ] Il pannello ha un'altezza di circa 200px
- [ ] Ci sono 4 gruppi: TIMING, PLAYBACK, CONTROLLERS, ACTIONS

### 2. Importa un file audio
1. Clicca su **File** → **Import Audio** (o trascina un file audio)
2. Il file dovrebbe apparire nella lista cue

### 3. Seleziona una cue
1. Clicca sulla cue audio nella lista
2. Il pannello in basso dovrebbe **attivarsi** e mostrare i valori della cue
3. I controlli dovrebbero essere abilitati (non più grigi)

### 4. Modifica i parametri
Prova a cambiare:
- **Fade In**: imposta 2.0 secondi
- **Fade Out**: imposta 3.0 secondi
- **Volume**: sposta lo slider (0-200%)
- **Loop**: attiva/disattiva il checkbox
- **Colore**: clicca sul pulsante colorato per scegliere un colore

### 5. Applica le modifiche
1. Clicca su **"✓ Apply Changes"** (pulsante verde)
2. Le modifiche dovrebbero essere salvate sulla cue

### 6. Testa la riproduzione
1. Seleziona la cue
2. Clicca sul pulsante **GO** (in alto a sinistra)
3. L'audio dovrebbe partire con il fade in che hai impostato

### 7. Confronta con Full Settings
1. Clicca su **"⚙ Full Settings"** nel pannello
2. Si apre la finestra delle impostazioni completa
3. Verifica che i valori siano gli stessi che hai impostato nel pannello

## Cosa ho modificato

### File modificati:
1. **lisp/plugins/list_layout/view.py**
   - Corretto la gerarchia degli splitter (erano annidati male)
   - Aggiunto il pannello con dimensioni fisse (180-250px)
   - Impostato il pannello come non comprimibile
   - Aggiunto dimensioni iniziali esplicite: [100, 400, 200]
   - Migliorato il metodo resetSize() per gestire finestre piccole

2. **lisp/ui/widgets/qlab_control_panel.py**
   - Creato widget con tutti i controlli
   - Aggiunto sfondo scuro (#2a2a35) molto visibile
   - Implementato setCue() per caricare i valori
   - Implementato applyCue() per salvare le modifiche

### Struttura corretta degli splitter:
```
mainSplitter (Verticale)
├── topSplitter (Orizzontale) - Pulsante GO, info panel, controlli
├── centralSplitter (Orizzontale) - Lista cue, cue in esecuzione
└── controlPanel - PANNELLO NUOVO IN BASSO (200px fissi)
```

## Se il pannello NON è visibile

Se non vedi il pannello, prova:

1. **Ridimensiona la finestra**: Trascina il bordo inferiore verso il basso
2. **Controlla l'altezza minima**: La finestra deve essere almeno 500-600px di altezza
3. **Cerca il bordo blu**: Scorri nella finestra per vedere se c'è un bordo blu in basso

## Debug

Per vedere i log:
```bash
tail -f /tmp/lsp_test.log
```

Dovresti vedere:
```
✅ QLab Control Panel added to layout!
```

## Se serve aiuto

Fammi sapere cosa vedi:
- Il pannello è visibile?
- Qual è l'altezza della finestra?
- Puoi fare uno screenshot?
