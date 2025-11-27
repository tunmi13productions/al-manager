# AL Manager - Enhanced OpenAL Audio Library
# Copyright (c) 2025 tunmi13productions
# Licensed under the MIT License (see LICENSE file)

# EFX Manager - Centralized audio effects management
# This module provides a cleaner approach to managing EFX extensions

import cyal
import cyal.efx
from typing import Dict, Optional

class EfxManager:
    """Centralized manager for EFX extensions to avoid Context attribute issues."""
    
    _instances: Dict[cyal.Context, cyal.efx.EfxExtension] = {}
    
    @classmethod
    def get_efx(cls, context: cyal.Context) -> cyal.efx.EfxExtension:
        """Get or create EFX extension for a given context."""
        # Use context memory address as key since Context objects may not be hashable
        ctx_id = id(context)
        
        # Check if we already have an EFX extension for this context
        for ctx, efx in cls._instances.items():
            if id(ctx) == ctx_id:
                return efx
        
        # Create new EFX extension
        try:
            efx = cyal.efx.EfxExtension(context)
            cls._instances[context] = efx
            return efx
        except Exception as e:
            raise RuntimeError(f"Failed to create EFX extension: {e}")
    
    @classmethod
    def has_efx(cls, context: cyal.Context) -> bool:
        """Check if EFX extension exists for a given context."""
        ctx_id = id(context)
        return any(id(ctx) == ctx_id for ctx in cls._instances.keys())
    
    @classmethod
    def remove_efx(cls, context: cyal.Context):
        """Remove EFX extension for a given context."""
        to_remove = None
        for ctx in cls._instances.keys():
            if id(ctx) == id(context):
                to_remove = ctx
                break
        
        if to_remove:
            del cls._instances[to_remove]