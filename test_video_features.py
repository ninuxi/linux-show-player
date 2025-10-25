#!/usr/bin/env python3
# Test script per le nuove funzionalità video e layout QLab

"""
Script di test per verificare le nuove funzionalità video e il layout QLab Style
"""

import sys
import os

# Aggiungi il percorso del progetto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_video_cue_import():
    """Test import della VideoCue"""
    try:
        from lisp.cues.video_cue import VideoCue
        print("✓ VideoCue importata correttamente")
        return True
    except ImportError as e:
        print(f"✗ Errore import VideoCue: {e}")
        return False

def test_video_widgets_import():
    """Test import dei widget video"""
    try:
        from lisp.ui.widgets.video_widget import ModernVideoWidget, VideoDisplayWidget, VideoControlWidget
        print("✓ Widget video importati correttamente")
        return True
    except ImportError as e:
        print(f"✗ Errore import widget video: {e}")
        return False

def test_qlab_layout_import():
    """Test import del layout QLab"""
    try:
        from lisp.plugins.qlab_layout import QLab_Layout
        print("✓ QLab_Layout importato correttamente")
        return True
    except ImportError as e:
        print(f"✗ Errore import QLab_Layout: {e}")
        return False

def test_qlab_theme_import():
    """Test import del tema QLab"""
    try:
        from lisp.ui.themes.qlab_dark import QLab_Dark_Theme
        print("✓ QLab_Dark_Theme importato correttamente")
        return True
    except ImportError as e:
        print(f"✗ Errore import QLab_Dark_Theme: {e}")
        return False

def test_gst_video_elements_import():
    """Test import degli elementi video GStreamer"""
    try:
        from lisp.plugins.gst_backend.elements.video_elements import VideoBalance, VideoSink, VideoConverter
        print("✓ Elementi video GStreamer importati correttamente")
        return True
    except ImportError as e:
        print(f"✗ Errore import elementi video GStreamer: {e}")
        return False

def test_video_cue_settings_import():
    """Test import delle impostazioni video cue"""
    try:
        from lisp.ui.settings.cue_pages.video_cue import VideoCueSettings
        print("✓ VideoCueSettings importate correttamente")
        return True
    except ImportError as e:
        print(f"✗ Errore import VideoCueSettings: {e}")
        return False

def test_gst_video_cue_import():
    """Test import della GStreamer video cue"""
    try:
        from lisp.plugins.gst_backend.gst_video_cue import GstVideoCue, UriVideoCueFactory
        print("✓ GstVideoCue e UriVideoCueFactory importate correttamente")
        return True
    except ImportError as e:
        print(f"✗ Errore import GstVideoCue: {e}")
        return False

def main():
    """Esegui tutti i test"""
    print("🧪 Test delle nuove funzionalità video e layout QLab")
    print("=" * 60)
    
    tests = [
        test_video_cue_import,
        test_video_widgets_import,
        test_qlab_layout_import,
        test_qlab_theme_import,
        test_gst_video_elements_import,
        test_video_cue_settings_import,
        test_gst_video_cue_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Risultati: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 Tutti i test sono passati! Le nuove funzionalità sono state integrate correttamente.")
        print("\n📋 Prossimi passi:")
        print("1. Avvia Linux Show Player")
        print("2. Vai in Impostazioni → Tema → Seleziona 'QLab Dark'")
        print("3. Crea un nuovo progetto e seleziona 'QLab Style Layout'")
        print("4. Prova ad aggiungere una Video Cue dal menu")
        return True
    else:
        print("⚠️ Alcuni test sono falliti. Controlla gli errori sopra.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)