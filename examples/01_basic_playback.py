#!/usr/bin/env python3
"""
Basic Audio Playback Example
============================

Demonstrates the simplest usage of AL Manager for playing audio files.
This example shows both direct (non-positional) and 3D positioned audio.
"""

import time
from al_manager.manager import Manager


def main():
    print("AL Manager - Basic Playback Example")
    print("=" * 40)
    
    # Create the audio manager
    manager = Manager()
    print("✓ Audio manager created")
    
    # Play a simple sound (direct/non-positional)
    print("\n1. Playing direct sound...")
    sound1 = manager.play("test.ogg", volume=0.8, looping=True)
    
    if sound1:
        print(f"✓ Playing: {sound1.filename}")
        print(f"  Volume: {sound1.volume}")
        print(f"  Direct: {sound1.direct}")
        time.sleep(3)
        
        # Adjust volume while playing
        print("  Adjusting volume to 0.5...")
        sound1.hd.volume = 0.5
        time.sleep(2)
        
        # Stop the sound
        sound1.stop()
        print("✓ Sound stopped")
    
    # Play a positioned sound in 3D space
    print("\n2. Playing positioned sound...")
    sound2 = manager.play_p("test.ogg", x=5, y=0, z=2, volume=0.7, looping=False)
    
    if sound2:
        print(f"✓ Playing positioned sound at ({sound2.x}, {sound2.y}, {sound2.z})")
        time.sleep(2)
        
        # Move the sound while playing
        print("  Moving sound to (10, 5, 0)...")
        sound2.set_position(10, 5, 0)
        time.sleep(2)
        
        # Wait for it to finish or stop it manually
        sound2.stop()
        print("✓ Positioned sound stopped")
    
    # Play multiple sounds at once
    print("\n3. Playing multiple sounds simultaneously...")
    sounds = []
    
    # Create sounds at different positions
    positions = [(0, 0, 0), (5, 0, 0), (-5, 0, 0), (0, 5, 0)]
    for i, (x, y, z) in enumerate(positions):
        sound = manager.play_p("test.ogg", x=x, y=y, z=z, volume=0.5, looping=True)
        if sound:
            sounds.append(sound)
            print(f"  Sound {i+1} at position ({x}, {y}, {z})")
    
    print(f"✓ Playing {len(sounds)} sounds simultaneously")
    time.sleep(4)
    
    # Stop all sounds
    for i, sound in enumerate(sounds):
        sound.stop()
        print(f"  Stopped sound {i+1}")
    
    # Cleanup
    manager.destroy_all()
    print("\n✓ All sounds cleaned up")
    print("Example completed!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. An audio file named 'test.ogg' in the current directory")
        print("2. OpenAL drivers installed")
        print("3. All required dependencies: pip install -r requirements.txt")