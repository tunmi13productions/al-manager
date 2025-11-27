#!/usr/bin/env python3
"""
Lazy Effects and Environmental Presets Example
==============================================

Demonstrates the lazy effects system - pre-configured effect combinations
with descriptive names for rapid prototyping and easy audio design.
No need to fiddle with complex parameters!
"""

import time
from al_manager.manager import Manager
from al_manager.lazy_effects import LAZY_REVERBS, LAZY_FILTERS, LAZY_COMBOS


def demo_lazy_reverbs(manager):
    """Demonstrate lazy reverb presets."""
    print("\n--- LAZY REVERB PRESETS ---")
    
    reverb_demos = [
        ("bathroom", "Small, tiled space"),
        ("garage", "Medium concrete space"),
        ("stadium", "Large outdoor arena"),
        ("cathedral", "Massive stone building"),
        ("underwater", "Submerged environment"),
        ("classroom", "Educational space"),
        ("gym", "Large indoor sports area")
    ]
    
    for preset_name, description in reverb_demos:
        if preset_name in LAZY_REVERBS:
            print(f"\n  Playing with '{preset_name}' reverb ({description})...")
            
            sound = manager.play("test.ogg", 
                               effects=LAZY_REVERBS[preset_name],
                               volume=0.8, 
                               looping=True)
            
            if sound:
                time.sleep(3)
                sound.stop()
                print(f"  ✓ {preset_name} demo completed")
            else:
                print(f"  ✗ Failed to play {preset_name}")
    
    print("\n✓ Lazy reverb presets demonstration completed")


def demo_lazy_filters(manager):
    """Demonstrate lazy filter presets."""
    print("\n--- LAZY FILTER PRESETS ---")
    
    filter_demos = [
        ("walkie_talkie", "Classic radio communication"),
        ("robot", "Mechanical/synthetic voice"),
        ("old_tv", "Vintage television speaker"),
        ("through_wall", "Muffled, distant sound"),
        ("car", "Sound from inside vehicle")
    ]
    
    for preset_name, description in filter_demos:
        if preset_name in LAZY_FILTERS:
            print(f"\n  Playing with '{preset_name}' filter ({description})...")
            
            sound = manager.play("test.ogg",
                               filters=LAZY_FILTERS[preset_name],
                               volume=0.8,
                               looping=True)
            
            if sound:
                time.sleep(3)
                sound.stop()
                print(f"  ✓ {preset_name} demo completed")
            else:
                print(f"  ✗ Failed to play {preset_name}")
    
    print("\n✓ Lazy filter presets demonstration completed")


def demo_lazy_combos(manager):
    """Demonstrate crazy effect combinations."""
    print("\n--- LAZY EFFECT COMBINATIONS ---")
    print("These are wild combinations of effects and filters!")
    
    combo_demos = [
        ("drunk", "Wobbly, disorienting audio"),
        ("ghost", "Ethereal, haunting presence"),
        ("robot_malfunction", "Glitchy mechanical breakdown"),
        ("time_warp", "Reality-bending distortion"),
        ("psychedelic", "Mind-altering experience"),
        ("nightmare", "Disturbing, unsettling atmosphere"),
        ("crystal_cave", "Mystical underground chamber")
    ]
    
    for preset_name, description in combo_demos:
        if preset_name in LAZY_COMBOS:
            combo = LAZY_COMBOS[preset_name]
            print(f"\n  Playing '{preset_name}' combo ({description})...")
            
            # Extract effects and filters from combo
            effects = combo.get("effects", None)
            filters = combo.get("filters", None)
            
            sound = manager.play("test.ogg",
                               effects=effects,
                               filters=filters,
                               volume=0.8,
                               looping=True)
            
            if sound:
                time.sleep(4)  # Longer for complex combinations
                sound.stop()
                print(f"  ✓ {preset_name} combo completed")
            else:
                print(f"  ✗ Failed to play {preset_name}")
    
    print("\n✓ Lazy combination presets demonstration completed")


def demo_environmental_scenarios(manager):
    """Demonstrate environmental audio scenarios."""
    print("\n--- ENVIRONMENTAL SCENARIOS ---")
    
    scenarios = [
        {
            "name": "Underwater Exploration",
            "sounds": [
                ("breathing", {"effects": LAZY_REVERBS["underwater"], "filters": LAZY_FILTERS.get("underwater_muffled", [])}),
                ("ambient", {"effects": LAZY_REVERBS["underwater"], "volume": 0.4})
            ]
        },
        {
            "name": "Space Station",
            "sounds": [
                ("communication", {"filters": LAZY_FILTERS["robot"], "volume": 0.6}),
                ("ambience", {"effects": LAZY_REVERBS.get("spaceship", []), "volume": 0.3})
            ]
        },
        {
            "name": "Haunted Cathedral",
            "sounds": [
                ("footsteps", {"effects": LAZY_REVERBS["cathedral"], "volume": 0.7}),
                ("whispers", {"effects": LAZY_COMBOS["ghost"]["effects"], "filters": LAZY_COMBOS["ghost"]["filters"], "volume": 0.4})
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n  Scenario: {scenario['name']}")
        
        active_sounds = []
        
        for sound_desc, params in scenario["sounds"]:
            print(f"    Starting {sound_desc} layer...")
            
            sound = manager.play("test.ogg",
                               effects=params.get("effects"),
                               filters=params.get("filters"),
                               volume=params.get("volume", 0.8),
                               looping=True)
            
            if sound:
                active_sounds.append(sound)
                time.sleep(1)  # Stagger the sound starts
        
        if active_sounds:
            print(f"    ✓ Playing {len(active_sounds)} layered sounds...")
            time.sleep(5)
            
            # Stop all sounds in this scenario
            for sound in active_sounds:
                sound.stop()
            
            print(f"    ✓ {scenario['name']} scenario completed")
    
    print("\n✓ Environmental scenarios demonstration completed")


def demo_positioned_lazy_effects(manager):
    """Demonstrate lazy effects with 3D positioning."""
    print("\n--- LAZY EFFECTS WITH 3D POSITIONING ---")
    
    positioned_effects = [
        ("bathroom", (-5, 0, 0), "Left bathroom"),
        ("garage", (5, 0, 0), "Right garage"),
        ("stadium", (0, 10, 0), "Front stadium"),
        ("underwater", (0, 0, -3), "Below water")
    ]
    
    sounds = []
    
    print("  Creating positioned sounds with different lazy effects...")
    
    for effect_name, (x, y, z), description in positioned_effects:
        if effect_name in LAZY_REVERBS:
            sound = manager.play_p("test.ogg",
                                 x=x, y=y, z=z,
                                 effects=LAZY_REVERBS[effect_name],
                                 volume=0.6,
                                 looping=True)
            
            if sound:
                sounds.append(sound)
                print(f"    {description} at ({x}, {y}, {z}) with {effect_name} effect")
    
    if sounds:
        print(f"\n  ✓ Playing {len(sounds)} positioned sounds with different environments")
        print("  Move your head/headphones to hear the spatial differences!")
        time.sleep(8)
        
        for sound in sounds:
            sound.stop()
    
    print("\n✓ Positioned lazy effects demonstration completed")


def main():
    print("AL Manager - Lazy Effects and Environmental Presets")
    print("=" * 55)
    print("For developers who want great audio without the hassle!")
    
    manager = Manager()
    print("✓ Audio manager created")
    
    # Demonstrate different categories of lazy effects
    demo_lazy_reverbs(manager)
    demo_lazy_filters(manager)
    demo_lazy_combos(manager)
    demo_environmental_scenarios(manager)
    demo_positioned_lazy_effects(manager)
    
    # Show available presets
    print("\n--- AVAILABLE LAZY PRESETS ---")
    
    print(f"Reverb presets ({len(LAZY_REVERBS)}):")
    print(f"  {', '.join(LAZY_REVERBS.keys())}")
    
    print(f"\nFilter presets ({len(LAZY_FILTERS)}):")
    print(f"  {', '.join(LAZY_FILTERS.keys())}")
    
    print(f"\nCombo presets ({len(LAZY_COMBOS)}):")
    print(f"  {', '.join(LAZY_COMBOS.keys())}")
    
    # Cleanup
    manager.destroy_all()
    print("\n✓ All sounds cleaned up")
    print("Lazy effects demonstration completed!")
    
    print("\nLazy Effects Philosophy:")
    print("🔧 'bathroom' is easier to remember than reverb parameters")
    print("🎭 'robot' filter vs configuring bandpass frequencies")  
    print("🚀 'psychedelic' combo for instant weirdness")
    print("⚡ Perfect for rapid prototyping and creative experiments")
    print("\nJust import and use - no audio engineering degree required!")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure the lazy_effects module exists in al_manager/")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. An audio file named 'test.ogg' in the current directory")
        print("2. OpenAL drivers with EFX extension support")
        print("3. All required dependencies: pip install -r requirements.txt")
        print("4. Headphones for best spatial audio experience")