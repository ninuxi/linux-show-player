# Linux Show Player - Video Support & QLab Style Layout

## Nuove Funzionalità Aggiunte

### 1. Supporto Video Completo

#### Video Cues
- **Nuova classe VideoCue**: Estende MediaCue con funzionalità specifiche per i video
- **Controlli video**: Luminosità, contrasto, saturazione, tonalità
- **Modalità fullscreen**: Supporto per proiezione a schermo intero
- **Output multipli**: Configurazione per display primari/secondari
- **Effetti video**: Fade video e controlli avanzati

#### Backend Video
- **Elementi GStreamer video**: VideoBalance, VideoSink, VideoConverter, VideoScale, VideoRate
- **Pipeline video**: Supporto completo per pipeline audio/video
- **Factory video**: UriVideoCueFactory per cue video da file
- **Integrazione GStreamer**: Utilizzo dell'infrastruttura esistente

### 2. Layout QLab Style

#### Interfaccia Moderna
- **Design ispirato a QLab**: Layout pulito e professionale
- **Pannelli organizzati**: 
  - Sinistra: Lista cue e controlli trasporto
  - Centro: Display video con controlli
  - Destra: Inspector e controlli cue
- **Controlli moderni**: Pulsanti GO/STOP stilizzati
- **Info workspace**: Pannello con statistiche sessione

#### Widget Video Avanzati
- **VideoDisplayWidget**: Area di visualizzazione video con placeholder
- **VideoControlWidget**: Controlli transport moderni (play/pause/stop/volume/fullscreen)
- **ModernVideoWidget**: Combinazione completa di display e controlli
- **Effetti grafici**: Ombre e gradienti per un look professionale

### 3. Tema QLab Dark

#### Stile Moderno
- **Palette scura**: Colori ispirati a QLab
- **Gradienti**: Effetti visivi moderni
- **Controlli stilizzati**: Pulsanti, slider, e widget con design coerente
- **Tipografia**: Font e dimensioni ottimizzate per la leggibilità

### 4. Impostazioni Video

#### Pagina Impostazioni Video Cue
- **Output video**: Selezione display di destinazione
- **Proprietà video**: Controlli per aspect ratio
- **Effetti colore**: Sliders per brightness, contrast, saturation, hue
- **Opzioni avanzate**: Fade video, fullscreen automatico

## Installazione e Uso

### Prerequisiti
Le dipendenze GStreamer per il video dovrebbero già essere installate con il supporto audio esistente:
- gstreamer1.0-plugins-good
- gstreamer1.0-plugins-bad
- gstreamer1.0-libav

### Attivazione

1. **Tema QLab Dark**: 
   - Vai in Impostazioni → Tema → "QLab Dark"

2. **Layout QLab Style**:
   - Crea nuovo progetto → Seleziona "QLab Style Layout"
   - O vai in Impostazioni → Layout → Cambia layout

3. **Video Cues**:
   - Menu → Media Cues → "Video cue (from file)" (Ctrl+V)
   - Seleziona file video supportati
   - Configura nelle impostazioni cue

### Formati Video Supportati
Tutti i formati supportati da GStreamer:
- MP4, MOV, AVI, MKV
- WEBM, OGV, FLV
- E molti altri...

### Controlli Video

#### Trasporto
- **GO**: Avvia la cue selezionata
- **STOP**: Ferma tutte le cue in esecuzione
- **Controlli video**: Play/Pause/Stop/Volume/Fullscreen per singole cue

#### Impostazioni Cue Video
- **Video Output**: Default, Primary Display, Secondary Display, Custom Window
- **Fullscreen**: Avvio automatico a schermo intero  
- **Aspect Ratio**: Auto, 4:3, 16:9, 16:10, Custom
- **Video Effects**: Brightness (-100 to +100), Contrast (-100 to +100), Saturation (-100 to +100), Hue (-180° to +180°)
- **Video Fade**: Abilita effetti di fade per il video

## Struttura File Aggiunti

```
lisp/
├── cues/
│   └── video_cue.py                    # Classe VideoCue
├── plugins/
│   ├── gst_backend/
│   │   ├── elements/
│   │   │   └── video_elements.py       # Elementi GStreamer video
│   │   ├── gst_video_cue.py           # GStreamer video cue implementation
│   └── qlab_layout/                    # Plugin layout QLab
│       ├── __init__.py                 # Classe QLab_Layout
│       ├── qlab_layout_plugin.py       # Plugin registration
│       └── default.json               # Configurazione plugin
├── ui/
│   ├── themes/
│   │   └── qlab_dark.py               # Tema QLab Dark
│   ├── settings/
│   │   └── cue_pages/
│   │       └── video_cue.py           # Impostazioni video cue
│   └── widgets/
│       └── video_widget.py            # Widget video moderni
```

## Sviluppi Futuri Possibili

### Funzionalità Avanzate Video
- **Mapping video**: Correzione keystone e mapping geometrico
- **Layers video**: Gestione multistrato
- **Effetti tempo reale**: Filtri e transizioni live
- **Sincronizzazione**: Sync video/audio preciso

### Miglioramenti Layout
- **Personalizzazione**: Layout configurabili dall'utente
- **Workspace multiple**: Gestione progetti multipli
- **Timeline view**: Vista timeline per sequencing
- **Live controls**: Controlli performance dal vivo

### Integrazione Hardware
- **Controlli MIDI/OSC video**: Mappatura controlli esterni
- **Hardware video**: Supporto schede capture/output dedicate
- **Proiezione multi-display**: Gestione avanzata output multipli

## Note Tecniche

### Architettura
- Utilizza l'architettura plugin esistente
- Estende le classi MediaCue/GstMediaCue
- Integrazione completa con il backend GStreamer
- Compatibilità con tutti i layout esistenti

### Performance
- Pipeline GStreamer ottimizzate
- Rendering hardware quando disponibile
- Gestione memoria efficiente per video
- Supporto codec hardware

### Compatibilità
- Mantiene compatibilità con progetti esistenti
- Supporta tutte le funzionalità audio esistenti
- Aggiornamento graduale opzionale
- Fallback automatico per elementi mancanti