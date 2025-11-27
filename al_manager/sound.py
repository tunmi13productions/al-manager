# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

# Basic sound manager for CyAL.
import cyal
import cyal.exceptions,cyal.listener
import os
import math
import pyogg
import requests
import io
from pydub import AudioSegment

import subprocess, threading
from .assist import convert_to_openal_coordinates
from .effects import AudioEffect, AudioFilter, EffectPresets
from .efx_manager import EfxManager
import threading
import queue


# Global buffers.
buffers = {}

# Helpful shortcut functions.


# This makes it easy to set orientation.
def deg2rad(angle):
    return (angle / 180.0) * math.pi


def make_orientation(hdegrees, vdegrees, bdegrees=0):
    hrad = deg2rad(hdegrees)
    vrad = deg2rad(vdegrees)
    return (math.sin(hrad), math.cos(hrad), -math.sin(vrad), 0, 0, 1)


# And now, for the sound class itself.
class Sound:
    # Initialization. Context is passed to this class.
    def __init__(self, ctx=cyal.Context(cyal.Device(), make_current=True, hrtf_soft=1)):
        # The context passed to the Sound class for a sound to be played.
        self.ctx = ctx
        # The source and buffer, used later.
        self.source = None
        self.buffer = None
        # Controls whether a source is direct (does not move), or is able to be positioned, or not. The value will be changed accordingly with a property.
        self.is_direct = False
        # Controls the position of the source.
        self.source_position = [0.0, 0.0, 0.0]
        # Audio effects support
        self.applied_effects = []
        self.applied_filters = []
        self.direct_filter = None

    # Loads a file, utilizing the data function above. Add the option to loop if the user wishes.
    def load(self, filename):
        path = os.path.realpath(filename)
        # First check if there is a pre-existing buffer that can be used.
        if path in buffers:
            # There is, so creation is not necessary.
            self.buffer = buffers[path]
        else:
            # One must be created.
            self.buffer = self.ctx.gen_buffer()
            # Detect file format and retrieve audio data accordingly
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext == '.ogg':
                # Load OGG file using pyogg
                ogg_file = pyogg.VorbisFile(filename)
                channels = ogg_file.channels
                samplerate = ogg_file.frequency
                audio_data = ogg_file.buffer
            else:
                # Load other formats (WAV, MP3, etc.) using pydub
                audio_segment = AudioSegment.from_file(filename)
                # Convert to raw audio data
                audio_data = audio_segment.raw_data
                channels = audio_segment.channels
                samplerate = audio_segment.frame_rate
            
            # Now it is time to set the buffer's data with the data retrieved.
            # First, check the amount of channels the audio has and assign the variable fm with the correct ENUM.
            if channels == 1:
                fm = cyal.BufferFormat.MONO16
            else:
                fm = cyal.BufferFormat.STEREO16
            # Now officially set it.
            self.buffer.set_data(audio_data, sample_rate=samplerate, format=fm)
            buffers[path] = self.buffer
        # Generate a source.
        self.source = self.ctx.gen_source()
        # Attach the buffer to the source.
        self.source.buffer = self.buffer
        # Spatialization
        self.source.spatialize = True

    def play(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Check if the source is playing.
        if self.is_playing:
            return False
        # Is it a looped source? If yes, make it stop looping.
        if self.looping:
            self.looping = False
        self.source.play()
        return True

    # Play the source and make it loop, if it is active (see properties below).
    def play_looped(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Check if the source is playing.
        if self.is_playing:
            return False
        # Is it a looped source? If not, make it loop.
        if not self.looping:
            self.looping = True
        self.source.play()
        return True

    # Pause the source without restarting the sound completely.
    def pause(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Check if the source is already paused.
        if self.paused:
            return False
        self.source.pause()
        return True

    # Stop the source if it is active (see properties below).
    def stop(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Check if the source is already stopped.
        if not self.is_playing:
            return False
        self.source.stop()
        return True

    # Properties
    # These are pretty much self explanatory so I won't go into any detail here.
    @property
    def is_active(self):
        if self.source and self.buffer:
            return True
        else:
            return False

    @property
    def is_playing(self):
        if not self.is_active:
            return False
        return bool(self.source.state == cyal.SourceState.PLAYING)

    @property
    def paused(self):
        if not self.is_active:
            return False
        return bool(self.source.state == cyal.SourceState.PAUSED)

    @property
    def looping(self):
        if not self.is_active:
            return False
        return bool(self.source.looping)

    @looping.setter
    def looping(self, value):
        if self.is_active:
            self.source.looping = value

    @property
    def direct(self):
        return self.is_direct

    @direct.setter
    def direct(self, value):
        if value != self.is_direct:
            if value:
                self.source.relative = True
                self.source.direct_channels = True
                self.position = [0.0, 0.0, 0.0]
                self.is_direct = True
            else:
                self.source.relative = False
                self.source.direct_channels = False
                self.is_direct = False

    @property
    def position(self):
        return self.source_position

    @position.setter
    def position(self, value):
        if self.is_direct:
            raise ValueError("Direct sources cannot be positioned.")
        self.source_position = value
        self.source.position = value  # convert_to_openal_coordinates(*value)

    @property
    def max_distance(self):
        return self.source.max_distance

    @max_distance.setter
    def max_distance(self, value):
        self.source.max_distance = value

    @property
    def reference_distance(self):
        return self.source.reference_distance

    @reference_distance.setter
    def reference_distance(self, value):
        self.source.reference_distance = value

    @property
    def rolloff_factor(self):
        return self.source.rolloff_factor

    @rolloff_factor.setter
    def rolloff_factor(self, value):
        self.source.rolloff_factor = value

    @property
    def volume(self):
        if not self.is_active:
            return 0.0
        return self.source.gain

    @volume.setter
    def volume(self, value):
        if self.is_active:
            self.source.gain = value

    @property
    def pitch(self):
        if not self.is_active:
            return 0.0
        return self.source.pitch

    @pitch.setter
    def pitch(self, value):
        if self.is_active:
            self.source.pitch = value

    # Audio Effects Methods
    def add_effect(self, effect_type: str, send_slot: int = 0, **kwargs) -> 'AudioEffect':
        """Add an audio effect to this sound.
        
        Args:
            effect_type: Type of effect ('reverb', 'distortion', 'echo', etc.)
            send_slot: Which auxiliary send slot to use (0-3)
            **kwargs: Effect parameters
        
        Returns:
            AudioEffect instance for further configuration
        """
        if not self.is_active:
            raise RuntimeError("Cannot add effects to inactive sound")
        
        # Get EFX extension using centralized manager
        try:
            efx = EfxManager.get_efx(self.ctx)
        except Exception as e:
            raise RuntimeError(f"EFX extension not available: {e}")
        
        effect = AudioEffect(efx)
        
        # Apply the requested effect type
        if effect_type == 'reverb':
            preset = kwargs.get('preset', 'room')
            effect.reverb(preset)
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
        
        # Send the source to the effect slot
        if effect.slot:
            efx.send(self.source, send_slot, effect.slot)
        
        self.applied_effects.append(effect)
        return effect
    
    def add_filter(self, filter_type: str, **kwargs) -> 'AudioFilter':
        """Add a filter directly to this sound source.
        
        Args:
            filter_type: Type of filter ('lowpass', 'highpass', 'bandpass')
            **kwargs: Filter parameters
        
        Returns:
            AudioFilter instance for further configuration
        """
        if not self.is_active:
            raise RuntimeError("Cannot add filters to inactive sound")
        
        # Get EFX extension using centralized manager
        try:
            efx = EfxManager.get_efx(self.ctx)
        except Exception as e:
            raise RuntimeError(f"EFX extension not available: {e}")
        
        audio_filter = AudioFilter(efx)
        
        # Apply the requested filter type
        if filter_type == 'lowpass':
            audio_filter.lowpass(**kwargs)
        elif filter_type == 'highpass':
            audio_filter.highpass(**kwargs)
        elif filter_type == 'bandpass':
            audio_filter.bandpass(**kwargs)
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")
        
        # Apply filter directly to source
        if audio_filter.filter:
            self.source.direct_filter = audio_filter.filter
            self.direct_filter = audio_filter
        
        self.applied_filters.append(audio_filter)
        return audio_filter
    
    def apply_filter_preset(self, preset_name: str):
        """Apply a predefined filter preset.
        
        Available presets: radio, telephone, muffled, thin, underwater, clear
        """
        presets = EffectPresets.get_filter_presets()
        if preset_name not in presets:
            raise ValueError(f"Unknown filter preset: {preset_name}. Available: {list(presets.keys())}")
        
        preset = presets[preset_name]
        filter_type = preset.pop('type')
        return self.add_filter(filter_type, **preset)
    
    def apply_reverb_preset(self, preset_name: str, send_slot: int = 0):
        """Apply a predefined reverb preset.
        
        Available presets: small_room, medium_room, large_hall, auditorium, underwater
        """
        presets = EffectPresets.get_reverb_presets()
        if preset_name not in presets:
            raise ValueError(f"Unknown reverb preset: {preset_name}. Available: {list(presets.keys())}")
        
        return self.add_effect('reverb', send_slot, preset=preset_name)
    
    def remove_all_effects(self):
        """Remove all applied effects from this sound."""
        if not self.is_active:
            return
        
        # Clear auxiliary sends
        if EfxManager.has_efx(self.ctx):
            efx = EfxManager.get_efx(self.ctx)
            for i in range(4):  # Clear all 4 auxiliary sends
                try:
                    efx.send(self.source, i, None)
                except:
                    pass
        
        self.applied_effects.clear()
    
    def remove_all_filters(self):
        """Remove all applied filters from this sound."""
        if not self.is_active:
            return
        
        # Clear direct filter
        try:
            if hasattr(self.source, 'direct_filter'):
                self.source.direct_filter = None
        except:
            pass
        
        self.direct_filter = None
        self.applied_filters.clear()
    
    def get_effect_count(self) -> int:
        """Get the number of applied effects."""
        return len(self.applied_effects)
    
    def get_filter_count(self) -> int:
        """Get the number of applied filters."""
        return len(self.applied_filters)
        
    # Destroy the sound.
    def close(self):
        # Clean up effects and filters first
        try:
            self.remove_all_effects()
            self.remove_all_filters()
        except:
            pass
        
        # Stop the source before cleanup
        try:
            if self.source and hasattr(self.source, 'stop'):
                self.source.stop()
        except:
            pass
        
        # Clean up OpenAL objects
        try:
            if hasattr(self, 'source') and self.source:
                self.source = None
        except:
            pass
        
        try:
            if hasattr(self, 'buffer') and self.buffer:
                # Don't delete shared buffers, just remove reference
                self.buffer = None
        except:
            pass


class URLSound:
    # Initialization. Context is passed to this class.
    def __init__(self, ctx=cyal.Context(cyal.Device(), make_current=True, hrtf_soft=1)):
        # The context passed to the Sound class for a sound to be played.
        self.ctx = ctx
        # The source and buffer, used later.
        self.source = None
        self.buffer = None
        self.buffer_size = 4096
        self.sample_rate = 44100
        self.format = cyal.BufferFormat.STEREO16
        #The stream, using requests to retrieve in chunks.
        self.stream = None
        # Controls whether a source is direct (does not move), or is able to be positioned, or not. The value will be changed accordingly with a property.
        self.is_direct = False
        # Controls the position of the source.
        self.source_position = [0.0, 0.0, 0.0]
        # Ffmpeg process.
        self.process = None

    def load(self, path, spatial_audio=False):
        # First generate a buffer.
        self.buffer = self.ctx.gen_buffer()
        # Make a source.
        self.source = self.ctx.gen_source()
        
        # Configure spatial audio based on parameter
        if spatial_audio:
            # Enable 3D positioning
            self.source.spatialize = True
            self.source.relative = False
            self.source.direct_channels = False
            self.source.position = [0.0, 0.0, 0.0]
            self.is_direct = False
        else:
            # Direct mode (default) - prevents static and positioning issues
            self.source.spatialize = False
            self.source.relative = True
            self.source.direct_channels = True
            self.source.position = [0.0, 0.0, 0.0]
            self.is_direct = True
            
        self.stream = requests.get(path, stream = True)

    def read(self):
        if not self.is_active:
            return
        
        try:
            # Load audio directly from stream
            audio = AudioSegment.from_file(io.BytesIO(self.stream.content))
        except Exception as e:
            print(f"Error loading audio: {e}")
            return
        
        try:
            # Get actual audio properties
            channels = audio.channels
            actual_sample_rate = audio.frame_rate
            
            # Normalize audio to prevent corruption and static
            # Convert to 16-bit PCM and ensure proper sample rate
            audio = audio.set_frame_rate(44100)  # Standardize sample rate
            audio = audio.set_sample_width(2)   # 16-bit samples
            
            # Apply gentle normalization to prevent clipping/static
            if audio.max_possible_amplitude > 0:
                normalized_audio = audio.normalize(headroom=0.1)  # Leave 10% headroom
            else:
                normalized_audio = audio
            
            pcm_data = normalized_audio.raw_data
            channels = normalized_audio.channels
            actual_sample_rate = normalized_audio.frame_rate
            
            # Set format based on actual channels
            if channels == 1:
                audio_format = cyal.BufferFormat.MONO16
            else:
                audio_format = cyal.BufferFormat.STEREO16
            
            print(f"  Audio info: {channels} channels, {actual_sample_rate}Hz, {len(pcm_data)} bytes")
            
            # Use standardized sample rate and normalized data
            self.buffer.set_data(
                pcm_data, format=audio_format, sample_rate=actual_sample_rate
            )
            
            # Update instance variables to reflect actual audio properties
            self.format = audio_format
            self.sample_rate = actual_sample_rate
            
        except Exception as e:
            print(f"Buffer Setting Error: {e}")
            return
        
        try:
            # Use queue_buffers method but ensure proper format
            self.source.queue_buffers(self.buffer)
        except Exception as e:
            print(f"Buffer Queuing Error: {e}")

    def play(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Is it a looped source? If yes, make it stop looping.
        if self.looping:
            self.looping = False
        self.source.play()
        return True

    # Play the source and make it loop, if it is active (see properties below).
    def play_looped(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Is it a looped source? If not, make it loop.
        if not self.looping:
            self.looping = True
        self.source.play()
        return True

    # Pause the source without restarting the sound completely.
    def pause(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Check if the source is already paused.
        if self.paused:
            return False
        self.source.pause()
        return True

    # Stop the source if it is active (see properties below).
    def stop(self):
        # Check if the source is active.
        if not self.is_active:
            return False
        # Check if the source is already stopped.
        if not self.is_playing:
            return False
        self.source.stop()
        return True

    # Properties
    # These are pretty much self explanatory so I won't go into any detail here.
    @property
    def is_active(self):
        if self.source:
            return True
        else:
            return False

    @property
    def is_playing(self):
        if not self.is_active:
            return False
        return bool(self.source.state == cyal.SourceState.PLAYING)

    @property
    def paused(self):
        if not self.is_active:
            return False
        return bool(self.source.state == cyal.SourceState.PAUSED)

    @property
    def looping(self):
        if not self.is_active:
            return False
        return bool(self.source.looping)

    @looping.setter
    def looping(self, value):
        if self.is_active:
            self.source.looping = value

    @property
    def direct(self):
        return self.is_direct

    @direct.setter
    def direct(self, value):
        if value != self.is_direct:
            if value:
                self.source.relative = True
                self.source.direct_channels = True
                self.position = [0.0, 0.0, 0.0]
                self.is_direct = True
            else:
                self.source.relative = False
                self.source.direct_channels = False
                self.is_direct = False

    @property
    def position(self):
        return self.source_position

    @position.setter
    def position(self, value):
        if self.is_direct:
            raise ValueError("Direct sources cannot be positioned.")
        self.source_position = value
        self.source.position = value  # convert_to_openal_coordinates(*value)

    @property
    def volume(self):
        if not self.is_active:
            return 0.0
        return self.source.gain

    @volume.setter
    def volume(self, value):
        if self.is_active:
            self.source.gain = value

    @property
    def pitch(self):
        if not self.is_active:
            return 0.0
        return self.source.pitch

    @pitch.setter
    def pitch(self, value):
        if self.is_active:
            self.source.pitch = value

    # Destroy the sound.
    def close(self):
        try:
            if hasattr(self, 'source') and self.source:
                self.source.stop()
                self.source = None
        except:
            pass
        try:
            if hasattr(self, 'buffer') and self.buffer:
                self.buffer = None
        except:
            pass
        try:
            if hasattr(self, 'stream') and self.stream:
                self.stream.close()
                self.stream = None
        except:
            pass


class StreamingSound:
    """
    Streaming sound class for large audio files (e.g., music).
    Loads and plays audio in chunks to avoid memory issues and provide instant playback.
    """
    
    def __init__(self, ctx=cyal.Context(cyal.Device(), make_current=True, hrtf_soft=1)):
        self.ctx = ctx
        self.source = None
        self.buffers = []
        self.buffer_queue = queue.Queue()
        self.is_streaming = False
        self.stream_thread = None
        self.filename = None
        
        # Streaming settings
        self.buffer_size = 4096 * 4  # Size of each audio chunk
        self.buffer_count = 4  # Number of buffers to queue
        self.sample_rate = 44100
        self.channels = 2
        
        # Audio format
        self.format = cyal.BufferFormat.STEREO16
        
        # Position and audio properties
        self.is_direct = True  # Streaming sounds are typically direct (music/ambient)
        self.source_position = [0.0, 0.0, 0.0]
        
        # Audio effects support
        self.applied_effects = []
        self.applied_filters = []
        self.direct_filter = None
        
        # State
        self.is_paused = False
        self.should_loop = False
        self.audio_file = None
    
    def load_stream(self, filename: str, chunk_size: int = None, preload_buffers: int = None):
        """
        Load an audio file for streaming.
        
        Args:
            filename: Path to the audio file
            chunk_size: Size of each audio chunk in bytes
            preload_buffers: Number of buffers to preload
        """
        self.filename = filename
        
        if chunk_size:
            self.buffer_size = chunk_size
        if preload_buffers:
            self.buffer_count = preload_buffers
        
        try:
            # Load audio file with pydub for format support
            self.audio_file = AudioSegment.from_file(filename)
            
            # Apply the same normalization fixes as URLSound
            # Normalize audio to prevent corruption and static
            self.audio_file = self.audio_file.set_frame_rate(44100)  # Standardize sample rate
            self.audio_file = self.audio_file.set_sample_width(2)   # 16-bit samples
            
            # Apply gentle normalization to prevent clipping/static
            if self.audio_file.max_possible_amplitude > 0:
                self.audio_file = self.audio_file.normalize(headroom=0.1)  # Leave 10% headroom
            
            # Get normalized audio properties
            self.sample_rate = self.audio_file.frame_rate
            self.channels = self.audio_file.channels
            
            # Set OpenAL format based on channels
            if self.channels == 1:
                self.format = cyal.BufferFormat.MONO16
            else:
                self.format = cyal.BufferFormat.STEREO16
            
            # Create OpenAL source
            self.source = self.ctx.gen_source()
            self.source.spatialize = not self.is_direct
            
            # Create streaming buffers
            self.buffers = self.ctx.gen_buffers(self.buffer_count)
            
            print(f"Streaming setup: {filename}")
            print(f"  Sample rate: {self.sample_rate} Hz")
            print(f"  Channels: {self.channels}")
            print(f"  Duration: {len(self.audio_file) / 1000:.1f} seconds")
            print(f"  Buffer size: {self.buffer_size} bytes")
            print(f"  Buffer count: {self.buffer_count}")
            
            return True
            
        except Exception as e:
            print(f"Error loading streaming audio '{filename}': {e}")
            return False
    
    def _stream_audio_data(self):
        """Stream audio data in a separate thread."""
        try:
            audio_data = self.audio_file.raw_data
            data_length = len(audio_data)
            position = 0
            
            while self.is_streaming:
                # Check if we need to queue more buffers
                queued = self.source.buffers_queued
                processed = self.source.buffers_processed
                
                # Unqueue processed buffers
                if processed > 0:
                    try:
                        processed_buffers = self.source.unqueue_buffers()
                    except:
                        # Fallback if API doesn't work as expected
                        processed_buffers = []
                    
                    # Refill processed buffers if there's more data
                    for buffer in processed_buffers:
                        if position < data_length:
                            # Get next chunk of audio data
                            chunk_end = min(position + self.buffer_size, data_length)
                            chunk_data = audio_data[position:chunk_end]
                            
                            if chunk_data:
                                # Set buffer data
                                buffer.set_data(chunk_data, sample_rate=self.sample_rate, format=self.format)
                                # Queue the buffer
                                self.source.queue_buffers(buffer)
                                position = chunk_end
                        
                        elif self.should_loop:
                            # Loop back to the beginning
                            position = 0
                
                # Check if source stopped playing and needs to be restarted
                if self.source.state != cyal.SourceState.PLAYING and not self.is_paused:
                    if queued > 0:  # Only restart if we have buffers queued
                        self.source.play()
                
                # Small delay to prevent excessive CPU usage
                threading.Event().wait(0.01)
                
        except Exception as e:
            print(f"Streaming error: {e}")
        finally:
            self.is_streaming = False
    
    def play(self, loop: bool = False):
        """Start streaming playback."""
        if not self.source or not self.audio_file:
            print("No audio loaded for streaming")
            return False
        
        if self.is_streaming:
            print("Already streaming")
            return False
        
        self.should_loop = loop
        self.is_streaming = True
        self.is_paused = False
        
        try:
            # Preload initial buffers
            audio_data = self.audio_file.raw_data
            position = 0
            
            for buffer in self.buffers:
                if position < len(audio_data):
                    chunk_end = min(position + self.buffer_size, len(audio_data))
                    chunk_data = audio_data[position:chunk_end]
                    
                    if chunk_data:
                        buffer.set_data(chunk_data, sample_rate=self.sample_rate, format=self.format)
                        self.source.queue_buffers(buffer)
                        position = chunk_end
            
            # Start playback
            self.source.play()
            
            # Start streaming thread
            self.stream_thread = threading.Thread(target=self._stream_audio_data, daemon=True)
            self.stream_thread.start()
            
            print(f"Started streaming: {self.filename}")
            return True
            
        except Exception as e:
            print(f"Error starting stream: {e}")
            self.is_streaming = False
            return False
    
    def pause(self):
        """Pause streaming playback."""
        if self.source and self.is_streaming:
            self.source.pause()
            self.is_paused = True
            print("Streaming paused")
    
    def resume(self):
        """Resume streaming playback."""
        if self.source and self.is_streaming and self.is_paused:
            self.source.play()
            self.is_paused = False
            print("Streaming resumed")
    
    def stop(self):
        """Stop streaming playback."""
        if self.is_streaming:
            self.is_streaming = False
            self.is_paused = False
            
            if self.source:
                self.source.stop()
                
                # Unqueue all buffers
                try:
                    queued = self.source.buffers_queued
                    if queued > 0:
                        self.source.unqueue_buffers()
                except:
                    pass
            
            # Wait for streaming thread to finish
            if self.stream_thread and self.stream_thread.is_alive():
                self.stream_thread.join(timeout=1.0)
            
            print("Streaming stopped")
    
    def set_volume(self, volume: float):
        """Set the volume of the streaming audio."""
        if self.source:
            self.source.gain = max(0.0, min(1.0, volume))
    
    def set_pitch(self, pitch: float):
        """Set the pitch of the streaming audio."""
        if self.source:
            self.source.pitch = max(0.5, min(2.0, pitch))
    
    def set_position(self, x: float, y: float, z: float):
        """Set 3D position (only works if not direct)."""
        if not self.is_direct and self.source:
            self.source.position = [x, y, z]
            self.source_position = [x, y, z]
    
    def set_direct(self, direct: bool):
        """Set whether this is a direct (non-positioned) sound."""
        if self.source:
            self.is_direct = direct
            self.source.relative = direct
            self.source.direct_channels = direct
            if direct:
                self.source.position = [0.0, 0.0, 0.0]
    
    @property
    def is_playing(self):
        """Check if the stream is currently playing."""
        if self.source:
            return self.source.state == cyal.SourceState.PLAYING and self.is_streaming
        return False
    
    @property
    def volume(self):
        """Get current volume."""
        if self.source:
            return self.source.gain
        return 0.0
    
    @property
    def pitch(self):
        """Get current pitch."""
        if self.source:
            return self.source.pitch
        return 1.0
    
    def get_playback_position(self):
        """Get approximate playback position in seconds."""
        if self.source and self.audio_file:
            # This is an approximation based on processed buffers
            processed = self.source.buffers_processed
            bytes_per_second = self.sample_rate * self.channels * 2  # 16-bit = 2 bytes
            position_seconds = (processed * self.buffer_size) / bytes_per_second
            return position_seconds
        return 0.0
    
    def get_duration(self):
        """Get total duration in seconds."""
        if self.audio_file:
            return len(self.audio_file) / 1000.0
        return 0.0
    
    def add_effect(self, effect_type: str, send_slot: int = 0, **kwargs):
        """Add an audio effect to the streaming sound."""
        if not self.source:
            raise RuntimeError("Cannot add effects to inactive stream")
        
        # Get EFX extension using centralized manager
        try:
            efx = EfxManager.get_efx(self.ctx)
        except Exception as e:
            raise RuntimeError(f"EFX extension not available: {e}")
        
        effect = AudioEffect(efx)
        
        # Apply the requested effect type
        if effect_type == 'reverb':
            preset = kwargs.get('preset', 'room')
            effect.reverb(preset)
        elif effect_type == 'equalizer':
            effect.equalizer(**kwargs)
        else:
            raise ValueError(f"Effect type '{effect_type}' not supported for streaming audio")
        
        # Send the source to the effect slot
        if effect.slot:
            efx.send(self.source, send_slot, effect.slot)
        
        self.applied_effects.append(effect)
        return effect
    
    def close(self):
        """Clean up the streaming sound."""
        self.stop()
        
        # Clean up effects and filters
        for effect in self.applied_effects:
            try:
                del effect
            except:
                pass
        self.applied_effects.clear()
        
        # Clean up OpenAL objects
        if self.source:
            del self.source
        if self.buffers:
            for buffer in self.buffers:
                del buffer
        
        self.audio_file = None
        print(f"Streaming sound closed: {self.filename}")
