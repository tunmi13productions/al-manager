# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

# The actual manager itself.
# First import everything from sound.
from .sound import *
from .effects import AudioEffect, AudioFilter, EffectPresets
from .efx_manager import EfxManager
import math


# We will first start off with our manager item, in which things will be controlled.
class ManagerItem:
    # Initialization where user can specify custom parameters.
    def __init__(self, filename, **kwargs):
        # Coords.
        self.x = kwargs.get("x", 0.0)
        self.y = kwargs.get("y", 0.0)
        self.z = kwargs.get("z", 0.0)
        # Attributes
        self.filename = filename
        self.volume = kwargs.get("volume", 1.0)
        self.original_volume = kwargs.get("volume", 1.0)
        self.pitch = kwargs.get("pitch", 1.0)
        self.looping = kwargs.get("looping", False)
        self.direct = kwargs.get("direct", False)
        self.max_distance = kwargs.get("max_distance", 10.0)
        self.reference_distance = kwargs.get("reference_distance", 5.0)
        self.rolloff_factor = kwargs.get("rolloff_factor", 1.0)
        # Manager reference for getting listener position
        self.manager = kwargs.get("manager", None)
        # Distance muting state
        self._distance_muted = False
        self._stored_volume = None
        # Maximum distance for muting (default 20 units)
        self._max_distance = 20.0
        # Handling
        self.ctx = kwargs.get("ctx", None)
        self.hd = Sound(self.ctx)
        self.hd.load(self.filename)
        self.hd.direct = self.direct
        self.hd.volume = self.volume
        self.hd.pitch = self.pitch
        self.hd.max_distance = self.max_distance
        self.hd.reference_distance = self.reference_distance
        self.hd.rolloff_factor = self.rolloff_factor
        if not self.direct:
            self.set_position(self.x, self.y, self.z)

    # Before we get too far, let's add a way to play, stop and destroy, directly from this class. This also includes checking if the sound is playing to begin with.
    def play(self):
        if self.hd:
            if self.looping:
                self.hd.play_looped()
            else:
                self.hd.play()

    def pause(self):
        if self.hd:
            self.hd.pause()

    def stop(self):
        if self.hd:
            self.hd.stop()

    def destroy(self):
        """Safely destroy this sound item."""
        try:
            if self.hd:
                self.hd.close()
                self.hd = None
        except:
            pass
        
        # Remove references to prevent memory leaks
        self.manager = None

    @property
    def is_playing(self):
        return self.hd.is_playing

    @property
    def paused(self):
        return self.hd.paused

    # Now that that is out of the way, let's continue, shall we?
    # Set the position of the source with a given set of coordinates.
    def set_position(self, x, y, z):
        if self.hd:
            self.hd.position = [x, y, z]
            self.x = x
            self.y = y
            self.z = z
            # Check distance muting when position changes
            if self.manager:
                self._check_distance_muting()
    
    def _check_distance_muting(self):
        """Check if this item should be muted based on distance to listener."""
        if not self.manager or self.direct:
            return
        
        # Calculate distance to listener using manager's last known position
        dx = self.x - self.manager.last_x
        dy = self.y - self.manager.last_y
        dz = self.z - self.manager.last_z
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        # Check if we should mute or unmute
        if distance > self._max_distance:
            # Should be muted
            if not self._distance_muted:
                self._mute_for_distance()
        else:
            # Should be audible
            if self._distance_muted:
                self._unmute_for_distance()
    
    def _mute_for_distance(self):
        """Mute this item due to distance."""
        if self.hd and not self._distance_muted:
            self._stored_volume = self.hd.volume
            self.hd.volume = 0.0
            self._distance_muted = True
    
    def _unmute_for_distance(self):
        """Unmute this item when back in range."""
        if self.hd and self._distance_muted and self._stored_volume is not None:
            self.hd.volume = self._stored_volume
            self._distance_muted = False
    
    def get_distance_to_listener(self):
        """Get current distance to listener."""
        if not self.manager:
            return 0.0
        
        dx = self.x - self.manager.last_x
        dy = self.y - self.manager.last_y
        dz = self.z - self.manager.last_z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def is_distance_muted(self):
        """Check if this item is currently muted due to distance."""
        return self._distance_muted
    
    def set_max_distance(self, distance):
        """Set the maximum distance before this item is muted."""
        self._max_distance = max(0.0, distance)
        self._check_distance_muting()
    
    def get_max_distance(self):
        """Get the maximum distance for this item."""
        return self._max_distance
    
    def on_listener_moved(self):
        """Called when the listener position changes."""
        if not self.direct and self.hd and hasattr(self.hd, 'source') and self.hd.source:
            self._check_distance_muting()


# Behold! The manager class! Coded by none other than the messy coder tunmi13 productions! Praise him! Worship him!
# This class takes what has been pre-coded, and assembles it all into one single class where sounds can be managed.
class Manager:
    # Init
    def __init__(self):
        # Create a global context.
        self.ctx = cyal.Context(cyal.Device(), make_current=True, hrtf_soft=3, STEREO_SOURCES = 1024, MONO_SOURCES = 1024)
        # This is where the list of items (ManagerItem) will be placed.
        self.items = []
        # This is where the list of slots (effect slots) will be placed.
        self.slots = []
        #EFX extension.
        self.efx = EfxManager.get_efx(self.ctx)
        # Global effect slots for shared effects
        self.global_effect_slots = {}
        self.global_filters = {}
        # Listener coordinates (last known position)
        self.last_x, self.last_y, self.last_z = 0.0, 0.0, 0.0
        # Set the orientation reference for the class. This does not actually affect the overall orientation unless you use the function which changes both the class's orientation variable and the context's orientation.
        self.orientation = make_orientation(0.0, 0.0)
        # Set the default max distance, reference distance, and rolloff factor for each source.
        self.max_distance = 15.0
        self.reference_distance = 3.0
        self.rolloff_factor = 1.0
        # N/A. Set the clean frequency. This checks how frequently sounds should be cleaned, and once that frequency is reached, it will clean any sounds that are not playing to reserve space for new ones.
        self.clean_frequency = 5
        
        # Sound pool for oneshot sounds (import here to avoid circular imports)
        from .sound_pool import SoundPool
        self.sound_pool = SoundPool(self)
        
        # Automatic cleanup counter
        self.play_count = 0
        self.auto_cleanup_frequency = 10  # Clean every 10 sound plays
    # A quicker way for accessing the listener.
    @property
    def listener(self):
        return self.ctx.listener
    # Adjust the listener's orientation.
    def adjust_orientation(self, orientation):
        self.ctx.listener.orientation = orientation
        self.orientation = self.ctx.listener.orientation

    # Similar to the way of updating the position for sounds, but update the position for the listener.
    def update(self, x, y, z):
        left_hand = [x, y, z]
        self.ctx.listener.position = (
            left_hand  # convert_to_openal_coordinates(*left_hand)
        )
        self.last_x = x
        self.last_y = y
        self.last_z = z
        
        # Notify all items that listener moved
        for item in self.items:
            if item:
                item.on_listener_moved()

    # Play a stationary source.
    def play(self, filename, looping=False, volume=1.0, pitch=1.0, effects=None, filters=None):
        """Play a sound with optional effects and filters. Automatically applies global 
        effects/filters if none are specified.
        
        Args:
            filename: Path to audio file
            looping: Whether to loop the sound
            volume: Sound volume (0.0 to 1.0)
            pitch: Sound pitch (0.5 to 2.0)
            effects: List of effect dictionaries [{'type': 'reverb', 'preset': 'hall'}, ...]
                    If None, automatically applies global effects from manager
            filters: List of filter dictionaries [{'type': 'lowpass', 'gain': 1.0, 'gainhf': 0.5}, ...]
                    If None, automatically applies global filters from manager
        
        Returns:
            ManagerItem instance with effects applied, or None if failed
        """
        # Check if the file exists first. If it doesn't, return None.
        if not os.path.exists(filename):
            return None
            
        # If it's not looping, use the oneshot pool
        if not looping:
            return self.play_oneshot(filename, volume=volume, pitch=pitch)
        
        # Else create an item for looping sounds.
        mi = self._create_manager_item(
            filename,
            looping=looping,
            volume=volume,
            pitch=pitch,
            direct=True
        )
        if not mi:
            return None
            
        self.items.append(mi)
        mi.play()
        
        # Apply effects if specified, or use global effects if none specified
        if effects:
            for i, effect_config in enumerate(effects):
                # Make a copy to avoid modifying the original
                effect_copy = dict(effect_config)
                effect_type = effect_copy.pop('type', 'reverb')
                try:
                    mi.hd.add_effect(effect_type, send_slot=i, **effect_copy)
                except Exception as e:
                    print(f"Failed to apply effect {effect_type}: {e}")
        elif self.global_effect_slots:
            # Auto-apply global effects when no specific effects are provided
            for i, (effect_name, effect) in enumerate(self.global_effect_slots.items()):
                try:
                    self.apply_global_effect_to_sound(mi, effect_name, send_slot=i)
                except Exception as e:
                    print(f"Failed to apply global effect {effect_name}: {e}")
        
        # Apply filters if specified, or use global filters if none specified
        if filters:
            for filter_config in filters:
                # Make a copy to avoid modifying the original
                filter_copy = dict(filter_config)
                filter_type = filter_copy.pop('type', 'lowpass')
                try:
                    mi.hd.add_filter(filter_type, **filter_copy)
                except Exception as e:
                    print(f"Failed to apply filter {filter_type}: {e}")
        elif self.global_filters:
            # Auto-apply global filters when no specific filters are provided
            for filter_name in self.global_filters.keys():
                try:
                    self.apply_global_filter_to_sound(mi, filter_name)
                    break  # Only apply the first global filter (direct filter limitation)
                except Exception as e:
                    print(f"Failed to apply global filter {filter_name}: {e}")
        
        # Check for cleaning.
        self._auto_cleanup()
        # Return the item to be manipulated externally.
        return mi

    def play_oneshot(self, filename, volume=1.0, pitch=1.0):
        """Play a oneshot sound using the sound pool for automatic cleanup."""
        return self.sound_pool.play_oneshot(filename, volume=volume, pitch=pitch)

    def play_p_oneshot(self, filename, x, y, z, volume=1.0, pitch=1.0):
        """Play a positioned oneshot sound using the sound pool for automatic cleanup."""
        return self.sound_pool.play_oneshot(filename, volume=volume, pitch=pitch, x=x, y=y, z=z)


    def _create_manager_item(self, filename, **kwargs):
        """Create a ManagerItem with error handling."""
        try:
            mi = ManagerItem(
                filename,
                ctx=self.ctx,
                max_distance=self.max_distance,
                reference_distance=self.reference_distance,
                rolloff_factor=self.rolloff_factor,
                manager=self,
                **kwargs
            )
            return mi
        except Exception as e:
            print(f"Error creating sound item for '{filename}': {e}")
            return None

    def _auto_cleanup(self):
        """Automatic cleanup based on play count."""
        self.play_count += 1
        if self.play_count >= self.auto_cleanup_frequency:
            self.clean()
            self.sound_pool.cleanup_finished_sounds()
            self.play_count = 0

    # Play a positioned source.
    def play_p(self, filename, x, y, z, looping=False, volume=1.0, pitch=1.0, effects=None, filters=None):
        """Play a positioned sound with optional effects and filters. Automatically applies 
        global effects/filters if none are specified.
        
        Args:
            filename: Path to audio file
            x, y, z: 3D position coordinates
            looping: Whether to loop the sound
            volume: Sound volume (0.0 to 1.0)
            pitch: Sound pitch (0.5 to 2.0)
            effects: List of effect dictionaries [{'type': 'reverb', 'preset': 'hall'}, ...]
                    If None, automatically applies global effects from manager
            filters: List of filter dictionaries [{'type': 'lowpass', 'gain': 1.0, 'gainhf': 0.5}, ...]
                    If None, automatically applies global filters from manager
        
        Returns:
            ManagerItem instance with effects applied, or None if failed
        """
        # Check if the file exists first. If it doesn't, return None.
        if not os.path.exists(filename):
            return None
            
        # If it's not looping, use the oneshot pool
        if not looping:
            return self.sound_pool.play_oneshot(filename, volume=volume, pitch=pitch, x=x, y=y, z=z)
        
        # Else create an item for looping sounds.
        mi = self._create_manager_item(
            filename,
            x=x,
            y=y,
            z=z,
            looping=looping,
            volume=volume,
            pitch=pitch,
            direct=False  # Positioned sounds are not direct
        )
        if not mi:
            return None
            
        self.items.append(mi)
        mi.play()
        
        # Apply effects if specified, or use global effects if none specified
        if effects:
            for i, effect_config in enumerate(effects):
                # Make a copy to avoid modifying the original
                effect_copy = dict(effect_config)
                effect_type = effect_copy.pop('type', 'reverb')
                try:
                    mi.hd.add_effect(effect_type, send_slot=i, **effect_copy)
                except Exception as e:
                    print(f"Failed to apply effect {effect_type}: {e}")
        elif self.global_effect_slots:
            # Auto-apply global effects when no specific effects are provided
            for i, (effect_name, effect) in enumerate(self.global_effect_slots.items()):
                try:
                    self.apply_global_effect_to_sound(mi, effect_name, send_slot=i)
                except Exception as e:
                    print(f"Failed to apply global effect {effect_name}: {e}")
        
        # Apply filters if specified, or use global filters if none specified
        if filters:
            for filter_config in filters:
                # Make a copy to avoid modifying the original
                filter_copy = dict(filter_config)
                filter_type = filter_copy.pop('type', 'lowpass')
                try:
                    mi.hd.add_filter(filter_type, **filter_copy)
                except Exception as e:
                    print(f"Failed to apply filter {filter_type}: {e}")
        elif self.global_filters:
            # Auto-apply global filters when no specific filters are provided
            for filter_name in self.global_filters.keys():
                try:
                    self.apply_global_filter_to_sound(mi, filter_name)
                    break  # Only apply the first global filter (direct filter limitation)
                except Exception as e:
                    print(f"Failed to apply global filter {filter_name}: {e}")
        
        # Check for cleaning.
        self._auto_cleanup()
        # Return the item to be manipulated externally.
        return mi


    # Updates the position of an item.
    def update_position(self, item, x, y, z):
        # Check if the item exists.
        if not item in self.items:
            return False
        item.set_position(x, y, z)
        return True

    # Updates the attributes of an item.
    def update_attribs(self, item, volume, pitch):
        # Check if the item exists.
        if not item in self.items:
            return False
        item.hd.volume = volume
        item.hd.pitch = pitch
        return True

    # Pause all items.
    def pause_all(self):
        for i in self.items:
            i.pause()

    # Resume all items.
    def resume_all(self):
        for i in self.items:
            i.play()

    # Do some cleaning!
    def clean(self):
        # Create a new list of items to keep
        items_to_keep = []
        
        for i in self.items:
            try:
                # Check if item should be kept
                if i.is_playing or i.paused:
                    items_to_keep.append(i)
                else:
                    # Destroy items that are not playing or paused
                    i.destroy()
            except:
                # If there's an error checking the item, destroy it
                try:
                    i.destroy()
                except:
                    pass  # Ignore errors during cleanup
        
        # Replace the items list with the cleaned list
        self.items = items_to_keep

    # Destroy a certain item.
    def destroy(self, item):
        for i in self.items:
            if i == item:
                i.destroy()
                return True
        return False

    # Destroy all items.
    def destroy_all(self):
        """Destroy all sounds and clean up resources."""
        destroyed_count = 0
        
        # Destroy regular items
        if len(self.items) > 0:
            for i in self.items:
                try:
                    i.destroy()
                    destroyed_count += 1
                except:
                    pass
            self.items.clear()
        
        # Destroy all oneshot sounds
        self.sound_pool.stop_all_oneshots()
        
        print(f"Destroyed {destroyed_count} regular sounds and all oneshot sounds")
        return destroyed_count > 0
        
    def cleanup_finished_sounds(self):
        """Clean up all finished sounds manually."""
        self.clean()
        self.sound_pool.cleanup_finished_sounds()
        
    def get_memory_stats(self):
        """Get memory usage statistics."""
        active_regular = len([i for i in self.items if i and hasattr(i, 'is_playing')])
        oneshot_stats = self.sound_pool.get_stats()
        
        return {
            'regular_sounds': len(self.items),
            'active_regular': active_regular,
            'oneshot_stats': oneshot_stats,
            'total_sounds': len(self.items) + oneshot_stats['total_active']
        }
    
    # Enhanced audio effects methods for the manager
    def create_global_effect(self, name: str, effect_type: str, **kwargs) -> AudioEffect:
        """Create a global effect that can be applied to multiple sounds.
        
        Args:
            name: Unique name for this effect
            effect_type: Type of effect ('reverb', 'distortion', etc.)
            **kwargs: Effect parameters
        
        Returns:
            AudioEffect instance
        """
        effect = AudioEffect(self.efx)
        
        # Apply the requested effect type
        if effect_type == 'reverb':
            preset = kwargs.get('preset', None)
            if preset:
                effect.reverb(preset=preset)
            else:
                effect.reverb(**kwargs)
        elif effect_type == 'distortion':
            effect.distortion(**kwargs)
        elif effect_type == 'echo':
            effect.echo(**kwargs)
        elif effect_type == 'chorus':
            effect.chorus(**kwargs)
        elif effect_type == 'flanger':
            effect.flanger(**kwargs)
        elif effect_type == 'pitch_shift':
            effect.pitch_shift(**kwargs)
        elif effect_type == 'auto_wah':
            effect.auto_wah(**kwargs)
        elif effect_type == 'compressor':
            effect.compressor(**kwargs)
        elif effect_type == 'equalizer':
            effect.equalizer(**kwargs)
        else:
            raise ValueError(f"Unknown effect type: {effect_type}")
        
        self.global_effect_slots[name] = effect
        return effect
    
    def apply_global_effect_to_sound(self, sound_item, effect_name: str, send_slot: int = 0):
        """Apply a global effect to a specific sound.
        
        Args:
            sound_item: ManagerItem instance
            effect_name: Name of the global effect
            send_slot: Which auxiliary send slot to use (0-3)
        """
        if effect_name not in self.global_effect_slots:
            raise ValueError(f"Global effect '{effect_name}' not found")
        
        effect = self.global_effect_slots[effect_name]
        if effect.slot and sound_item.hd and sound_item.hd.source:
            self.efx.send(sound_item.hd.source, send_slot, effect.slot)
    
    def create_global_filter(self, name: str, filter_type: str, **kwargs) -> AudioFilter:
        """Create a global filter that can be applied to multiple sounds.
        
        Args:
            name: Unique name for this filter
            filter_type: Type of filter ('lowpass', 'highpass', 'bandpass')
            **kwargs: Filter parameters
        
        Returns:
            AudioFilter instance
        """
        audio_filter = AudioFilter(self.efx)
        
        # Apply the requested filter type
        if filter_type == 'lowpass':
            audio_filter.lowpass(**kwargs)
        elif filter_type == 'highpass':
            audio_filter.highpass(**kwargs)
        elif filter_type == 'bandpass':
            audio_filter.bandpass(**kwargs)
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")
        
        self.global_filters[name] = audio_filter
        return audio_filter
    
    def apply_global_filter_to_sound(self, sound_item, filter_name: str):
        """Apply a global filter to a specific sound.
        
        Args:
            sound_item: ManagerItem instance
            filter_name: Name of the global filter
        """
        if filter_name not in self.global_filters:
            raise ValueError(f"Global filter '{filter_name}' not found")
        
        audio_filter = self.global_filters[filter_name]
        if audio_filter.filter and sound_item.hd and sound_item.hd.source:
            sound_item.hd.source.direct_filter = audio_filter.filter
    
    def apply_room_acoustics(self, room_type: str = "room"):
        """Apply room acoustics to all currently playing sounds.
        
        Args:
            room_type: Type of room acoustics to apply
        """
        # Create or update global room reverb
        effect_name = f"room_acoustics_{room_type}"
        if effect_name not in self.global_effect_slots:
            self.create_global_effect(effect_name, 'reverb', preset=room_type)
        
        # Apply to all active sounds
        for item in self.items:
            if item.is_playing:
                try:
                    self.apply_global_effect_to_sound(item, effect_name, 0)
                except:
                    pass  # Skip if error occurs
    
    def apply_environmental_filter(self, environment: str = "clear"):
        """Apply environmental filtering to all currently playing sounds.
        
        Args:
            environment: Type of environment ('underwater', 'radio', 'muffled', etc.)
        """
        filter_name = f"env_filter_{environment}"
        if filter_name not in self.global_filters:
            presets = EffectPresets.get_filter_presets()
            if environment in presets:
                preset = presets[environment]
                filter_type = preset['type']
                filter_params = {k: v for k, v in preset.items() if k != 'type'}
                self.create_global_filter(filter_name, filter_type, **filter_params)
        
        # Apply to all active sounds
        for item in self.items:
            if item.is_playing:
                try:
                    self.apply_global_filter_to_sound(item, filter_name)
                except:
                    pass  # Skip if error occurs
    
    def get_available_effects(self) -> list:
        """Get list of available effect types."""
        return ['reverb', 'distortion', 'echo', 'chorus', 'flanger', 'pitch_shift', 
                'auto_wah', 'compressor', 'equalizer']
    
    def get_available_filters(self) -> list:
        """Get list of available filter types."""
        return ['lowpass', 'highpass', 'bandpass']
    
    def get_reverb_presets(self) -> list:
        """Get list of available reverb presets."""
        return list(EffectPresets.get_reverb_presets().keys())
    
    def get_filter_presets(self) -> list:
        """Get list of available filter presets."""
        return list(EffectPresets.get_filter_presets().keys())
    
    def remove_global_effect(self, name: str):
        """Remove a global effect."""
        if name in self.global_effect_slots:
            # Remove from all sounds using this effect
            for item in self.items:
                try:
                    if item.hd and item.hd.source:
                        for i in range(4):
                            self.efx.send(item.hd.source, i, None)
                except:
                    pass
            del self.global_effect_slots[name]
    
    def remove_global_filter(self, name: str):
        """Remove a global filter."""
        if name in self.global_filters:
            # Remove from all sounds using this filter  
            for item in self.items:
                try:
                    if item.hd and item.hd.source and hasattr(item.hd.source, 'direct_filter'):
                        item.hd.source.direct_filter = None
                except:
                    pass
            del self.global_filters[name]
    
    def clear_all_effects(self):
        """Remove all effects from all sounds."""
        for item in self.items:
            if item.hd:
                try:
                    item.hd.remove_all_effects()
                    item.hd.remove_all_filters()
                except:
                    pass
        
        self.global_effect_slots.clear()
        self.global_filters.clear()
    
    # Streaming audio methods
    def create_streaming_sound(self, ctx=None):
        """Create a new streaming sound instance."""
        from .sound import StreamingSound
        return StreamingSound(ctx or self.ctx)
    
    def play_streaming(self, filename: str, loop: bool = False, volume: float = 1.0, 
                      chunk_size: int = None, preload_buffers: int = None):
        """
        Play a streaming audio file (useful for music/large files).
        
        Args:
            filename: Path to audio file
            loop: Whether to loop the audio
            volume: Initial volume (0.0 to 1.0)
            chunk_size: Size of audio chunks in bytes
            preload_buffers: Number of buffers to preload
            
        Returns:
            StreamingSound instance or None if failed
        """
        stream = self.create_streaming_sound()
        
        if stream.load_stream(filename, chunk_size, preload_buffers):
            stream.set_volume(volume)
            if stream.play(loop):
                return stream
        
        return None

audio_manager = Manager()