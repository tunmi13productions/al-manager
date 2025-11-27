# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

# Audio Effects Module for AL Manager
# High-level wrappers for OpenAL EFX (Effects Extension)

import cyal
import cyal.efx
from typing import Optional, Dict, Any, Tuple

class AudioFilter:
    """High-level wrapper for OpenAL filters with easy-to-use methods."""
    
    def __init__(self, efx: cyal.efx.EfxExtension):
        self.efx = efx
        self.filter = None
        self._filter_type = None
    
    def lowpass(self, gain: float = 1.0, gainhf: float = 0.5, **kwargs):
        """Create a low-pass filter that reduces high frequencies.
        
        Args:
            gain: Overall gain (0.0 to 1.0, default 1.0)
            gainhf: High frequency gain (0.0 to 1.0, default 0.5)
            **kwargs: Additional filter parameters
        """
        self.filter = self.efx.gen_filter(type="lowpass")
        self.filter.set("gain", gain)
        self.filter.set("gainhf", gainhf)
        
        # Apply any additional custom parameters
        for param, value in kwargs.items():
            try:
                self.filter.set(param, value)
            except Exception as e:
                print(f"Warning: Failed to set lowpass parameter {param}={value}: {e}")
        
        self._filter_type = "lowpass"
        return self
    
    def highpass(self, gain: float = 1.0, gainlf: float = 0.5, **kwargs):
        """Create a high-pass filter that reduces low frequencies.
        
        Args:
            gain: Overall gain (0.0 to 1.0, default 1.0)
            gainlf: Low frequency gain (0.0 to 1.0, default 0.5)
            **kwargs: Additional filter parameters
        """
        self.filter = self.efx.gen_filter(type="highpass")
        self.filter.set("gain", gain)
        self.filter.set("gainlf", gainlf)
        
        # Apply any additional custom parameters
        for param, value in kwargs.items():
            try:
                self.filter.set(param, value)
            except Exception as e:
                print(f"Warning: Failed to set highpass parameter {param}={value}: {e}")
        
        self._filter_type = "highpass"
        return self
    
    def bandpass(self, gain: float = 1.0, gainlf: float = 0.5, gainhf: float = 0.5, **kwargs):
        """Create a band-pass filter that only allows frequencies in a specific range.
        
        Args:
            gain: Overall gain (0.0 to 1.0, default 1.0)
            gainlf: Low frequency gain (0.0 to 1.0, default 0.5)
            gainhf: High frequency gain (0.0 to 1.0, default 0.5)
            **kwargs: Additional filter parameters
        """
        self.filter = self.efx.gen_filter(type="bandpass")
        self.filter.set("gain", gain)
        self.filter.set("gainlf", gainlf)
        self.filter.set("gainhf", gainhf)
        
        # Apply any additional custom parameters
        for param, value in kwargs.items():
            try:
                self.filter.set(param, value)
            except Exception as e:
                print(f"Warning: Failed to set bandpass parameter {param}={value}: {e}")
        
        self._filter_type = "bandpass"
        return self
    
    def set_parameter(self, param: str, value: float):
        """Set a filter parameter directly."""
        if self.filter:
            self.filter.set(param, value)
    
    def get_parameter(self, param: str) -> float:
        """Get a filter parameter value."""
        if self.filter:
            return self.filter.get_float(param)
        return 0.0

class AudioEffect:
    """High-level wrapper for OpenAL effects with presets and easy configuration."""
    
    def __init__(self, efx: cyal.efx.EfxExtension):
        self.efx = efx
        self.effect = None
        self.slot = None
        self._effect_type = None
    
    def reverb(self, preset: str = None, **kwargs):
        """Apply reverb effect with preset configurations or custom parameters.
        
        Available presets: room, hall, cathedral, bathroom, cave, arena
        
        Custom parameters:
            density: Reverb modal density (0.0 to 1.0, default 1.0)
            diffusion: Reverb diffusion (0.0 to 1.0, default 1.0) 
            gain: Reverb gain (0.0 to 1.0, default 0.32)
            gainhf: High frequency gain (0.0 to 1.0, default 0.89)
            decay_time: Decay time in seconds (0.1 to 20.0, default 1.49)
            decay_hfratio: HF decay ratio (0.1 to 2.0, default 0.54)
            reflections_gain: Early reflections gain (0.0 to 3.16, default 0.05)
            reflections_delay: Early reflections delay (0.0 to 0.3, default 0.007)
            late_reverb_gain: Late reverb gain (0.0 to 10.0, default 1.26)
            late_reverb_delay: Late reverb delay (0.0 to 0.1, default 0.011)
        """
        self.effect = self.efx.gen_effect(type="reverb")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "reverb"
        
        # Use custom parameters if provided, otherwise use preset
        if kwargs:
            # Apply custom parameters
            for param, value in kwargs.items():
                try:
                    self.effect.set(param, value)
                except Exception as e:
                    print(f"Warning: Failed to set reverb parameter {param}={value}: {e}")
        elif preset:
            # Use preset configuration
            presets = {
                "room": {
                    "density": 1.0,
                    "diffusion": 1.0,
                    "gain": 0.32,
                    "gainhf": 0.89,
                    "decay_time": 1.49,
                    "decay_hfratio": 0.54,
                    "reflections_gain": 0.05,
                    "reflections_delay": 0.007,
                    "late_reverb_gain": 1.26,
                    "late_reverb_delay": 0.011
                },
                "hall": {
                    "density": 1.0,
                    "diffusion": 1.0,
                    "gain": 0.32,
                    "gainhf": 0.59,
                    "decay_time": 3.92,
                    "decay_hfratio": 0.70,
                    "reflections_gain": 0.24,
                    "reflections_delay": 0.020,
                    "late_reverb_gain": 1.26,
                    "late_reverb_delay": 0.030
                },
                "cathedral": {
                    "density": 1.0,
                    "diffusion": 1.0,
                    "gain": 0.32,
                    "gainhf": 0.62,
                    "decay_time": 5.04,
                    "decay_hfratio": 0.87,
                    "reflections_gain": 0.20,
                    "reflections_delay": 0.030,
                    "late_reverb_gain": 1.26,
                    "late_reverb_delay": 0.090
                },
                "bathroom": {
                    "density": 0.17,
                    "diffusion": 0.65,
                    "gain": 0.32,
                    "gainhf": 0.54,
                    "decay_time": 1.51,
                    "decay_hfratio": 1.25,
                    "reflections_gain": 0.65,
                    "reflections_delay": 0.025,
                    "late_reverb_gain": 1.26,
                    "late_reverb_delay": 0.030
                },
                "cave": {
                    "density": 1.0,
                    "diffusion": 1.0,
                    "gain": 0.32,
                    "gainhf": 1.0,
                    "decay_time": 2.91,
                    "decay_hfratio": 1.30,
                    "reflections_gain": 0.50,
                    "reflections_delay": 0.015,
                    "late_reverb_gain": 0.71,
                    "late_reverb_delay": 0.022
                },
                "arena": {
                    "density": 1.0,
                    "diffusion": 1.0,
                    "gain": 0.32,
                    "gainhf": 0.44,
                    "decay_time": 7.24,
                    "decay_hfratio": 0.33,
                    "reflections_gain": 0.26,
                    "reflections_delay": 0.020,
                    "late_reverb_gain": 1.01,
                    "late_reverb_delay": 0.030
                }
            }
            
            if preset in presets:
                for param, value in presets[preset].items():
                    self.effect.set(param, value)
        else:
            # Default to room preset if nothing specified
            preset = "room"
            self.reverb(preset=preset)
        
        self.slot.effect = self.effect
        return self
    
    def distortion(self, edge: float = 0.2, gain: float = 0.05, lowpass_cutoff: float = 8000.0):
        """Apply distortion effect.
        
        Args:
            edge: Distortion edge (0.0 to 1.0, default 0.2)
            gain: Distortion gain (0.01 to 1.0, default 0.05)
            lowpass_cutoff: Low-pass cutoff frequency (80 to 24000 Hz, default 8000)
        """
        self.effect = self.efx.gen_effect(type="distortion")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "distortion"
        
        self.effect.set("edge", edge)
        self.effect.set("gain", gain)
        self.effect.set("lowpass_cutoff", lowpass_cutoff)
        self.effect.set("eqcenter", 3600.0)
        self.effect.set("eqbandwidth", 3600.0)
        
        self.slot.effect = self.effect
        return self
    
    def echo(self, delay: float = 0.1, lr_delay: float = 0.1, damping: float = 0.5, 
             feedback: float = 0.5, spread: float = -1.0):
        """Apply echo effect.
        
        Args:
            delay: Echo delay in seconds (0.0 to 0.207, default 0.1)
            lr_delay: Left-right delay in seconds (0.0 to 0.404, default 0.1) 
            damping: Echo damping (0.0 to 0.99, default 0.5)
            feedback: Echo feedback (0.0 to 1.0, default 0.5)
            spread: Echo spread (-1.0 to 1.0, default -1.0)
        """
        self.effect = self.efx.gen_effect(type="echo")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "echo"
        
        self.effect.set("delay", delay)
        self.effect.set("lrdelay", lr_delay)
        self.effect.set("damping", damping)
        self.effect.set("feedback", feedback)
        self.effect.set("spread", spread)
        
        self.slot.effect = self.effect
        return self
    
    def chorus(self, waveform: int = 1, phase: int = 90, rate: float = 1.1, 
               depth: float = 0.1, feedback: float = 0.25, delay: float = 0.016):
        """Apply chorus effect.
        
        Args:
            waveform: Waveform type (0=sinusoid, 1=triangle, default 1)
            phase: Phase in degrees (-180 to 180, default 90)
            rate: Rate in Hz (0.0 to 10.0, default 1.1)
            depth: Depth (0.0 to 1.0, default 0.1)
            feedback: Feedback (-1.0 to 1.0, default 0.25)
            delay: Delay in seconds (0.0 to 0.016, default 0.016)
        """
        self.effect = self.efx.gen_effect(type="chorus")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "chorus"
        
        self.effect.set("waveform", waveform)
        self.effect.set("phase", phase)
        self.effect.set("rate", rate)
        self.effect.set("depth", depth)
        self.effect.set("feedback", feedback)
        self.effect.set("delay", delay)
        
        self.slot.effect = self.effect
        return self
    
    def flanger(self, waveform: int = 1, phase: int = 0, rate: float = 0.27,
                depth: float = 1.0, feedback: float = -0.5, delay: float = 0.002):
        """Apply flanger effect.
        
        Args:
            waveform: Waveform type (0=sinusoid, 1=triangle, default 1)
            phase: Phase in degrees (-180 to 180, default 0)
            rate: Rate in Hz (0.0 to 10.0, default 0.27)
            depth: Depth (0.0 to 1.0, default 1.0)
            feedback: Feedback (-1.0 to 1.0, default -0.5)
            delay: Delay in seconds (0.0 to 0.004, default 0.002)
        """
        self.effect = self.efx.gen_effect(type="flanger")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "flanger"
        
        self.effect.set("waveform", waveform)
        self.effect.set("phase", phase)
        self.effect.set("rate", rate)
        self.effect.set("depth", depth)
        self.effect.set("feedback", feedback)
        self.effect.set("delay", delay)
        
        self.slot.effect = self.effect
        return self
    
    def pitch_shift(self, coarse_tune: int = 12, fine_tune: int = 0):
        """Apply pitch shifting effect.
        
        Args:
            coarse_tune: Coarse tuning in semitones (-12 to 12, default 12)
            fine_tune: Fine tuning in cents (-50 to 50, default 0)
        """
        self.effect = self.efx.gen_effect(type="pitch_shifter")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "pitch_shifter"
        
        self.effect.set("coarse_tune", coarse_tune)
        self.effect.set("fine_tune", fine_tune)
        
        self.slot.effect = self.effect
        return self
    
    def auto_wah(self, attack_time: float = 0.06, release_time: float = 0.06,
                 resonance: float = 1000.0, peak_gain: float = 11.22):
        """Apply auto-wah effect.
        
        Args:
            attack_time: Attack time in seconds (0.0001 to 1.0, default 0.06)
            release_time: Release time in seconds (0.0001 to 1.0, default 0.06)
            resonance: Resonance (2.0 to 1000.0, default 1000.0)
            peak_gain: Peak gain in dB (0.00003 to 31622.78, default 11.22)
        """
        self.effect = self.efx.gen_effect(type="autowah")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "autowah"
        
        self.effect.set("attack_time", attack_time)
        self.effect.set("release_time", release_time)
        self.effect.set("resonance", resonance)
        self.effect.set("peak_gain", peak_gain)
        
        self.slot.effect = self.effect
        return self
    
    def compressor(self, enabled: bool = True):
        """Apply compressor effect.
        
        Args:
            enabled: Whether compressor is enabled (default True)
        """
        self.effect = self.efx.gen_effect(type="compressor")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "compressor"
        
        self.effect.set("onoff", 1 if enabled else 0)
        
        self.slot.effect = self.effect
        return self
    
    def equalizer(self, low_gain: float = 1.0, low_cutoff: float = 200.0,
                  mid1_gain: float = 1.0, mid1_center: float = 500.0, mid1_width: float = 1.0,
                  mid2_gain: float = 1.0, mid2_center: float = 3000.0, mid2_width: float = 1.0,
                  high_gain: float = 1.0, high_cutoff: float = 6000.0):
        """Apply 4-band equalizer effect.
        
        Args:
            low_gain: Low frequency gain (0.126 to 7.943, default 1.0)
            low_cutoff: Low frequency cutoff (50 to 800 Hz, default 200)
            mid1_gain: Mid1 frequency gain (0.126 to 7.943, default 1.0)
            mid1_center: Mid1 frequency center (200 to 3000 Hz, default 500)
            mid1_width: Mid1 frequency width (0.01 to 1.0, default 1.0)
            mid2_gain: Mid2 frequency gain (0.126 to 7.943, default 1.0)
            mid2_center: Mid2 frequency center (1000 to 8000 Hz, default 3000)
            mid2_width: Mid2 frequency width (0.01 to 1.0, default 1.0)
            high_gain: High frequency gain (0.126 to 7.943, default 1.0)
            high_cutoff: High frequency cutoff (4000 to 16000 Hz, default 6000)
        """
        self.effect = self.efx.gen_effect(type="equalizer")
        self.slot = self.efx.gen_auxiliary_effect_slot()
        self._effect_type = "equalizer"
        
        self.effect.set("low_gain", low_gain)
        self.effect.set("low_cutoff", low_cutoff)
        self.effect.set("mid1_gain", mid1_gain)
        self.effect.set("mid1_center", mid1_center)
        self.effect.set("mid1_width", mid1_width)
        self.effect.set("mid2_gain", mid2_gain)
        self.effect.set("mid2_center", mid2_center)
        self.effect.set("mid2_width", mid2_width)
        self.effect.set("high_gain", high_gain)
        self.effect.set("high_cutoff", high_cutoff)
        
        self.slot.effect = self.effect
        return self
    
    def set_parameter(self, param: str, value):
        """Set an effect parameter directly."""
        if self.effect:
            self.effect.set(param, value)
    
    def get_parameter(self, param: str):
        """Get an effect parameter value."""
        if self.effect:
            if isinstance(param, str) and param.isdigit():
                return self.effect.get_int(param)
            else:
                return self.effect.get_float(param)
        return None
    
    def set_gain(self, gain: float):
        """Set the overall effect gain."""
        if self.slot:
            self.slot.gain = gain

class EffectPresets:
    """Pre-defined effect configurations for common audio scenarios."""
    
    @staticmethod
    def get_reverb_presets() -> Dict[str, Dict[str, float]]:
        """Get all available reverb presets."""
        return {
            "small_room": {
                "density": 0.4,
                "diffusion": 0.83,
                "gain": 0.32,
                "gainhf": 0.89,
                "decay_time": 1.49,
                "decay_hfratio": 0.54,
                "reflections_gain": 0.05,
                "reflections_delay": 0.007,
                "late_reverb_gain": 1.26,
                "late_reverb_delay": 0.011
            },
            "medium_room": {
                "density": 0.6,
                "diffusion": 1.0,
                "gain": 0.32,
                "gainhf": 0.89,
                "decay_time": 2.3,
                "decay_hfratio": 0.54,
                "reflections_gain": 0.1,
                "reflections_delay": 0.010,
                "late_reverb_gain": 1.26,
                "late_reverb_delay": 0.015
            },
            "large_hall": {
                "density": 1.0,
                "diffusion": 1.0,
                "gain": 0.32,
                "gainhf": 0.59,
                "decay_time": 3.92,
                "decay_hfratio": 0.70,
                "reflections_gain": 0.24,
                "reflections_delay": 0.020,
                "late_reverb_gain": 1.26,
                "late_reverb_delay": 0.030
            },
            "auditorium": {
                "density": 1.0,
                "diffusion": 1.0,
                "gain": 0.32,
                "gainhf": 0.57,
                "decay_time": 4.32,
                "decay_hfratio": 0.59,
                "reflections_gain": 0.40,
                "reflections_delay": 0.020,
                "late_reverb_gain": 0.71,
                "late_reverb_delay": 0.030
            },
            "underwater": {
                "density": 0.36,
                "diffusion": 1.0,
                "gain": 0.32,
                "gainhf": 0.1,
                "decay_time": 1.49,
                "decay_hfratio": 0.1,
                "reflections_gain": 0.6,
                "reflections_delay": 0.007,
                "late_reverb_gain": 1.18,
                "late_reverb_delay": 0.025
            }
        }
    
    @staticmethod
    def get_filter_presets() -> Dict[str, Dict[str, float]]:
        """Get all available filter presets."""
        return {
            "radio": {"type": "bandpass", "gain": 1.0, "gainlf": 0.1, "gainhf": 0.3},
            "telephone": {"type": "bandpass", "gain": 1.0, "gainlf": 0.05, "gainhf": 0.1},
            "muffled": {"type": "lowpass", "gain": 1.0, "gainhf": 0.2},
            "thin": {"type": "highpass", "gain": 1.0, "gainlf": 0.2},
            "underwater": {"type": "lowpass", "gain": 0.9, "gainhf": 0.1},
            "clear": {"type": "lowpass", "gain": 1.0, "gainhf": 1.0}
        }