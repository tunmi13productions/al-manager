# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

"""
Lazy Effects - For Developers Who Don't Want To Think
====================================================

"I just want my sound to sound like [THING]. Don't make me configure reverb parameters!"

This module provides pre-made effect configurations with logical, amusing names.
Perfect for rapid prototyping, lazy developers, or when you just want something 
that sounds decent without diving into the technical details.

Usage:
    from al_manager.lazy_effects import LAZY_REVERBS, LAZY_FILTERS, LAZY_COMBOS
    
    # Apply a "bathroom" reverb 
    manager.play("sound.ogg", effects=LAZY_REVERBS["bathroom"])
    
    # Make it sound like a walkie-talkie
    manager.play("sound.ogg", filters=LAZY_FILTERS["walkie_talkie"])
    
    # Combine both for "bathroom walkie-talkie" (because why not?)
    manager.play("sound.ogg", 
                 effects=LAZY_REVERBS["bathroom"], 
                 filters=LAZY_FILTERS["walkie_talkie"])
"""

# =============================================================================
# REVERB PRESETS - For When You Want Space But Don't Know The Math
# =============================================================================

LAZY_REVERBS = {
    # SMALL SPACES
    "bathroom": [{
        "type": "reverb",
        "preset": "bathroom"  # Uses built-in bathroom preset
    }],
    
    "closet": [{
        "type": "reverb", 
        "density": 0.2,
        "diffusion": 0.4,
        "gain": 0.25,
        "gainhf": 0.9,
        "decay_time": 0.6,
        "decay_hfratio": 1.2,
        "reflections_gain": 0.8,
        "reflections_delay": 0.002,
        "late_reverb_gain": 0.6,
        "late_reverb_delay": 0.005
    }],
    
    "phone_booth": [{
        "type": "reverb",
        "density": 0.3,
        "diffusion": 0.5,
        "gain": 0.28,
        "gainhf": 0.7,
        "decay_time": 0.9,
        "decay_hfratio": 1.1,
        "reflections_gain": 0.6,
        "reflections_delay": 0.003,
        "late_reverb_gain": 0.8,
        "late_reverb_delay": 0.008
    }],
    
    # MEDIUM SPACES
    "classroom": [{
        "type": "reverb",
        "density": 0.7,
        "diffusion": 0.85,
        "gain": 0.3,
        "gainhf": 0.6,
        "decay_time": 2.1,
        "decay_hfratio": 0.7,
        "reflections_gain": 0.2,
        "reflections_delay": 0.012,
        "late_reverb_gain": 1.0,
        "late_reverb_delay": 0.018
    }],
    
    "garage": [{
        "type": "reverb",
        "density": 0.6,
        "diffusion": 0.9,
        "gain": 0.32,
        "gainhf": 0.4,
        "decay_time": 2.8,
        "decay_hfratio": 0.5,
        "reflections_gain": 0.3,
        "reflections_delay": 0.015,
        "late_reverb_gain": 1.1,
        "late_reverb_delay": 0.025
    }],
    
    "gym": [{
        "type": "reverb",
        "density": 0.9,
        "diffusion": 1.0,
        "gain": 0.35,
        "gainhf": 0.3,
        "decay_time": 4.2,
        "decay_hfratio": 0.4,
        "reflections_gain": 0.4,
        "reflections_delay": 0.020,
        "late_reverb_gain": 1.3,
        "late_reverb_delay": 0.030
    }],
    
    # LARGE SPACES
    "cathedral": [{
        "type": "reverb",
        "preset": "cathedral"  # Uses built-in cathedral preset
    }],
    
    "stadium": [{
        "type": "reverb",
        "density": 1.0,
        "diffusion": 1.0,
        "gain": 0.4,
        "gainhf": 0.2,
        "decay_time": 6.8,
        "decay_hfratio": 0.25,
        "reflections_gain": 0.5,
        "reflections_delay": 0.035,
        "late_reverb_gain": 1.5,
        "late_reverb_delay": 0.060
    }],
    
    "airplane_hangar": [{
        "type": "reverb",
        "density": 1.0,
        "diffusion": 0.95,
        "gain": 0.38,
        "gainhf": 0.15,
        "decay_time": 8.5,
        "decay_hfratio": 0.2,
        "reflections_gain": 0.6,
        "reflections_delay": 0.040,
        "late_reverb_gain": 1.8,
        "late_reverb_delay": 0.080
    }],
    
    # SPECIAL ENVIRONMENTS
    "cave": [{
        "type": "reverb",
        "preset": "cave"  # Uses built-in cave preset
    }],
    
    "underwater": [{
        "type": "reverb",
        "density": 0.4,
        "diffusion": 1.0,
        "gain": 0.3,
        "gainhf": 0.1,
        "decay_time": 1.8,
        "decay_hfratio": 0.1,
        "reflections_gain": 0.7,
        "reflections_delay": 0.008,
        "late_reverb_gain": 1.2,
        "late_reverb_delay": 0.030
    }],
    
    "spaceship": [{
        "type": "reverb",
        "density": 0.8,
        "diffusion": 0.9,
        "gain": 0.28,
        "gainhf": 0.6,
        "decay_time": 2.5,
        "decay_hfratio": 0.8,
        "reflections_gain": 0.3,
        "reflections_delay": 0.010,
        "late_reverb_gain": 0.9,
        "late_reverb_delay": 0.020
    }],
    
    "wind_tunnel": [{
        "type": "reverb",
        "density": 0.5,
        "diffusion": 1.0,
        "gain": 0.25,
        "gainhf": 0.3,
        "decay_time": 5.2,
        "decay_hfratio": 0.2,
        "reflections_gain": 0.15,
        "reflections_delay": 0.025,
        "late_reverb_gain": 0.8,
        "late_reverb_delay": 0.045
    }]
}

# =============================================================================
# FILTER PRESETS - For When You Want Character But Hate EQ Curves
# =============================================================================

LAZY_FILTERS = {
    # COMMUNICATION DEVICES
    "walkie_talkie": [{
        "type": "bandpass",
        "gain": 1.0,
        "gainlf": 0.1,
        "gainhf": 0.2
    }],
    
    "phone_call": [{
        "type": "bandpass", 
        "gain": 0.9,
        "gainlf": 0.05,
        "gainhf": 0.1
    }],
    
    "radio": [{
        "type": "bandpass",
        "gain": 0.95,
        "gainlf": 0.15,
        "gainhf": 0.3
    }],
    
    "megaphone": [{
        "type": "bandpass",
        "gain": 1.0,
        "gainlf": 0.2,
        "gainhf": 0.4
    }],
    
    # TRANSPORTATION
    "car": [{
        "type": "lowpass",
        "gain": 0.9,
        "gainhf": 0.6
    }],
    
    "schoolbus": [{
        "type": "lowpass",
        "gain": 0.85,
        "gainhf": 0.4
    }],
    
    "airplane": [{
        "type": "lowpass", 
        "gain": 0.8,
        "gainhf": 0.3
    }],
    
    "motorcycle": [{
        "type": "highpass",
        "gain": 0.95,
        "gainlf": 0.7
    }],
    
    # ENVIRONMENTAL
    "underwater": [{
        "type": "lowpass",
        "gain": 0.8,
        "gainhf": 0.15
    }],
    
    "through_wall": [{
        "type": "lowpass",
        "gain": 0.7,
        "gainhf": 0.25
    }],
    
    "through_glass": [{
        "type": "lowpass",
        "gain": 0.85,
        "gainhf": 0.5
    }],
    
    "in_helmet": [{
        "type": "lowpass",
        "gain": 0.9,
        "gainhf": 0.4
    }],
    
    # VINTAGE/NOSTALGIC
    "old_tv": [{
        "type": "bandpass",
        "gain": 0.8,
        "gainlf": 0.3,
        "gainhf": 0.6
    }],
    
    "gramophone": [{
        "type": "lowpass",
        "gain": 0.7,
        "gainhf": 0.2
    }],
    
    "am_radio": [{
        "type": "bandpass",
        "gain": 0.75,
        "gainlf": 0.1,
        "gainhf": 0.3
    }],
    
    # FANTASY/SCI-FI
    "robot": [{
        "type": "bandpass",
        "gain": 0.9,
        "gainlf": 0.4,
        "gainhf": 0.8
    }],
    
    "alien_voice": [{
        "type": "highpass",
        "gain": 0.8,
        "gainlf": 0.2
    }],
    
    "force_field": [{
        "type": "highpass",
        "gain": 0.9,
        "gainlf": 0.5
    }]
}

# =============================================================================
# COMBO PRESETS - Multiple Effects For Maximum Laziness
# =============================================================================

LAZY_COMBOS = {
    # Combine effects + filters for specific scenarios
    "drunk": {
        "effects": [{
            "type": "chorus",
            "waveform": 1,
            "phase": 45,
            "rate": 0.8,
            "depth": 0.3,
            "feedback": 0.1,
            "delay": 0.01
        }],
        "filters": [{
            "type": "lowpass",
            "gain": 0.9,
            "gainhf": 0.7
        }]
    },
    
    "ghost": {
        "effects": [{
            "type": "echo",
            "delay": 0.15,
            "lrdelay": 0.12,
            "damping": 0.7,
            "feedback": 0.4,
            "spread": 0.5
        }],
        "filters": [{
            "type": "highpass",
            "gain": 0.8,
            "gainlf": 0.3
        }]
    },
    
    "robot_in_tunnel": {
        "effects": LAZY_REVERBS["wind_tunnel"],
        "filters": LAZY_FILTERS["robot"]
    },
    
    "underwater_radio": {
        "effects": LAZY_REVERBS["underwater"], 
        "filters": LAZY_FILTERS["radio"]
    },
    
    "haunted_phone": {
        "effects": [{
            "type": "echo",
            "delay": 0.3,
            "feedback": 0.6,
            "damping": 0.5
        }],
        "filters": LAZY_FILTERS["phone_call"]
    },
    
    "spaceship_intercom": {
        "effects": LAZY_REVERBS["spaceship"],
        "filters": LAZY_FILTERS["megaphone"]
    },
    
    "broken_radio": {
        "effects": [{
            "type": "distortion",
            "edge": 0.4,
            "gain": 0.03,
            "lowpass_cutoff": 6000.0
        }],
        "filters": LAZY_FILTERS["am_radio"]
    },
    
    "alien_cave": {
        "effects": LAZY_REVERBS["cave"],
        "filters": LAZY_FILTERS["alien_voice"]
    },
    
    # NEW CREATIVE COMBOS - Using full parameter ranges!
    "time_warp": {
        "effects": [{
            "type": "pitch_shifter",
            "coarse_tune": -5,  # Lower pitch
            "fine_tune": 25
        }, {
            "type": "flanger",
            "waveform": 0,  # Sinusoid
            "phase": 90,
            "rate": 0.5,
            "depth": 0.8,
            "feedback": 0.3,
            "delay": 0.003
        }]
    },
    
    "robot_malfunction": {
        "effects": [{
            "type": "distortion",
            "edge": 0.6,
            "gain": 0.08,
            "lowpass_cutoff": 4000.0
        }, {
            "type": "chorus",
            "waveform": 1,  # Triangle
            "phase": 180,
            "rate": 3.2,
            "depth": 0.4,
            "feedback": 0.1,
            "delay": 0.01
        }],
        "filters": LAZY_FILTERS["robot"]
    },
    
    "psychedelic": {
        "effects": [{
            "type": "auto_wah",
            "attack_time": 0.2,
            "release_time": 0.8,
            "resonance": 800.0,
            "peak_gain": 15.0
        }, {
            "type": "chorus",
            "waveform": 0,
            "phase": 45,
            "rate": 1.8,
            "depth": 0.6,
            "feedback": 0.4,
            "delay": 0.012
        }]
    },
    
    "nightmare": {
        "effects": [{
            "type": "pitch_shifter",
            "coarse_tune": -12,  # One octave down
            "fine_tune": -50
        }, {
            "type": "echo",
            "delay": 0.25,
            "lrdelay": 0.20,
            "damping": 0.3,
            "feedback": 0.7,
            "spread": 0.8
        }],
        "filters": [{
            "type": "lowpass",
            "gain": 0.8,
            "gainhf": 0.2
        }]
    },
    
    "chipmunk": {
        "effects": [{
            "type": "pitch_shifter",
            "coarse_tune": 12,  # One octave up
            "fine_tune": 0
        }],
        "filters": [{
            "type": "highpass",
            "gain": 1.0,
            "gainlf": 0.6
        }]
    },
    
    "washing_machine": {
        "effects": [{
            "type": "chorus",
            "waveform": 1,
            "phase": 0,
            "rate": 2.5,
            "depth": 0.8,
            "feedback": 0.6,
            "delay": 0.016
        }],
        "filters": [{
            "type": "lowpass",
            "gain": 0.9,
            "gainhf": 0.4
        }]
    },
    
    "crystal_cave": {
        "effects": [{
            "type": "reverb",
            "density": 0.9,
            "diffusion": 1.0,
            "gain": 0.4,
            "gainhf": 0.8,
            "decay_time": 4.5,
            "decay_hfratio": 1.2,
            "reflections_gain": 0.6,
            "reflections_delay": 0.020,
            "late_reverb_gain": 1.4,
            "late_reverb_delay": 0.050
        }, {
            "type": "equalizer",
            "low_gain": 0.8,
            "low_cutoff": 200.0,
            "mid1_gain": 1.2,
            "mid1_center": 800.0,
            "mid1_width": 0.5,
            "mid2_gain": 1.5,
            "mid2_center": 4000.0,
            "mid2_width": 0.3,
            "high_gain": 2.0,
            "high_cutoff": 8000.0
        }]
    }
}

# =============================================================================
# CONVENIENCE FUNCTIONS - Even Lazier Ways To Apply Effects
# =============================================================================

def get_random_reverb():
    """Get a random reverb effect for when you're feeling particularly lazy."""
    import random
    reverb_name = random.choice(list(LAZY_REVERBS.keys()))
    return reverb_name, LAZY_REVERBS[reverb_name]

def get_random_filter():
    """Get a random filter for when you don't even want to choose."""
    import random
    filter_name = random.choice(list(LAZY_FILTERS.keys()))
    return filter_name, LAZY_FILTERS[filter_name]

def get_random_combo():
    """Get a random combination effect. Maximum chaos, minimum effort."""
    import random
    combo_name = random.choice(list(LAZY_COMBOS.keys()))
    return combo_name, LAZY_COMBOS[combo_name]

def apply_lazy_effect(manager, sound_name, effect_name, position=None):
    """
    Apply a lazy effect by name with maximum convenience.
    
    Args:
        manager: AL Manager instance
        sound_name: Name/path of sound file
        effect_name: Name of effect from LAZY_REVERBS, LAZY_FILTERS, or LAZY_COMBOS
        position: Optional (x, y, z) tuple for positioned sound
    
    Returns:
        Sound item or None if failed
    """
    effects = None
    filters = None
    
    # Check each category
    if effect_name in LAZY_REVERBS:
        effects = LAZY_REVERBS[effect_name]
    elif effect_name in LAZY_FILTERS:
        filters = LAZY_FILTERS[effect_name]
    elif effect_name in LAZY_COMBOS:
        combo = LAZY_COMBOS[effect_name]
        effects = combo.get("effects")
        filters = combo.get("filters")
    else:
        print(f"Unknown lazy effect: {effect_name}")
        return None
    
    # Play with appropriate method
    if position:
        x, y, z = position
        return manager.play_p(sound_name, x, y, z, effects=effects, filters=filters)
    else:
        return manager.play(sound_name, effects=effects, filters=filters)

def list_all_effects():
    """Print all available lazy effects for reference."""
    print("LAZY REVERBS:")
    for name in sorted(LAZY_REVERBS.keys()):
        print(f"  - {name}")
    
    print("\nLAZY FILTERS:")
    for name in sorted(LAZY_FILTERS.keys()):
        print(f"  - {name}")
    
    print("\nLAZY COMBOS:")
    for name in sorted(LAZY_COMBOS.keys()):
        print(f"  - {name}")

def search_effects(keyword):
    """Find effects containing a keyword. For when you sort of know what you want."""
    matches = []
    
    # Search reverbs
    for name in LAZY_REVERBS.keys():
        if keyword.lower() in name.lower():
            matches.append(("reverb", name))
    
    # Search filters  
    for name in LAZY_FILTERS.keys():
        if keyword.lower() in name.lower():
            matches.append(("filter", name))
    
    # Search combos
    for name in LAZY_COMBOS.keys():
        if keyword.lower() in name.lower():
            matches.append(("combo", name))
    
    return matches

# =============================================================================
# PRESET CATEGORIES - For Slightly Less Lazy Organization
# =============================================================================

EFFECT_CATEGORIES = {
    "small_spaces": ["bathroom", "closet", "phone_booth"],
    "medium_spaces": ["classroom", "garage", "gym"], 
    "large_spaces": ["cathedral", "stadium", "airplane_hangar"],
    "communication": ["walkie_talkie", "phone_call", "radio", "megaphone"],
    "transportation": ["car", "schoolbus", "airplane", "motorcycle"],
    "vintage": ["old_tv", "gramophone", "am_radio", "broken_radio"],
    "sci_fi": ["robot", "alien_voice", "force_field", "spaceship", "time_warp", "robot_malfunction"],
    "spooky": ["ghost", "haunted_phone", "alien_cave", "nightmare", "crystal_cave"],
    "environmental": ["underwater", "cave", "wind_tunnel", "through_wall"],
    "creative": ["psychedelic", "chipmunk", "washing_machine", "drunk"],
    "character_voices": ["chipmunk", "robot", "alien_voice", "nightmare"],
    "magical": ["crystal_cave", "time_warp", "psychedelic"],
    "broken_tech": ["broken_radio", "robot_malfunction", "old_tv"]
}

def get_category_effects(category):
    """Get all effects in a specific category."""
    if category not in EFFECT_CATEGORIES:
        return None
    
    effects = {}
    for effect_name in EFFECT_CATEGORIES[category]:
        if effect_name in LAZY_REVERBS:
            effects[effect_name] = ("reverb", LAZY_REVERBS[effect_name])
        elif effect_name in LAZY_FILTERS:
            effects[effect_name] = ("filter", LAZY_FILTERS[effect_name])
        elif effect_name in LAZY_COMBOS:
            effects[effect_name] = ("combo", LAZY_COMBOS[effect_name])
    
    return effects

# =============================================================================
# EXAMPLES - Copy-Paste Ready Code
# =============================================================================

"""
USAGE EXAMPLES:

# Basic lazy application
from al_manager.lazy_effects import apply_lazy_effect

manager = Manager()
apply_lazy_effect(manager, "explosion.ogg", "stadium")
apply_lazy_effect(manager, "voice.ogg", "walkie_talkie", position=(10, 0, 0))

# Manual application
from al_manager.lazy_effects import LAZY_REVERBS, LAZY_FILTERS

manager.play("footsteps.ogg", effects=LAZY_REVERBS["garage"])
manager.play_p("radio.ogg", 5, 0, 0, filters=LAZY_FILTERS["old_tv"])

# Random effects for variety
from al_manager.lazy_effects import get_random_reverb

reverb_name, reverb_effect = get_random_reverb()
print(f"Using random reverb: {reverb_name}")
manager.play("ambient.ogg", effects=reverb_effect)

# Browse available effects
from al_manager.lazy_effects import list_all_effects, search_effects

list_all_effects()
matches = search_effects("radio")
print("Radio-related effects:", matches)
"""