# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

# Sound pool for managing oneshot sounds and preventing memory leaks
import os
from typing import List, Optional, Any
from .manager import ManagerItem

class SoundPool:
    """
    Sound pool for managing oneshot sounds efficiently.
    Provides automatic cleanup and sound reuse to prevent memory leaks.
    """
    
    def __init__(self, manager):
        self.manager = manager
        self.active_oneshots: List[ManagerItem] = []
        self.max_oneshots = 100  # Maximum number of concurrent oneshots
        self.cleanup_threshold = 20  # Clean when this many sounds finish
        
    def play_oneshot(self, filename: str, volume: float = 1.0, pitch: float = 1.0, 
                     x: float = None, y: float = None, z: float = None) -> Optional[ManagerItem]:
        """
        Play a oneshot sound with automatic cleanup.
        
        Args:
            filename: Path to audio file
            volume: Sound volume
            pitch: Sound pitch
            x, y, z: Optional 3D position
        
        Returns:
            ManagerItem if successful, None otherwise
        """
        # Clean up finished sounds periodically
        self.cleanup_finished_sounds()
        
        # Check if we're at capacity
        if len(self.active_oneshots) >= self.max_oneshots:
            self.force_cleanup_oldest()
        
        # Check if file exists
        if not os.path.exists(filename):
            return None
        
        try:
            # Determine if this should be direct or positioned
            is_direct = x is None or y is None or z is None
            
            # Create the sound item
            item = self.manager._create_manager_item(filename, volume=volume, pitch=pitch, direct=is_direct)
            if not item:
                return None
            
            # Set position if provided (for positioned sounds)
            if not is_direct:
                item.set_position(x, y, z)
            
            # Play the sound
            item.play()
            
            # Apply global effects if they exist (same logic as main play method)
            if self.manager.global_effect_slots:
                for i, (effect_name, effect) in enumerate(self.manager.global_effect_slots.items()):
                    try:
                        self.manager.apply_global_effect_to_sound(item, effect_name, send_slot=i)
                    except Exception as e:
                        print(f"Failed to apply global effect {effect_name} to oneshot: {e}")
            
            # Apply global filters if they exist
            if self.manager.global_filters:
                for filter_name in self.manager.global_filters.keys():
                    try:
                        self.manager.apply_global_filter_to_sound(item, filter_name)
                        break  # Only apply the first global filter (direct filter limitation)
                    except Exception as e:
                        print(f"Failed to apply global filter {filter_name} to oneshot: {e}")
            
            # Add to active list
            self.active_oneshots.append(item)
            
            return item
            
        except Exception as e:
            print(f"Error playing oneshot '{filename}': {e}")
            return None
    
    def cleanup_finished_sounds(self):
        """Remove finished oneshot sounds from memory."""
        finished_count = 0
        still_active = []
        
        for item in self.active_oneshots:
            try:
                if item and hasattr(item, 'is_playing') and hasattr(item, 'paused'):
                    # Keep sounds that are still playing or paused
                    if item.is_playing or item.paused:
                        still_active.append(item)
                    else:
                        # Sound is finished, destroy it
                        item.destroy()
                        finished_count += 1
                else:
                    # Item is invalid, count as finished
                    try:
                        item.destroy()
                    except:
                        pass
                    finished_count += 1
            except:
                # Error accessing item, assume it's finished
                try:
                    item.destroy()
                except:
                    pass
                finished_count += 1
        
        self.active_oneshots = still_active
        
        if finished_count > 0:
            print(f"Cleaned up {finished_count} finished oneshot sounds")
    
    def force_cleanup_oldest(self):
        """Force cleanup of oldest sounds when at capacity."""
        if not self.active_oneshots:
            return
        
        # Stop and remove the oldest 20% of sounds
        cleanup_count = max(1, len(self.active_oneshots) // 5)
        
        for i in range(cleanup_count):
            if self.active_oneshots:
                oldest = self.active_oneshots.pop(0)
                try:
                    oldest.stop()
                    oldest.destroy()
                except:
                    pass
        
        print(f"Force cleaned up {cleanup_count} oldest sounds due to capacity limit")
    
    def stop_all_oneshots(self):
        """Stop and clean up all oneshot sounds."""
        count = len(self.active_oneshots)
        
        for item in self.active_oneshots:
            try:
                item.stop()
                item.destroy()
            except:
                pass
        
        self.active_oneshots.clear()
        
        if count > 0:
            print(f"Stopped and cleaned up {count} oneshot sounds")
    
    def get_active_count(self) -> int:
        """Get the number of currently active oneshot sounds."""
        return len(self.active_oneshots)
    
    def set_max_oneshots(self, max_count: int):
        """Set the maximum number of concurrent oneshots."""
        self.max_oneshots = max(10, max_count)  # Minimum of 10
        
        # If we're already over the limit, clean up
        if len(self.active_oneshots) > self.max_oneshots:
            self.force_cleanup_oldest()
    
    def get_stats(self) -> dict:
        """Get statistics about the sound pool."""
        playing_count = 0
        paused_count = 0
        
        for item in self.active_oneshots:
            try:
                if hasattr(item, 'is_playing') and item.is_playing:
                    playing_count += 1
                elif hasattr(item, 'paused') and item.paused:
                    paused_count += 1
            except:
                pass
        
        return {
            'total_active': len(self.active_oneshots),
            'currently_playing': playing_count,
            'currently_paused': paused_count,
            'max_capacity': self.max_oneshots
        }