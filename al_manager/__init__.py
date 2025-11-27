# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

# High-level wrapper for cyal (Cython OpenAL) with effects and filters

from .manager import *
from .effects import AudioEffect, AudioFilter, EffectPresets
from .efx_manager import EfxManager
from .sound_group import SoundGroup, create_player_sound_group, create_enemy_sound_group, create_npc_sound_group
from .sound import StreamingSound

__version__ = "2.0.0"
__author__ = "Enhanced by Claude"