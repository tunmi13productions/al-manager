# AL Manager Examples

This folder contains comprehensive examples demonstrating all features of AL Manager.

## Prerequisites

Before running any examples, make sure you have:

1. **Required dependencies installed:**
   ```bash
   pip install -r requirements.txt
   ```

2. **An audio file named `test.ogg`** in the main project directory
   - Examples expect this file to exist
   - You can use any OGG Vorbis audio file
   - Rename your audio file or modify the examples to use a different filename

3. **OpenAL drivers installed** with EFX extension support for effects

## Examples Overview

### 01_basic_playback.py
**Basic Audio Playback**
- Simple sound playback (direct and positioned)
- Volume and pitch control
- Multiple simultaneous sounds
- Basic sound management

```bash
python examples/01_basic_playback.py
```

### 02_effects_and_filters.py
**Audio Effects and Filters**
- Individual effect application (reverb, distortion, echo, chorus)
- Audio filters (low-pass, high-pass, band-pass)
- Filter presets (underwater, radio, telephone)
- Real-time effect modification
- Multiple effects combinations

```bash
python examples/02_effects_and_filters.py
```

### 03_3d_audio_positioning.py
**3D Audio Positioning**
- Sound source positioning in 3D space
- Listener movement and positioning
- Distance-based volume attenuation
- Moving sound sources (circular patterns, orbits)
- Height/elevation demonstration
- Custom distance parameters

```bash
python examples/03_3d_audio_positioning.py
```

### 04_global_effects.py
**Global Effects and Environmental Audio**
- Creating reusable global effects
- Applying effects to multiple sounds efficiently
- Room acoustics simulation
- Environmental filtering
- Complex audio scene management
- Performance optimization with shared effects

```bash
python examples/04_global_effects.py
```

### 05_lazy_effects_presets.py
**Lazy Effects and Environmental Presets**
- Pre-configured effect combinations with descriptive names
- Reverb presets (bathroom, garage, stadium, cathedral)
- Filter presets (walkie-talkie, robot, old TV)
- Crazy effect combinations (drunk, ghost, psychedelic)
- Environmental scenarios
- Positioned lazy effects

```bash
python examples/05_lazy_effects_presets.py
```

## Interactive Demo

For a visual, interactive experience, try the 3D audio demo:

```bash
python 3d_audio_demo.py
```

**Controls:**
- Arrow keys: Move listener position
- Page Up/Down: Change height
- Space: Cycle through lazy effects
- R: Reset position
- ESC: Exit

## Tips for Best Experience

1. **Use headphones** for spatial audio effects
2. **Adjust volume** appropriately - some effects can be loud
3. **Check EFX support** - run examples to see which effects work on your system
4. **Experiment** - modify the examples to try different parameters
5. **Read the code** - examples are heavily commented for learning

## Troubleshooting

### "File not found" errors
- Make sure `test.ogg` exists in the project root directory
- Or modify examples to use your audio file

### Effects not working
- Check if your audio drivers support OpenAL EFX extension
- Some integrated audio chips have limited EFX support
- Try running examples to see which effects work

### No sound output
- Verify OpenAL drivers are installed
- Check system volume and audio output device
- Ensure no other applications are using exclusive audio access

### Import errors
- Verify AL Manager is properly installed: `pip install -r requirements.txt`
- Check that you're running from the correct directory

## Creating Your Own Examples

Use these examples as templates for your own projects:

```python
from al_manager.manager import Manager

# Basic setup
manager = Manager()

# Your audio code here
sound = manager.play("your_audio.ogg", volume=0.8)

# Always clean up
manager.destroy_all()
```

## More Information

- **Main README**: `../README.md` for project overview
- **Source Code**: `../al_manager/` for implementation details
- **Documentation**: `../docs/` for detailed API reference
- **cyal Library**: [https://github.com/lower-elements/cyal](https://github.com/lower-elements/cyal) (MIT License)