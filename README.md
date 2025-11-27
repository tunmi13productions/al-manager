# AL Manager

Enhanced Python wrapper for OpenAL with comprehensive audio effects and 3D positioning.

## Features

- 3D positional audio with volume, pitch, and looping controls
- Real-time audio effects: reverb, distortion, echo, chorus, equalizer
- Audio filters: low-pass, high-pass, band-pass
- Environmental presets and room acoustics simulation
- Global effect management for multiple sounds

## Installation

```bash
pip install cyal pyogg pydub requests
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from al_manager.manager import Manager

# Basic playback
manager = Manager()
sound = manager.play("audio.ogg", volume=0.8)

# 3D positioned audio
positioned_sound = manager.play_p("audio.ogg", x=5, y=0, z=10)

# Add effects
sound.hd.add_effect('reverb', preset='hall')
sound.hd.add_effect('distortion', edge=0.3, gain=0.1)

# Apply presets
sound.hd.apply_filter_preset('underwater')

manager.destroy_all()
```

## Links

- **cyal on GitHub**: [https://github.com/lower-elements/cyal](https://github.com/lower-elements/cyal) (MIT License)
- **Examples**: See `examples` directory for comprehensive usage examples

## AI Collaboration Notice

While the core AL Manager implementation was originally developed by tunmi13productions, significant enhancements and improvements have been made with assistance from Claude Sonnet (Anthropic). These AI-assisted improvements include documentation, examples, code organization, and feature enhancements.

Although the library has been thoroughly tested and is actively used in projects, users should conduct their own testing to ensure compatibility with their specific use cases. The collaborative nature of development means that while the core functionality is stable, some enhanced features may require additional validation. It is strongly recommended that you put in any issues you may encounter, or if you are good at development, to submit a pull request if you find any features could be improved and/or fixed.

## License

This enhanced wrapper is compatible with cyal (MIT License). See  the `license` file for specific licensing terms.