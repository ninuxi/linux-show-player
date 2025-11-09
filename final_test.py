#!/usr/bin/env python3

"""
Final comprehensive test for Linux Show Player with video improvements
"""

import sys
import os

# Add the lisp module to Python path
sys.path.insert(0, '/home/nto/linux-show-player-master')

print("🎬 LINUX SHOW PLAYER - VIDEO ENHANCEMENT FINAL TEST")
print("=" * 60)

def test_application_startup():
    """Test if the application can start"""
    print("\n🚀 Testing application startup...")
    
    try:
        # Import main modules
        from lisp import application
        from lisp.main import main
        print("✓ Main application modules imported successfully")
        
        # Test video cue imports
        from lisp.cues.video_cue import VideoCue
        from lisp.plugins.gst_backend.gst_video_cue import GstVideoCue
        print("✓ Video cue modules imported successfully")
        
        # Test UI modules
        from lisp.ui.widgets.video_widget import ModernVideoWidget
        from lisp.ui.settings.cue_pages.video_cue import VideoCueSettings
        print("✓ Video UI modules imported successfully")
        
        # Test layout modules
        from lisp.plugins.qlab_layout import QLab_Layout
        print("✓ QLab layout imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Application startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_video_cue_creation():
    """Test video cue creation without GUI"""
    print("\n🎥 Testing video cue creation...")
    
    try:
        from lisp.plugins.gst_backend.gst_video_cue import UriVideoCueFactory
        
        # Create a mock app
        class MockApp:
            pass
            
        app = MockApp()
        factory = UriVideoCueFactory([])
        
        # Test factory creation
        video_cue = factory(app, uri="/fake/path/video.mp4")
        print("✓ Video cue factory works")
        
        # Test video cue properties
        video_cue.fullscreen = True
        video_cue.brightness = 0.75
        video_cue.video_output = "secondary_display"
        
        print("✓ Video cue properties can be set")
        print(f"  - Fullscreen: {video_cue.fullscreen}")
        print(f"  - Brightness: {video_cue.brightness}")
        print(f"  - Video Output: {video_cue.video_output}")
        
        return True
        
    except Exception as e:
        print(f"✗ Video cue creation failed: {e}")
        return False

def test_gstreamer_backend():
    """Test GStreamer backend integration"""
    print("\n🔧 Testing GStreamer backend integration...")
    
    try:
        from lisp.plugins.gst_backend.gst_backend import GstBackend
        
        # Test supported extensions includes video
        class MockApp:
            conf = {"cache.position": "/tmp"}
            
        backend = GstBackend(MockApp())
        extensions = backend.supported_extensions()
        
        has_video = len(extensions.get('video', [])) > 0
        has_audio = len(extensions.get('audio', [])) > 0
        
        print(f"✓ Backend supports {len(extensions.get('video', []))} video formats")
        print(f"✓ Backend supports {len(extensions.get('audio', []))} audio formats")
        
        return has_video and has_audio
        
    except Exception as e:
        print(f"✗ GStreamer backend test failed: {e}")
        return False

def test_layout_registration():
    """Test layout registration system"""
    print("\n📐 Testing layout registration...")
    
    try:
        from lisp import layout
        from lisp.plugins.qlab_layout import QLab_Layout
        
        # Register the layout
        layout.register_layout(QLab_Layout)
        
        # Check if it's registered
        layouts = layout.get_layouts()
        layout_names = layout.layout_names()
        
        qlab_registered = 'QLab_Layout' in layout_names
        
        print(f"✓ Found {len(layouts)} registered layouts")
        print(f"✓ QLab Layout registered: {qlab_registered}")
        
        if qlab_registered:
            qlab_layout = layout.get_layout('QLab_Layout')
            print(f"✓ QLab Layout class: {qlab_layout.__name__}")
            print(f"✓ QLab Layout description: {qlab_layout.Description}")
        
        return qlab_registered
        
    except Exception as e:
        print(f"✗ Layout registration test failed: {e}")
        return False

def create_demo_session():
    """Create a demo session file to test with"""
    print("\n📄 Creating demo session...")
    
    try:
        import json
        
        demo_session = {
            "meta": {
                "version": "0.6.5",
                "plugins": {}
            },
            "session": {
                "layout_type": "QLab_Layout",
                "name": "Video Demo Session"
            },
            "cues": []
        }
        
        demo_path = "/tmp/video_demo_session.lsp"
        with open(demo_path, 'w') as f:
            json.dump(demo_session, f, indent=2)
            
        print(f"✓ Demo session created: {demo_path}")
        return demo_path
        
    except Exception as e:
        print(f"✗ Demo session creation failed: {e}")
        return None

def main():
    """Run all final tests"""
    print("Starting final comprehensive tests...\n")
    
    tests = [
        ("Application Startup", test_application_startup),
        ("Video Cue Creation", test_video_cue_creation),
        ("GStreamer Backend", test_gstreamer_backend),
        ("Layout Registration", test_layout_registration),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🔍 Running: {name}")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test {name} crashed: {e}")
            results.append((name, False))
    
    # Create demo session
    demo_path = create_demo_session()
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 🎊 CONGRATULAZIONI! 🎊 🎉")
        print("\nLinux Show Player è stato migliorato con successo!")
        print("\n📋 CARATTERISTICHE AGGIUNTE:")
        print("   ✨ Supporto video completo")
        print("   🎨 Interfaccia moderna stile QLab") 
        print("   🎛️ Controlli video avanzati")
        print("   📺 Gestione multi-display")
        print("   🔧 Backend GStreamer esteso")
        
        print("\n🚀 COME PROCEDERE:")
        print("   1. Avvia l'applicazione:")
        print("      cd /home/nto/linux-show-player-master")
        print("      python3 -m lisp.main")
        print("   2. Seleziona 'QLab Style Layout'")
        print("   3. Crea video cue dal menu File")
        print("   4. Divertiti con le nuove funzionalità!")
        
        if demo_path:
            print(f"\n📂 Sessione demo creata in: {demo_path}")
            
        print(f"\n📖 Leggi il README completo: README_VIDEO_IMPROVEMENTS.md")
    else:
        print(f"\n⚠️ {total - passed} test(s) falliti.")
        print("Controlla gli errori sopra prima di procedere.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    sys.exit(0 if success else 1)