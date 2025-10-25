# Linux Show Player - Modern Audio-Focused Edition
## Design Document

### 🎯 Obiettivo
Creare un'applicazione di controllo audio professionale, moderna e pulita, 
ispirata a QLab ma ottimizzata per Linux, focalizzata esclusivamente sull'audio.

### ✨ Funzionalità Chiave (QLab-like)

#### 1. **Audio Cue Professionali**
- ✅ Import audio (WAV, MP3, FLAC, OGG, AAC)
- ✅ Waveform visualization in tempo reale
- ✅ Precise in/out points (millisecondi)
- ✅ Fade in/out con curve personalizzabili
- ✅ Volume individual per cue
- ✅ Rate control (pitch/speed)
- ✅ Pre-wait / Post-wait timers
- ✅ Auto-follow (playback automatico cue successive)

#### 2. **Group Cues** (come QLab)
- 📦 Raggruppare multiple cue
- 🎭 Play simultaneo o sequenziale
- 🔄 Loop di gruppo
- 📊 Controllo master volume del gruppo

#### 3. **Interfaccia Moderna**
- 🎨 Design pulito e minimale
- 📊 Waveform display grande e leggibile
- 🎨 Color coding delle cue (personalizzabile)
- ⚡ Drag & drop fluido
- ⌨️ Hot keys personalizzabili
- 🎯 Quick search/filter cues
- 📱 Layout responsive

#### 4. **Transport Controls**
- ▶️ Play / ⏸️ Pause / ⏹️ Stop
- ⏪ Previous / ⏩ Next cue
- 🔄 Loop current cue
- 📍 Scrub through audio
- ⏱️ Timeline visuale con playhead

#### 5. **Workspace Management**
- 💾 Sessions auto-save
- 📂 Project organization
- 🔖 Cue bookmarks
- 📝 Cue notes/descriptions
- 🏷️ Tags per organizzazione

### 🎨 UI Improvements

#### Main Layout
```
┌─────────────────────────────────────────────────────────────┐
│  [🎵 File] [Edit] [Cues] [View] [Tools] [Help]       [⚙️]  │
├──────────────┬──────────────────────────────────────────────┤
│   CUE LIST   │         WAVEFORM / DETAILS                   │
│              │                                               │
│  1. Intro    │  ▓▓▓▓░░▓▓▓▓░░▓▓▓▓░░▓▓▓▓                    │
│  2. Music    │  ├──────────┤█├─────────────┤              │
│  3. Outro    │    IN       ▼      OUT                      │
│              │                                               │
│              │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━            │
│              │  Transport: ⏮️ ⏪ ▶️ ⏸️ ⏹️ ⏩ ⏭️         │
│              │                                               │
│              │  Properties:                                  │
│              │  Volume: ████████░░ 80%                      │
│              │  Fade In: 1.5s  |  Fade Out: 2.0s           │
│              │  Pre-wait: 0.0s |  Post-wait: 0.5s          │
│              │  □ Auto-follow  ☑ Loop                       │
└──────────────┴──────────────────────────────────────────────┘
```

### 🛠️ Implementazione

#### Fase 1: Core Audio (✅ Completata parzialmente)
- [x] Rimozione codice video
- [x] GStreamer backend funzionante
- [ ] Migliorare waveform generation
- [ ] Ottimizzare fade curves

#### Fase 2: UI Moderna (🔜 Prossima)
- [ ] Nuovo layout principale
- [ ] Waveform display migliorato
- [ ] Color picker per cue
- [ ] Transport controls visuali

#### Fase 3: Funzioni QLab-like
- [ ] Auto-follow system
- [ ] Group cues
- [ ] Hot keys customization
- [ ] Quick search

#### Fase 4: Polish & Performance
- [ ] Performance optimization
- [ ] Memoria management
- [ ] UI theming (dark/light)
- [ ] Accessibility

### 📦 Dipendenze
- PyQt5 (UI)
- GStreamer (Audio engine)
- NumPy (Waveform processing)
- Python 3.12+

### 🚫 NON Include
- ❌ Video playback (rimosso completamente)
- ❌ VLC backend (rimosso)
- ❌ Dipendenze complicate

### 🎯 Target Users
- Sound designers teatrali
- Event producers
- Museum installations
- Live show operators
- Broadcast radio

### ✅ Success Metrics
1. Import audio file < 2 secondi
2. Waveform visible immediatamente
3. Playback latency < 10ms
4. UI responsive (60fps)
5. Memoria stabile (no leaks)
6. Zero crashes durante show

---

## 🚀 Quick Start (dopo implementazione)

```bash
# Installa
sudo apt install python3-pyqt5 python3-gst-1.0 gstreamer1.0-plugins-good

# Avvia
python3 lisp/main.py

# Import audio
File → Import Audio (CTRL+I)

# Configure
Double-click cue → Set in/out, fades, etc.

# Play
Select cue → Press SPACE or GO button
```

---

**Note**: Questo è un programma AUDIO-ONLY. Per video, usa software dedicato.
