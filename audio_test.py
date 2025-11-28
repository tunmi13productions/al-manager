#!/usr/bin/env python3
"""Test script demonstrating the unified Sound class with different audio sources.

This script tests:
1. Loading test.ogg as a regular file
2. Loading test.ogg as streaming audio  
3. Loading http://files.tunmi13.com/stuff/Coconut.wav from URL
4. Legacy class compatibility

Usage:
    python audio_test.py          # Run all tests without audio playback
    python audio_test.py --play   # Run all tests with audio playback
"""

import time
import os
import sys
from al_manager.sound import Sound

def test_audio_loading(enable_playback=False):
    """Test loading different audio sources with the unified Sound class."""
    print("=== AL Manager Unified Sound Class Test ===\n")
    
    if enable_playback:
        print("[AUDIO] Audio playback ENABLED - you will hear sounds during testing")
    else:
        print("[AUDIO] Audio playback DISABLED - tests will run silently")
    print()
    
    # Test 1: Load test.ogg as regular file
    print("Test 1: Loading test.ogg as regular file")
    print("-" * 40)
    
    if os.path.exists("test.ogg"):
        try:
            file_sound = Sound()
            result = file_sound.load("test.ogg")
            
            if result:
                print(f"[PASS] Successfully loaded test.ogg as file")
                print(f"  Sound type: {file_sound._sound_type}")
                print(f"  Is active: {file_sound.is_active}")
                print(f"  Volume: {file_sound.volume}")
                print(f"  Pitch: {file_sound.pitch}")
                
                # Test playback 
                if enable_playback:
                    print("  [PLAY] Playing for 2 seconds...")
                    file_sound.play()
                    time.sleep(2)
                    file_sound.stop()
                    print("  [STOP] Playback stopped")
                
            else:
                print("[FAIL] Failed to load test.ogg as file")
                
            file_sound.close()
            
        except Exception as e:
            print(f"[FAIL] Error loading test.ogg as file: {e}")
    else:
        print("[FAIL] test.ogg file not found")
    
    print()
    
    # Test 2: Load test.ogg as streaming
    print("Test 2: Loading test.ogg as streaming")
    print("-" * 40)
    
    if os.path.exists("test.ogg"):
        try:
            stream_sound = Sound()
            result = stream_sound.load("test.ogg", streaming=True, chunk_size=4096*2, preload_buffers=3)
            
            if result:
                print(f"[PASS] Successfully loaded test.ogg for streaming")
                print(f"  Sound type: {stream_sound._sound_type}")
                print(f"  Is active: {stream_sound.is_active}")
                print(f"  Buffer size: {stream_sound.buffer_size} bytes")
                print(f"  Buffer count: {stream_sound.buffer_count}")
                print(f"  Sample rate: {stream_sound.sample_rate} Hz")
                print(f"  Channels: {stream_sound.channels}")
                if stream_sound.audio_file:
                    print(f"  Duration: {stream_sound.get_duration():.1f} seconds")
                
                # Test streaming playback
                if enable_playback:
                    print("  [STREAM] Starting stream for 3 seconds...")
                    stream_sound.play(loop=False)
                    time.sleep(3)
                    stream_sound.stop()
                    print("  [STOP] Stream stopped")
                
            else:
                print("[FAIL] Failed to load test.ogg for streaming")
                
            stream_sound.close()
            
        except Exception as e:
            print(f"[FAIL] Error loading test.ogg for streaming: {e}")
    else:
        print("[FAIL] test.ogg file not found")
    
    print()
    
    # Test 3: Load URL audio
    print("Test 3: Loading http://files.tunmi13.com/stuff/Coconut.wav from URL")
    print("-" * 60)
    
    try:
        url_sound = Sound()
        print("  Attempting to download and load URL audio...")
        result = url_sound.load("http://files.tunmi13.com/stuff/Coconut.wav", spatial_audio=False)
        
        if result:
            print(f"[PASS] Successfully loaded URL audio")
            print(f"  Sound type: {url_sound._sound_type}")
            print(f"  Is active: {url_sound.is_active}")
            print(f"  Is direct: {url_sound.is_direct}")
            print(f"  Sample rate: {url_sound.sample_rate} Hz")
            print(f"  Format: {url_sound.format}")
            
            # Test URL playback
            if enable_playback:
                print("  [PLAY] Playing URL audio for 3 seconds...")
                url_sound.play()
                time.sleep(3)
                url_sound.stop()
                print("  [STOP] URL playback stopped")
            
        else:
            print("[FAIL] Failed to load URL audio")
            
        url_sound.close()
        
    except Exception as e:
        print(f"[FAIL] Error loading URL audio: {e}")
    
    print()
    
    # Test 4: Test legacy compatibility
    print("Test 4: Testing legacy class compatibility")
    print("-" * 40)
    
    try:
        from al_manager.sound import URLSound, StreamingSound
        
        # Test legacy URLSound
        print("Testing legacy URLSound class:")
        legacy_url = URLSound()
        print(f"  [PASS] URLSound instantiated (should show deprecation warning)")
        legacy_url.close()
        
        # Test legacy StreamingSound  
        print("Testing legacy StreamingSound class:")
        legacy_stream = StreamingSound()
        print(f"  [PASS] StreamingSound instantiated (should show deprecation warning)")
        legacy_stream.close()
        
    except Exception as e:
        print(f"[FAIL] Error testing legacy classes: {e}")
    
    print()
    print("=== Audio Test Complete ===")
    
    if not enable_playback:
        print("\nTo test with audio playback, run: python audio_test.py --play")

if __name__ == "__main__":
    # Check for --play argument
    enable_playback = "--play" in sys.argv
    test_audio_loading(enable_playback)