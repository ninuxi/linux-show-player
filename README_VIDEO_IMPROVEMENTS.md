# 🎬 Linux Show Player - Video Enhancement & QLab Interface

## Nuove Funzionalità Aggiunte

Questo progetto migliora Linux Show Player con:

### 🎥 **Supporto Video Completo**
- **VideoCue**: Nuova classe per gestire cue video con controlli specifici
- **Controlli Video Avanzati**: Luminosità, contrasto, saturazione, tonalità
- **Modalità Fullscreen**: Supporto per output video a schermo intero
- **Gestione Multi-Display**: Possibilità di scegliere l'output video

### 🎨 **Interfaccia Moderna in Stile QLab**
- **Layout QLab**: Nuovo layout moderno ispirato all'interfaccia di QLab
- **Controlli Moderni**: Pulsanti e slider con design professionale
- **Video Widget**: Widget video integrato con controlli di trasporto
- **Workspace Info**: Pannello informativo stile QLab

### 🔧 **Backend GStreamer Esteso**
- **GstVideoCue**: Implementazione GStreamer per le video cue
- **Factory Pattern**: Sistema per creare video cue da file
- **Pipeline Video**: Pipeline GStreamer ottimizzata per video
- **Menu Integrato**: Nuova opzione menu "Video cue (from file)"

## 📁 File Aggiunti/Modificati

### Nuovi File Creati:
```
lisp/cues/video_cue.py                           # Video cue base class
lisp/ui/widgets/video_widget.py                  # Widget video moderni
lisp/plugins/gst_backend/gst_video_cue.py       # GStreamer video cue
lisp/ui/settings/cue_pages/video_cue.py         # Impostazioni video cue
lisp/plugins/qlab_layout/__init__.py             # Layout stile QLab
lisp/plugins/qlab_layout/qlab_layout_plugin.py  # Plugin layout
```

### File Modificati:
```
lisp/application.py                              # Registrazione video cue settings
lisp/plugins/gst_backend/gst_backend.py         # Supporto video cue
lisp/cues/__init__.py                            # Export VideoCue
```

## 🚀 Come Utilizzare

### 1. Installazione Dipendenze
```bash
sudo apt update
sudo apt install -y python3-pyqt5 python3-gi python3-gi-cairo \
                    gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \
                    python3-numpy libcairo2-dev
```

### 2. Avvio dell'Applicazione
```bash
cd /percorso/verso/linux-show-player-master
python3 -m lisp.main
```

### 3. Creazione Video Cue
1. Vai nel menu **File** → **Audio/Video Cues** 
2. Seleziona **"Video cue (from file)"** (Ctrl+V)
3. Scegli un file video supportato (.mp4, .avi, .mov, etc.)
4. La video cue verrà aggiunta alla lista

### 4. Configurazione Video Cue
1. Fai doppio clic sulla video cue
2. Vai alla tab **"Video"**
3. Configura:
   - Output video (Default/Primary/Secondary)
   - Modalità fullscreen
   - Effetti video (luminosità, contrasto, etc.)
   - Rapporto aspetto

### 5. Layout QLab Style
1. All'avvio, seleziona **"QLab Style Layout"**
2. Interfaccia moderna con:
   - Lista cue a sinistra
   - Video player centrale
   - Inspector a destra
   - Controlli di trasporto moderni

## 🎛️ Controlli Video

### Controlli di Trasporto:
- **▶ GO**: Avvia la cue selezionata
- **⏹ STOP**: Ferma tutte le cue in esecuzione
- **Timeline**: Controllo posizione video
- **🔊 Volume**: Controllo volume audio
- **⛶ Fullscreen**: Modalità schermo intero

### Effetti Video:
- **Brightness**: -100 a +100
- **Contrast**: -100 a +100  
- **Saturation**: -100 a +100
- **Hue**: -180° a +180°
- **Video Fade**: Fade in/out per video

## 🎨 Personalizzazione Interfaccia

Il nuovo tema QLab Style include:
- **Colori Scuri**: Tema scuro professionale
- **Gradienti Moderni**: Effetti gradient sui controlli
- **Ombre**: Drop shadow sui widget
- **Tipografia**: Font ottimizzato per leggibilità
- **Animazioni**: Effetti hover fluidi

## 🔧 Configurazioni Tecniche

### Formati Video Supportati:
- **Container**: MP4, AVI, MOV, MKV, WebM
- **Codec Video**: H.264, H.265, VP8, VP9
- **Codec Audio**: AAC, MP3, Vorbis, FLAC

### Pipeline GStreamer:
```
UriInput → VideoBalance → VideoSink
       ↘ → Volume → AudioSink
```

### Elementi Video:
- **VideoBalance**: Controllo luminosità/contrasto
- **VideoSink**: Output video con supporto multi-display
- **AudioSink**: Output audio sincronizzato

## 🐛 Troubleshooting

### Problemi Comuni:

1. **Video non si riproduce:**
   ```bash
   sudo apt install gstreamer1.0-plugins-ugly gstreamer1.0-libav
   ```

2. **Audio assente:**
   ```bash
   sudo apt install gstreamer1.0-pulseaudio
   ```

3. **Interfaccia non si carica:**
   - Verificare che PyQt5 sia installato correttamente
   - Controllare la compatibilità del display

4. **Video cue non appare nel menu:**
   - Verificare che il backend GStreamer sia caricato
   - Controllare i log per errori di import

### Log e Debug:
```bash
python3 -m lisp.main --log debug
```

## 🎯 Funzionalità Avanzate

### Multi-Display Setup:
1. Configurare display secondario in sistema
2. Nelle impostazioni video cue selezionare "Secondary Display"
3. Il video apparirà sul display secondario in fullscreen

### Automazione:
- Le video cue supportano tutti i trigger standard (MIDI, OSC, Timer)
- Possibile concatenare video cue con follow actions
- Integrazione con show control systems

### Performance:
- Cache video automatica per playback fluido
- Ottimizzazioni GStreamer per bassa latenza
- Supporto hardware acceleration quando disponibile

## 📈 Roadmap Future

- [ ] Supporto per streaming video (RTMP, NDI)
- [ ] Effetti video avanzati (blur, color correction)
- [ ] Timeline multi-traccia
- [ ] Integrazione con proiettori via rete
- [ ] Templates per show comuni

## 🤝 Contributi

Per contribuire al progetto:
1. Fai fork del repository
2. Crea un branch per le tue modifiche
3. Testa accuratamente le nuove funzionalità
4. Invia una pull request con descrizione dettagliata

## 📄 Licenza

Questo progetto mantiene la licenza GPLv3 dell'originale Linux Show Player.

---

**Autore**: Miglioramenti video by AI Assistant
**Versione**: 0.7.0 (Enhanced with Video Support)
**Data**: Ottobre 2024