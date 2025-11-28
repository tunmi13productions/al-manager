# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

# Sound Group System for Game Entities
# Allows easy attachment of multiple sounds to game objects

import os
import math
import random
from typing import Dict, List, Optional, Tuple, Any, Callable
from .manager import Manager
from .effects import EffectPresets

class SoundGroup:
    """
    A sound group that can be attached to game entities (players, enemies, NPCs, etc.)
    Manages multiple sounds with automatic positioning, state-based playback, and effects.
    """
    
    def __init__(self, manager: Manager, entity_id: str = None):
        """
        Initialize a sound group.
        
        Args:
            manager: The AL Manager instance
            entity_id: Optional identifier for this entity (for debugging)
        """
        self.manager = manager
        self.entity_id = entity_id or f"entity_{id(self)}"
        
        # Auto-register with manager for automatic cleanup
        self.manager.register_sound_group(self)
        
        # Position tracking
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        # Sound storage - simplified without categories
        self.sounds = {}
        
        # Currently playing sounds
        self.active_sounds = {}
        
        # State management
        self.is_enabled = True
        self.global_volume = 1.0
        # Removed category volumes - now using global volume only
        
        # Auto-positioning
        self.auto_update_position = True
        self.position_callback = None  # Function to get entity position
        
        # Distance-based effects
        self.distance_effects = {
            'far': {'filters': [{'type': 'lowpass', 'gainhf': 0.3}]},
            'underwater': {'effects': [{'type': 'reverb', 'preset': 'underwater'}]},
            'echo': {'effects': [{'type': 'echo', 'delay': 0.2, 'feedback': 0.3}]}
        }
        
        # Random variation settings
        self.pitch_variation = 0.1  # ±10% pitch variation
        self.volume_variation = 0.1  # ±10% volume variation
    
    def set_position(self, x: float, y: float, z: float):
        """Update the position of this sound group."""
        self.x = x
        self.y = y
        self.z = z
        
        # Update all active positioned sounds
        for sound_item in self.active_sounds.values():
            if sound_item:
                try:
                    # ManagerItem has set_position method
                    sound_item.set_position(x, y, z)
                except Exception as e:
                    print(f"Warning: Error updating position for sound in group {self.entity_id}: {e}")
    
    def set_position_callback(self, callback: Callable[[], Tuple[float, float, float]]):
        """
        Set a callback function that returns the entity's current position.
        This enables automatic position updates.
        
        Args:
            callback: Function that returns (x, y, z) tuple
        """
        self.position_callback = callback
        self.auto_update_position = True
    
    def update_position_from_callback(self):
        """Update position using the callback function if set."""
        if self.position_callback and self.auto_update_position:
            try:
                x, y, z = self.position_callback()
                self.set_position(x, y, z)
            except Exception as e:
                print(f"Warning: Position callback failed for {self.entity_id}: {e}")
    
    def add_sound(self, name: str, file_path: str, 
                  effects: List[Dict] = None, filters: List[Dict] = None,
                  volume: float = 1.0, pitch: float = 1.0,
                  looping: bool = False, positioned: bool = True,
                  autoplay: bool = False):
        """
        Add a sound to this group.
        
        Args:
            name: Unique name for this sound
            file_path: Path to the audio file
            effects: List of effect configurations
            filters: List of filter configurations
            volume: Base volume (0.0 to 1.0)
            pitch: Base pitch (0.5 to 2.0)
            looping: Whether the sound should loop
            positioned: Whether this sound should be positioned in 3D space
            autoplay: Whether to instantly play the sound after adding it
        """
        sound_config = {
            'name': name,
            'file_path': file_path,
            'effects': effects or [],
            'filters': filters or [],
            'volume': volume,
            'pitch': pitch,
            'looping': looping,
            'positioned': positioned,
            'variations': []  # For random sound variations
        }
        
        self.sounds[name] = sound_config
        
        # Auto-play the sound if requested
        if autoplay:
            self.play_sound(name)
    
    def add_sound_variation(self, base_name: str, variation_path: str, autoplay: bool = False):
        """Add a variation of an existing sound for randomization.
        
        Args:
            base_name: Name of the base sound to add variation to
            variation_path: Path to the variation audio file
            autoplay: Whether to instantly play this variation after adding it
        """
        if base_name in self.sounds:
            self.sounds[base_name]['variations'].append(variation_path)
            
            # Auto-play the variation if requested
            if autoplay:
                # Temporarily set the base sound to use this specific variation
                original_path = self.sounds[base_name]['file_path']
                self.sounds[base_name]['file_path'] = variation_path
                self.play_sound(base_name)
                # Restore original path
                self.sounds[base_name]['file_path'] = original_path
    
    def play_sound(self, name: str, 
                   override_volume: float = None,
                   override_pitch: float = None,
                   override_effects: List[Dict] = None,
                   stop_existing: bool = False) -> Optional[Any]:
        """
        Play a specific sound by name.
        
        Args:
            name: Sound name
            override_volume: Override the default volume
            override_pitch: Override the default pitch
            override_effects: Override the default effects
            stop_existing: Stop any existing sound with this name
        
        Returns:
            The sound item if successful, None otherwise
        """
        if not self.is_enabled:
            return None
        
        # Update position from callback if available
        self.update_position_from_callback()
        
        # Find the sound configuration
        if name not in self.sounds:
            print(f"Warning: Sound '{name}' not found for {self.entity_id}")
            return None
        
        sound_config = self.sounds[name]
        
        # Stop existing sound if requested
        if stop_existing and name in self.active_sounds:
            existing_sound = self.active_sounds[name]
            if existing_sound:
                self.manager.destroy(existing_sound)
                del self.active_sounds[name]
        
        # Choose file path (with variations)
        file_path = sound_config['file_path']
        if sound_config['variations'] and random.random() < 0.5:
            file_path = random.choice(sound_config['variations'])
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Warning: Audio file not found: {file_path}")
            return None
        
        # Calculate final audio parameters
        final_volume = (override_volume or sound_config['volume']) * self.global_volume
        
        # Add random variation
        if self.volume_variation > 0:
            volume_mult = 1.0 + random.uniform(-self.volume_variation, self.volume_variation)
            final_volume *= volume_mult
        
        final_pitch = override_pitch or sound_config['pitch']
        if self.pitch_variation > 0:
            pitch_mult = 1.0 + random.uniform(-self.pitch_variation, self.pitch_variation)
            final_pitch *= pitch_mult
        
        # Determine effects and filters
        effects = override_effects or sound_config['effects']
        filters = sound_config['filters']
        
        # Apply distance-based effects if positioned
        if sound_config['positioned']:
            distance = self._get_distance_to_listener()
            effects = list(effects)  # Copy to avoid modifying original
            filters = list(filters)  # Copy to avoid modifying original
            
            # Add distance-based effects
            if distance > 20:
                effects.extend(self.distance_effects['far'].get('effects', []))
                filters.extend(self.distance_effects['far'].get('filters', []))
        
        try:
            # Play the sound
            if sound_config['positioned']:
                sound_item = self.manager.play_p(
                    file_path,
                    x=self.x, y=self.y, z=self.z,
                    looping=sound_config['looping'],
                    volume=final_volume,
                    pitch=final_pitch,
                    effects=effects if effects else None,
                    filters=filters if filters else None
                )
            else:
                sound_item = self.manager.play(
                    file_path,
                    looping=sound_config['looping'],
                    volume=final_volume,
                    pitch=final_pitch,
                    effects=effects if effects else None,
                    filters=filters if filters else None
                )
            
            if sound_item:
                self.active_sounds[name] = sound_item
                return sound_item
            
        except Exception as e:
            print(f"Error playing sound '{name}' for {self.entity_id}: {e}")
        
        return None
    
    def play_random_sound(self, **kwargs) -> Optional[Any]:
        """Play a random sound from this group."""
        if not self.sounds:
            return None
        
        sound_name = random.choice(list(self.sounds.keys()))
        return self.play_sound(sound_name, **kwargs)
    
    def stop_sound(self, name: str):
        """Stop a specific sound."""
        if name in self.active_sounds:
            sound_item = self.active_sounds[name]
            if sound_item:
                self.manager.destroy(sound_item)
            del self.active_sounds[name]
    
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds."""
        for sound_item in self.active_sounds.values():
            if sound_item:
                self.manager.destroy(sound_item)
        self.active_sounds.clear()
    
    def pause_all_sounds(self):
        """Pause all currently playing sounds."""
        for sound_item in self.active_sounds.values():
            if sound_item:
                try:
                    sound_item.pause()
                except Exception as e:
                    print(f"Warning: Error pausing sound in group {self.entity_id}: {e}")
    
    def resume_all_sounds(self):
        """Resume all currently paused sounds."""
        for sound_item in self.active_sounds.values():
            if sound_item:
                try:
                    sound_item.play()
                except Exception as e:
                    print(f"Warning: Error resuming sound in group {self.entity_id}: {e}")
    
    
    def set_global_volume(self, volume: float):
        """Set global volume for this sound group."""
        self.global_volume = max(0.0, min(1.0, volume))
    
    def enable(self):
        """Enable sound playback for this group."""
        self.is_enabled = True
    
    def disable(self):
        """Disable sound playback and stop all sounds."""
        self.is_enabled = False
        self.stop_all_sounds()
    
    def is_playing(self, name: str) -> bool:
        """Check if a specific sound is currently playing."""
        if name in self.active_sounds:
            sound_item = self.active_sounds[name]
            if sound_item:
                try:
                    return sound_item.is_playing
                except:
                    return False
        return False
    
    def get_active_sounds_count(self) -> int:
        """Get the number of currently active sounds."""
        return len([s for s in self.active_sounds.values() if s])
    
    def cleanup_finished_sounds(self):
        """Remove finished (non-looping) sounds from active list."""
        to_remove = []
        for sound_name, sound_item in self.active_sounds.items():
            if sound_item:
                try:
                    # ManagerItem has is_playing and paused properties
                    if not sound_item.is_playing and not sound_item.paused:
                        to_remove.append(sound_name)
                except Exception as e:
                    # If we can't check status, remove the sound item
                    print(f"Warning: Error checking sound status in group {self.entity_id}: {e}")
                    to_remove.append(sound_name)
        
        for name in to_remove:
            del self.active_sounds[name]
    
    def _get_distance_to_listener(self) -> float:
        """Calculate distance to the listener."""
        try:
            # Get listener position from manager
            listener_x = self.manager.last_x
            listener_y = self.manager.last_y
            listener_z = self.manager.last_z
            
            dx = self.x - listener_x
            dy = self.y - listener_y
            dz = self.z - listener_z
            
            return math.sqrt(dx*dx + dy*dy + dz*dz)
        except Exception as e:
            print(f"Warning: Error calculating distance in group {self.entity_id}: {e}")
            return 0.0
    
    def apply_environmental_effect(self, effect_name: str):
        """Apply an environmental effect to all active sounds."""
        if effect_name in self.distance_effects:
            effect_config = self.distance_effects[effect_name]
            
            for sound_item in self.active_sounds.values():
                if sound_item:
                    # Apply effects
                    for effect in effect_config.get('effects', []):
                        try:
                            # ManagerItem has hd property
                            sound_item.hd.add_effect(**effect)
                        except Exception as e:
                            print(f"Warning: Error applying effect to sound in group {self.entity_id}: {e}")
                    
                    # Apply filters
                    for filter_config in effect_config.get('filters', []):
                        try:
                            # ManagerItem has hd property
                            sound_item.hd.add_filter(**filter_config)
                        except Exception as e:
                            print(f"Warning: Error applying filter to sound in group {self.entity_id}: {e}")
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about this sound group."""
        return {
            'entity_id': self.entity_id,
            'position': (self.x, self.y, self.z),
            'is_enabled': self.is_enabled,
            'global_volume': self.global_volume,
            'total_sounds_configured': len(self.sounds),
            'active_sounds_count': self.get_active_sounds_count(),
            'auto_update_position': self.auto_update_position
        }
    
    def destroy(self):
        """Properly destroy this sound group and clean up all resources."""
        # Stop all active sounds
        self.stop_all_sounds()
        
        # Unregister from manager
        self.manager.unregister_sound_group(self)
        
        # Clear references
        self.sounds.clear()
        self.active_sounds.clear()
        self.position_callback = None

# Convenience functions for common game entity types

def create_player_sound_group(manager: Manager, entity_id: str = "player") -> SoundGroup:
    """Create a pre-configured sound group for a player character."""
    group = SoundGroup(manager, entity_id)
    
    # Typical player sounds (you'll need to add actual file paths)
    # group.add_sound('footstep', 'audio/player/footstep.ogg', looping=False)
    # group.add_sound('run', 'audio/player/run.ogg', looping=True)
    # group.add_sound('jump', 'audio/player/jump.ogg', looping=False)
    # group.add_sound('hurt', 'audio/player/hurt.ogg', looping=False)
    # group.add_sound('grunt', 'audio/player/grunt.ogg', looping=False)
    
    # Player-specific settings
    group.pitch_variation = 0.05  # Less pitch variation for player
    
    return group

def create_enemy_sound_group(manager: Manager, entity_id: str, enemy_type: str = "generic") -> SoundGroup:
    """Create a pre-configured sound group for an enemy."""
    group = SoundGroup(manager, f"{enemy_type}_{entity_id}")
    
    # Enemy-specific settings
    group.pitch_variation = 0.15  # More variation for enemies
    group.volume_variation = 0.15
    
    return group

def create_npc_sound_group(manager: Manager, entity_id: str) -> SoundGroup:
    """Create a pre-configured sound group for an NPC."""
    group = SoundGroup(manager, f"npc_{entity_id}")
    
    # NPC-specific settings
    group.pitch_variation = 0.08
    
    return group