#!/bin/bash
# Quick start script per Linux Show Player modernizzato

echo "🎵 Linux Show Player - Modern Audio Edition"
echo "==========================================="
echo ""
echo "✅ Modifiche implementate:"
echo "  - Rimosso completamente il codice video VLC"
echo "  - Aggiunto pannello controlli stile QLab in fondo"
echo "  - Controlli rapidi per fade, loop, volume, etc."
echo ""
echo "🚀 Avvio applicazione..."
echo ""

cd /home/nto/linux-show-player-master

export PYTHONPATH=/home/nto/linux-show-player-master
export DISPLAY=:0

echo "📋 Comandi disponibili:"
echo "  - Import Audio: Menu → Import Audio"
echo "  - Seleziona Cue: Click sulla lista"
echo "  - Modifica rapida: Usa pannello in basso"
echo "  - Apply: Click bottone verde '✓ Apply Changes'"
echo "  - Settings completi: Click '⚙ Full Settings...'"
echo ""
echo "💡 TIP: Il pannello in basso si attiva quando selezioni una cue!"
echo ""

python3 lisp/main.py

echo ""
echo "✅ Applicazione chiusa"
