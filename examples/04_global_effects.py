#!/usr/bin/env python3
"""
Global Effects and Environmental Audio Example
==============================================

Demonstrates global effects management, which allows you to:
- Create reusable effect configurations
- Apply the same effect to multiple sounds efficiently
- Simulate environmental acoustics
- Manage complex audio scenes
"""

import time
from al_manager.manager import Manager


def main():
    print("AL Manager - Global Effects Example")
    print("=" * 40)
    
    manager = Manager()
    print("✓ Audio manager created")
    
    # 1. Creating global effects
    print("\n1. Creating global effects...")
    
    # Create some global effect configurations
    global_effects = [
        ("cave_reverb", "reverb", {"preset": "cave"}),
        ("hall_reverb", "reverb", {"preset": "hall"}),
        ("subtle_chorus", "chorus", {"rate": 0.8, "depth": 0.1, "feedback": 0.2}),
        ("heavy_distortion", "distortion", {"edge": 0.5, "gain": 0.2})
    ]
    
    for name, effect_type, params in global_effects:
        manager.create_global_effect(name, effect_type, **params)
        print(f"  Created global effect: {name}")
    
    # Create global filters
    global_filters = [
        ("underwater_filter", "lowpass", {"gain": 1.0, "gainhf": 0.3}),
        ("radio_filter", "bandpass", {"gain": 1.0, "gainlf": 0.3, "gainhf": 0.7})
    ]
    
    for name, filter_type, params in global_filters:
        manager.create_global_filter(name, filter_type, **params)
        print(f"  Created global filter: {name}")
    
    print("✓ Global effects and filters created")
    
    # 2. Applying global effects to individual sounds
    print("\n2. Applying global effects to sounds...")
    
    # Play several sounds
    sounds = []
    positions = [(0, 0, 0), (5, 0, 0), (-5, 0, 0), (0, 5, 0)]
    
    for i, (x, y, z) in enumerate(positions):
        sound = manager.play_p("test.ogg", x=x, y=y, z=z, volume=0.6, looping=True)
        if sound:
            sounds.append(sound)
            print(f"  Sound {i+1} at ({x}, {y}, {z})")
    
    if sounds:
        print("✓ Multiple sounds playing")
        time.sleep(2)
        
        # Apply cave reverb to first sound
        print("  Applying cave reverb to sound 1...")
        manager.apply_global_effect_to_sound(sounds[0], "cave_reverb")
        time.sleep(3)
        
        # Apply chorus to second sound
        print("  Applying chorus to sound 2...")
        manager.apply_global_effect_to_sound(sounds[1], "subtle_chorus")
        time.sleep(3)
        
        # Apply multiple effects to third sound
        print("  Applying multiple effects to sound 3...")
        manager.apply_global_effect_to_sound(sounds[2], "hall_reverb")
        manager.apply_global_filter_to_sound(sounds[2], "underwater_filter")
        time.sleep(3)
        
        # Stop all sounds
        for sound in sounds:
            sound.stop()
    
    # 3. Room acoustics simulation
    print("\n3. Room acoustics simulation...")
    
    # Create a scene with multiple sounds
    scene_sounds = []
    sound_positions = [
        (0, 0, 0, "Center speaker"),
        (8, 0, 2, "Right wall speaker"),
        (-8, 0, 2, "Left wall speaker"),
        (0, 10, 1, "Front speaker")
    ]
    
    for x, y, z, description in sound_positions:
        sound = manager.play_p("test.ogg", x=x, y=y, z=z, volume=0.5, looping=True)
        if sound:
            scene_sounds.append(sound)
            print(f"  {description} at ({x}, {y}, {z})")
    
    if scene_sounds:
        print(f"✓ Audio scene with {len(scene_sounds)} speakers created")
        time.sleep(2)
        
        # Simulate different room types
        room_types = ["auditorium", "large_hall", "cathedral"]
        
        for room_type in room_types:
            print(f"  Simulating {room_type} acoustics...")
            manager.apply_room_acoustics(room_type)
            time.sleep(4)
        
        # Reset to no room acoustics
        print("  Removing room acoustics...")
        # Note: You might need to manually remove effects or recreate sounds
        # depending on your implementation
        
        # Stop scene sounds
        for sound in scene_sounds:
            sound.stop()
    
    # 4. Environmental filtering
    print("\n4. Environmental audio filtering...")
    
    # Create environmental sounds
    env_sounds = []
    for i in range(3):
        sound = manager.play_p("test.ogg", x=i*3, y=0, z=0, volume=0.7, looping=True)
        if sound:
            env_sounds.append(sound)
    
    if env_sounds:
        print(f"✓ {len(env_sounds)} environmental sounds created")
        time.sleep(2)
        
        # Apply different environmental filters
        environments = ["underwater", "radio", "muffled"]
        
        for env in environments:
            print(f"  Applying {env} environment...")
            manager.apply_environmental_filter(env)
            time.sleep(3)
        
        # Stop environmental sounds
        for sound in env_sounds:
            sound.stop()
    
    # 5. Complex audio scene with mixed effects
    print("\n5. Complex audio scene with mixed global effects...")
    
    # Create a complex scene
    complex_sounds = []
    
    # Background ambience with subtle reverb
    bg_sound = manager.play("test.ogg", volume=0.3, looping=True)
    if bg_sound:
        manager.apply_global_effect_to_sound(bg_sound, "hall_reverb")
        complex_sounds.append(("background", bg_sound))
        print("  Background ambience with hall reverb")
    
    # Positioned sound with chorus
    pos_sound = manager.play_p("test.ogg", x=5, y=2, z=1, volume=0.6, looping=True)
    if pos_sound:
        manager.apply_global_effect_to_sound(pos_sound, "subtle_chorus")
        complex_sounds.append(("positioned", pos_sound))
        print("  Positioned sound with chorus")
    
    # Distant sound with underwater filter
    distant_sound = manager.play_p("test.ogg", x=-8, y=5, z=0, volume=0.4, looping=True)
    if distant_sound:
        manager.apply_global_filter_to_sound(distant_sound, "underwater_filter")
        complex_sounds.append(("distant", distant_sound))
        print("  Distant sound with underwater filter")
    
    if complex_sounds:
        print(f"✓ Complex scene with {len(complex_sounds)} elements")
        print("  Listening to mixed environment...")
        time.sleep(8)
        
        # Stop complex scene
        for description, sound in complex_sounds:
            sound.stop()
            print(f"  Stopped {description} sound")
    
    # 6. Performance comparison
    print("\n6. Performance demonstration...")
    print("Global effects are more efficient than individual effects")
    print("when applying the same effect to multiple sounds.")
    
    # Demonstrate efficiency by creating many sounds with the same effect
    print("  Creating 10 sounds with the same global reverb...")
    
    many_sounds = []
    for i in range(10):
        x = (i - 5) * 2  # Spread sounds across X-axis
        sound = manager.play_p("test.ogg", x=x, y=0, z=0, volume=0.3, looping=True)
        if sound:
            # Apply the same global effect to all
            manager.apply_global_effect_to_sound(sound, "cave_reverb")
            many_sounds.append(sound)
    
    if many_sounds:
        print(f"✓ {len(many_sounds)} sounds with shared global effect")
        time.sleep(5)
        
        # Stop all sounds
        for sound in many_sounds:
            sound.stop()
    
    # Cleanup
    manager.destroy_all()
    print("\n✓ All sounds and global effects cleaned up")
    print("Global effects example completed!")
    
    print("\nGlobal Effects Benefits:")
    print("- Efficient: One effect configuration used by multiple sounds")
    print("- Consistent: Same effect parameters across all sounds")
    print("- Flexible: Can be applied/removed dynamically")
    print("- Memory efficient: Shared effect instances")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. An audio file named 'test.ogg' in the current directory")
        print("2. OpenAL drivers with EFX extension support")
        print("3. All required dependencies: pip install -r requirements.txt")
        print("\nNote: Global effects require EFX support in your audio drivers.")