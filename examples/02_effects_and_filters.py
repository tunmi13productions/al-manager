#!/usr/bin/env python3
"""
Audio Effects and Filters Example
=================================

Demonstrates how to apply various audio effects and filters to sounds.
Shows both individual effect application and using preset configurations.
"""

import time
from al_manager.manager import Manager


def main():
    print("AL Manager - Effects and Filters Example")
    print("=" * 45)
    
    manager = Manager()
    print("✓ Audio manager created")
    
    # 1. Basic effect application
    print("\n1. Applying individual effects...")
    
    sound1 = manager.play("test.ogg", volume=0.8, looping=True)
    if sound1:
        print("✓ Base sound playing")
        time.sleep(2)
        
        # Add reverb effect
        print("  Adding reverb (hall preset)...")
        sound1.hd.add_effect('reverb', preset='hall')
        time.sleep(3)
        
        # Add distortion
        print("  Adding distortion...")
        sound1.hd.add_effect('distortion', edge=0.3, gain=0.1)
        time.sleep(3)
        
        # Add echo
        print("  Adding echo...")
        sound1.hd.add_effect('echo', delay=0.1, feedback=0.5)
        time.sleep(3)
        
        sound1.stop()
        print("✓ Effects demo completed")
    
    # 2. Filter application
    print("\n2. Applying audio filters...")
    
    sound2 = manager.play("test.ogg", volume=0.8, looping=True)
    if sound2:
        print("✓ Base sound playing")
        time.sleep(2)
        
        # Low-pass filter (muffled sound)
        print("  Applying low-pass filter...")
        sound2.hd.add_filter('lowpass', gain=1.0, gainhf=0.3)
        time.sleep(3)
        
        # Remove filters and add high-pass
        sound2.hd.remove_all_filters()
        print("  Applying high-pass filter...")
        sound2.hd.add_filter('highpass', gain=1.0, gainlf=0.3)
        time.sleep(3)
        
        sound2.stop()
        print("✓ Filter demo completed")
    
    # 3. Filter presets
    print("\n3. Using filter presets...")
    
    presets_to_demo = ['underwater', 'radio', 'telephone', 'muffled']
    
    for preset in presets_to_demo:
        print(f"  Applying '{preset}' preset...")
        sound = manager.play("test.ogg", volume=0.8, looping=True)
        if sound:
            sound.hd.apply_filter_preset(preset)
            time.sleep(3)
            sound.stop()
    
    print("✓ Filter presets demo completed")
    
    # 4. Multiple effects at once
    print("\n4. Combining multiple effects...")
    
    sound3 = manager.play_with_effects(
        "test.ogg",
        effects=[
            {'type': 'reverb', 'preset': 'cathedral'},
            {'type': 'chorus', 'rate': 1.2, 'depth': 0.15, 'feedback': 0.25}
        ],
        filters=[
            {'type': 'lowpass', 'gain': 1.0, 'gainhf': 0.8}
        ],
        volume=0.8,
        looping=True
    )
    
    if sound3:
        print("✓ Playing with cathedral reverb + chorus + low-pass filter")
        time.sleep(5)
        
        # Show effect/filter counts
        print(f"  Effects applied: {sound3.hd.get_effect_count()}")
        print(f"  Filters applied: {sound3.hd.get_filter_count()}")
        
        sound3.stop()
    
    # 5. Real-time effect modification
    print("\n5. Real-time effect parameter changes...")
    
    sound4 = manager.play("test.ogg", volume=0.8, looping=True)
    if sound4:
        # Add equalizer
        sound4.hd.add_effect('equalizer', 
                            low_gain=1.0, 
                            mid1_gain=2.0,  # Boost mids
                            high_gain=0.5)  # Reduce highs
        
        print("✓ Equalizer applied (boosted mids, reduced highs)")
        time.sleep(3)
        
        # Remove all effects and add auto-wah
        sound4.hd.remove_all_effects()
        sound4.hd.add_effect('autowah', attack_time=0.06, release_time=0.06, resonance=2000)
        
        print("✓ Auto-wah effect applied")
        time.sleep(4)
        
        sound4.stop()
    
    # 6. Available effects and filters
    print("\n6. Available effects and filters:")
    
    available_effects = manager.get_available_effects()
    available_filters = manager.get_available_filters()
    
    print(f"  Available effects: {', '.join(available_effects)}")
    print(f"  Available filters: {', '.join(available_filters)}")
    
    reverb_presets = manager.get_reverb_presets()
    filter_presets = manager.get_filter_presets()
    
    print(f"  Reverb presets: {', '.join(reverb_presets)}")
    print(f"  Filter presets: {', '.join(filter_presets)}")
    
    # Cleanup
    manager.destroy_all()
    print("\n✓ All sounds cleaned up")
    print("Effects and filters example completed!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. An audio file named 'test.ogg' in the current directory")
        print("2. OpenAL drivers with EFX extension support")
        print("3. All required dependencies: pip install -r requirements.txt")
        print("\nNote: Some effects might not work if your audio drivers don't support EFX.")