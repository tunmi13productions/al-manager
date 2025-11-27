#!/usr/bin/env python3
"""
3D Audio Positioning Example
============================

Demonstrates 3D positional audio capabilities including:
- Sound source positioning
- Listener positioning and movement
- Distance-based volume attenuation
- Doppler effects
"""

import time
import math
from al_manager.manager import Manager


def main():
    print("AL Manager - 3D Audio Positioning Example")
    print("=" * 45)
    
    manager = Manager()
    print("✓ Audio manager created")
    
    # 1. Basic positioning
    print("\n1. Basic 3D positioning...")
    
    # Place sounds at different positions
    positions = [
        (0, 0, 0, "Center"),
        (5, 0, 0, "Right"),
        (-5, 0, 0, "Left"), 
        (0, 5, 0, "Front"),
        (0, -5, 0, "Back"),
        (0, 0, 5, "Above"),
        (0, 0, -5, "Below")
    ]
    
    sounds = []
    for x, y, z, description in positions:
        sound = manager.play_p("test.ogg", x=x, y=y, z=z, volume=0.6, looping=True)
        if sound:
            sounds.append(sound)
            print(f"  Sound at {description}: ({x}, {y}, {z})")
    
    print(f"✓ Playing {len(sounds)} positioned sounds")
    time.sleep(4)
    
    # Stop positioned sounds
    for sound in sounds:
        sound.stop()
    
    # 2. Moving sound source
    print("\n2. Moving sound source in a circle...")
    
    moving_sound = manager.play_p("test.ogg", x=5, y=0, z=0, volume=0.8, looping=True)
    if moving_sound:
        print("✓ Moving sound in a circle around the listener")
        
        # Move in a circle for 8 seconds
        radius = 8
        for i in range(80):  # 80 steps over 8 seconds
            angle = (i / 80) * 2 * math.pi
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = 0
            
            moving_sound.set_position(x, y, z)
            print(f"\r  Position: ({x:.1f}, {y:.1f}, {z:.1f})", end="", flush=True)
            time.sleep(0.1)
        
        print("\n✓ Circular movement completed")
        moving_sound.stop()
    
    # 3. Listener movement
    print("\n3. Moving listener position...")
    
    static_sound = manager.play_p("test.ogg", x=10, y=0, z=0, volume=0.8, looping=True)
    if static_sound:
        print("✓ Sound fixed at (10, 0, 0), moving listener")
        
        # Move listener towards and away from sound
        positions_sequence = [
            (0, 0, 0, "Starting at origin"),
            (5, 0, 0, "Moving closer"),
            (8, 0, 0, "Very close"),
            (15, 0, 0, "Moving away"),
            (20, 0, 0, "Far away"),
            (0, 0, 0, "Back to origin")
        ]
        
        for x, y, z, description in positions_sequence:
            manager.update(x, y, z)
            print(f"  {description}: ({x}, {y}, {z})")
            time.sleep(2)
        
        print("✓ Listener movement completed")
        static_sound.stop()
    
    # 4. Distance attenuation demonstration
    print("\n4. Distance attenuation demonstration...")
    
    # Create sound with custom distance parameters
    distant_sound = manager.play_p("test.ogg", 
                                  x=0, y=0, z=0, 
                                  volume=1.0, 
                                  looping=True,
                                  max_distance=15.0,
                                  reference_distance=2.0,
                                  rolloff_factor=1.5)
    
    if distant_sound:
        print("✓ Sound with custom distance parameters")
        print(f"  Max distance: {distant_sound.max_distance}")
        print(f"  Reference distance: {distant_sound.reference_distance}")
        print(f"  Rolloff factor: {distant_sound.rolloff_factor}")
        
        # Move listener to different distances
        test_distances = [1, 2, 5, 10, 15, 20]
        
        for distance in test_distances:
            manager.update(distance, 0, 0)
            print(f"  At distance {distance}: volume should be {'audible' if distance <= 15 else 'silent'}")
            time.sleep(2)
        
        # Reset listener position
        manager.update(0, 0, 0)
        print("✓ Distance attenuation demo completed")
        distant_sound.stop()
    
    # 5. Multiple moving sources
    print("\n5. Multiple moving sound sources...")
    
    # Create multiple sounds moving in different patterns
    orbit_sounds = []
    for i in range(3):
        sound = manager.play_p("test.ogg", x=5, y=0, z=0, volume=0.5, looping=True)
        if sound:
            orbit_sounds.append((sound, i))
    
    if orbit_sounds:
        print(f"✓ {len(orbit_sounds)} sounds orbiting at different speeds")
        
        for step in range(60):  # 6 seconds
            for sound, sound_id in orbit_sounds:
                # Different orbit radius and speed for each sound
                radius = 6 + sound_id * 2
                speed = 1 + sound_id * 0.5
                angle = (step * speed / 60) * 2 * math.pi
                
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                z = sound_id  # Different heights
                
                sound.set_position(x, y, z)
            
            time.sleep(0.1)
        
        print("\n✓ Multiple orbit demo completed")
        for sound, _ in orbit_sounds:
            sound.stop()
    
    # 6. Height demonstration (Z-axis)
    print("\n6. Height/elevation demonstration...")
    
    height_sound = manager.play_p("test.ogg", x=0, y=5, z=0, volume=0.8, looping=True)
    if height_sound:
        print("✓ Sound moving vertically")
        
        # Move sound up and down
        for height in range(-10, 11, 2):
            height_sound.set_position(0, 5, height)
            print(f"  Height: {height}")
            time.sleep(0.8)
        
        print("✓ Vertical movement completed")
        height_sound.stop()
    
    # Cleanup
    manager.destroy_all()
    print("\n✓ All sounds cleaned up")
    print("3D positioning example completed!")
    
    print("\nTips for 3D audio:")
    print("- Use headphones for best positional audio experience")
    print("- Reference distance is where volume = 1.0")
    print("- Sounds beyond max_distance become silent")
    print("- Higher rolloff_factor = faster volume decrease with distance")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. An audio file named 'test.ogg' in the current directory")
        print("2. OpenAL drivers installed")
        print("3. Headphones or good speakers for spatial audio")
        print("4. All required dependencies: pip install -r requirements.txt")