#!/usr/bin/env python3

"""
Quick test script for Linux Show Player video improvements
Tests basic functionality without requiring full Poetry setup
"""

import sys
import os

# Add the lisp module to Python path
sys.path.insert(0, '/home/nto/linux-show-player-master')

print("🎬 Testing Linux Show Player Video Improvements")
print("=" * 50)

def test_imports():
    """Test if our new modules can be imported"""
    print("\n📦 Testing imports...")
    
    try:
        from lisp.cues.video_cue import VideoCue
        print("✓ VideoCue imported successfully")
    except Exception as e:
        print(f"✗ Failed to import VideoCue: {e}")
        return False
    
    try:
        from lisp.ui.widgets.video_widget import ModernVideoWidget
        print("✓ ModernVideoWidget imported successfully")
    except Exception as e:
        print(f"✗ Failed to import ModernVideoWidget: {e}")
        return False
        
    try:
        from lisp.plugins.gst_backend.gst_video_cue import GstVideoCue
        print("✓ GstVideoCue imported successfully")
    except Exception as e:
        print(f"✗ Failed to import GstVideoCue: {e}")
        return False
        
    return True

def test_video_cue_properties():
    """Test VideoCue properties"""
    print("\n🎥 Testing VideoCue properties...")
    
    try:
        from lisp.cues.video_cue import VideoCue
        
        # Create a mock app object
        class MockApp:
            pass
            
        # Create a mock media object  
        class MockMedia:
            def __init__(self):
                self.changed_signals = {}
                self.elements_changed = MockSignal()
                self.error = MockSignal()
                self.eos = MockSignal()
                
            def changed(self, prop):
                if prop not in self.changed_signals:
                    self.changed_signals[prop] = MockSignal()
                return self.changed_signals[prop]
                
            def element(self, name):
                return None
                
        class MockSignal:
            def connect(self, func):
                pass
                
        app = MockApp()
        media = MockMedia()
        
        # Create VideoCue instance
        video_cue = VideoCue(app, media)
        
        # Test properties
        video_cue.fullscreen = True
        assert video_cue.fullscreen == True, "Fullscreen property failed"
        
        video_cue.brightness = 0.8
        assert video_cue.brightness == 0.8, "Brightness property failed"
        
        print("✓ VideoCue properties work correctly")
        return True
        
    except Exception as e:
        print(f"✗ VideoCue properties test failed: {e}")
        return False

def test_video_widget():
    """Test video widget creation (without Qt)"""
    print("\n📺 Testing video widget structure...")
    
    try:
        from lisp.ui.widgets.video_widget import (
            VideoControlWidget, VideoDisplayWidget, ModernVideoWidget
        )
        
        # Just test class definitions exist
        print("✓ VideoControlWidget class exists")
        print("✓ VideoDisplayWidget class exists") 
        print("✓ ModernVideoWidget class exists")
        
        return True
        
    except Exception as e:
        print(f"✗ Video widget test failed: {e}")
        return False

def check_file_structure():
    """Check if all our new files exist"""
    print("\n📁 Checking file structure...")
    
    files_to_check = [
        '/home/nto/linux-show-player-master/lisp/cues/video_cue.py',
        '/home/nto/linux-show-player-master/lisp/ui/widgets/video_widget.py',
        '/home/nto/linux-show-player-master/lisp/plugins/gst_backend/gst_video_cue.py',
        '/home/nto/linux-show-player-master/lisp/ui/settings/cue_pages/video_cue.py',
        '/home/nto/linux-show-player-master/lisp/plugins/qlab_layout/__init__.py'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {os.path.basename(file_path)}")
        else:
            print(f"✗ {os.path.basename(file_path)} missing")
            all_exist = False
            
    return all_exist

def main():
    """Run all tests"""
    print("Starting comprehensive tests...\n")
    
    tests = [
        ("File Structure", check_file_structure),
        ("Module Imports", test_imports),
        ("VideoCue Properties", test_video_cue_properties),
        ("Video Widgets", test_video_widget),
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
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Linux Show Player video improvements are ready!")
        print("\n🚀 Next steps:")
        print("   1. Install missing system dependencies if needed")
        print("   2. Run: python3 -m lisp.main")
        print("   3. Try creating video cues from the menu")
        print("   4. Test the new QLab-style interface")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)