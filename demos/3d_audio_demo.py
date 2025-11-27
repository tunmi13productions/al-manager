#!/usr/bin/env python3
"""
3D Audio Positioning Demo with Pygame
=====================================

This demo creates a visual representation of 3D audio positioning using pygame.
A sound source is placed at (0, 0, 0) and you can move around it to experience
how positional audio works with the enhanced AL Manager.

Controls:
- Left/Right Arrow Keys: Move along X-axis (left/right)
- Up/Down Arrow Keys: Move along Y-axis (forward/backward) 
- Page Up/Page Down: Move along Z-axis (up/down)
- Space: Toggle between different audio effects
- R: Reset listener position to origin
- ESC: Exit

Audio File: Make sure to have an audio file named 'test_sound.ogg' in the directory,
or update the AUDIO_FILE variable below.
"""

import pygame
import sys
import math
import time
import os
from al_manager.manager import Manager
from al_manager.lazy_effects import LAZY_REVERBS, LAZY_FILTERS, LAZY_COMBOS
# Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
AUDIO_FILE = "test.ogg"  # Update this to your audio file
MOVE_SPEED = 0.5
GRID_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class Audio3DDemo:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("3D Audio Positioning Demo - AL Manager Enhanced")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Initialize audio manager
        self.manager = Manager()
        
        # Listener position (you)
        self.listener_x = 5.0
        self.listener_y = 5.0 
        self.listener_z = 0.0
        
        # Sound source position (fixed at origin)
        self.source_x = 0.0
        self.source_y = 0.0
        self.source_z = 0.0
        
        # Lazy effects - now with maximum laziness!
        self.effects = [
            ("None", None, None),
            
            # REVERB PRESETS
            ("Bathroom", LAZY_REVERBS["bathroom"], None),
            ("Garage", LAZY_REVERBS["garage"], None),
            ("Stadium", LAZY_REVERBS["stadium"], None),
            ("Spaceship", LAZY_REVERBS["spaceship"], None),
            ("Underwater Cave", LAZY_REVERBS["underwater"], None),
            ("Wind Tunnel", LAZY_REVERBS["wind_tunnel"], None),
            
            # FILTER PRESETS  
            ("Walkie-Talkie", None, LAZY_FILTERS["walkie_talkie"]),
            ("Robot Voice", None, LAZY_FILTERS["robot"]),
            ("Old TV", None, LAZY_FILTERS["old_tv"]),
            ("Through Wall", None, LAZY_FILTERS["through_wall"]),
            ("Car Window", None, LAZY_FILTERS["car"]),
            
            # CRAZY COMBOS
            ("Drunk", 
             LAZY_COMBOS["drunk"]["effects"], 
             LAZY_COMBOS["drunk"]["filters"]),
            ("Ghost", 
             LAZY_COMBOS["ghost"]["effects"], 
             LAZY_COMBOS["ghost"]["filters"]),
            ("Time Warp", 
             LAZY_COMBOS["time_warp"]["effects"], 
             None),
            ("Robot Malfunction", 
             LAZY_COMBOS["robot_malfunction"]["effects"], 
             LAZY_COMBOS["robot_malfunction"]["filters"]),
            ("Psychedelic", 
             LAZY_COMBOS["psychedelic"]["effects"], 
             None),
            ("Nightmare", 
             LAZY_COMBOS["nightmare"]["effects"], 
             LAZY_COMBOS["nightmare"]["filters"]),
            ("Chipmunk", 
             LAZY_COMBOS["chipmunk"]["effects"], 
             LAZY_COMBOS["chipmunk"]["filters"]),
            ("Crystal Cave", 
             LAZY_COMBOS["crystal_cave"]["effects"], 
             None),
        ]
        self.current_effect = 0
        
        # Audio state
        self.sound_item = None
        self.is_playing = False
        
        # Visual settings
        self.zoom = 20  # Pixels per unit
        self.center_x = WINDOW_WIDTH // 2
        self.center_y = WINDOW_HEIGHT // 2
        
        # Try to start audio
        self.start_audio()
    
    def start_audio(self):
        """Start playing the audio file."""
        try:
            # Check if audio file exists
            if not os.path.exists(AUDIO_FILE):
                print(f"✗ Audio file not found: {AUDIO_FILE}")
                print(f"Please make sure the audio file exists in the current directory.")
                self.is_playing = False
                return
            
            # Stop any existing sound
            if self.sound_item:
                self.manager.destroy(self.sound_item)
            
            # Create sound with current effect
            effect_name, effects_config, filters_config = self.effects[self.current_effect]
            
            # Prepare effects and filters (make copies to avoid modifying originals)
            effects = None
            filters = None
            
            if effects_config:
                effects = []
                for effect in effects_config:
                    effects.append(dict(effect))
            
            if filters_config:
                filters = []
                for filt in filters_config:
                    filters.append(dict(filt))
            
            # Play the sound with effects and/or filters
            self.sound_item = self.manager.play_p(
                AUDIO_FILE,
                x=self.source_x,
                y=self.source_y,
                z=self.source_z,
                looping=True,
                volume=0.8,
                effects=effects,
                filters=filters
            )
            
            if self.sound_item:
                # Set initial positions
                self.sound_item.set_position(self.source_x, self.source_y, self.source_z)
                self.manager.update(self.listener_x, self.listener_y, self.listener_z)
                self.is_playing = True
                print(f"✓ Audio started with effect: {effect_name}")
            else:
                print(f"✗ Failed to load audio file: {AUDIO_FILE}")
                self.is_playing = False
                
        except Exception as e:
            print(f"✗ Audio error: {e}")
            import traceback
            traceback.print_exc()
            print(f"Make sure '{AUDIO_FILE}' exists in the current directory")
            self.is_playing = False
    
    def update_listener_position(self):
        """Update the listener position in the audio manager."""
        if self.is_playing and self.manager:
            self.manager.update(self.listener_x, self.listener_y, self.listener_z)
    
    def toggle_effect(self):
        """Switch to the next audio effect."""
        self.current_effect = (self.current_effect + 1) % len(self.effects)
        effect_name, _, _ = self.effects[self.current_effect]
        print(f"Switching to lazy effect: {effect_name}")
        self.start_audio()  # Restart with new effect
    
    def reset_position(self):
        """Reset listener to origin."""
        self.listener_x = 5.0
        self.listener_y = 5.0
        self.listener_z = 0.0
        self.update_listener_position()
        print(f"Reset listener position to ({self.listener_x:.1f}, {self.listener_y:.1f}, {self.listener_z:.1f})")
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = self.center_x + (world_x * self.zoom)
        screen_y = self.center_y - (world_y * self.zoom)  # Flip Y for screen coordinates
        return int(screen_x), int(screen_y)
    
    def draw_grid(self):
        """Draw a coordinate grid."""
        # Draw grid lines
        for i in range(-20, 21, 2):
            # Vertical lines (X axis)
            start_x, start_y = self.world_to_screen(i, -15)
            end_x, end_y = self.world_to_screen(i, 15)
            if 0 <= start_x <= WINDOW_WIDTH:
                pygame.draw.line(self.screen, LIGHT_GRAY, (start_x, start_y), (end_x, end_y), 1)
            
            # Horizontal lines (Y axis)
            start_x, start_y = self.world_to_screen(-20, i)
            end_x, end_y = self.world_to_screen(20, i)
            if 0 <= start_y <= WINDOW_HEIGHT:
                pygame.draw.line(self.screen, LIGHT_GRAY, (start_x, start_y), (end_x, end_y), 1)
        
        # Draw main axes
        # X-axis
        start_x, start_y = self.world_to_screen(-20, 0)
        end_x, end_y = self.world_to_screen(20, 0)
        pygame.draw.line(self.screen, GRAY, (start_x, start_y), (end_x, end_y), 2)
        
        # Y-axis
        start_x, start_y = self.world_to_screen(0, -15)
        end_x, end_y = self.world_to_screen(0, 15)
        pygame.draw.line(self.screen, GRAY, (start_x, start_y), (end_x, end_y), 2)
    
    def draw_sound_source(self):
        """Draw the sound source at origin."""
        source_screen_x, source_screen_y = self.world_to_screen(self.source_x, self.source_y)
        
        # Draw sound source as a pulsing circle
        pulse = int(10 + 5 * math.sin(pygame.time.get_ticks() * 0.01))
        pygame.draw.circle(self.screen, RED, (source_screen_x, source_screen_y), pulse, 3)
        pygame.draw.circle(self.screen, RED, (source_screen_x, source_screen_y), 5)
        
        # Label
        label = self.font.render("♪ Sound Source (0,0,0)", True, RED)
        self.screen.blit(label, (source_screen_x + 15, source_screen_y - 10))
    
    def draw_listener(self):
        """Draw the listener (you)."""
        listener_screen_x, listener_screen_y = self.world_to_screen(self.listener_x, self.listener_y)
        
        # Draw listener as a triangle pointing in direction
        size = 8
        points = [
            (listener_screen_x, listener_screen_y - size),      # Top
            (listener_screen_x - size, listener_screen_y + size), # Bottom left
            (listener_screen_x + size, listener_screen_y + size)   # Bottom right
        ]
        pygame.draw.polygon(self.screen, BLUE, points)
        
        # Draw Z-axis indicator (height)
        z_indicator_height = int(self.listener_z * 3)  # Scale for visibility
        if z_indicator_height != 0:
            start_y = listener_screen_y
            end_y = listener_screen_y - z_indicator_height
            color = GREEN if z_indicator_height > 0 else YELLOW
            pygame.draw.line(self.screen, color, 
                           (listener_screen_x, start_y), 
                           (listener_screen_x, end_y), 3)
        
        # Label
        label = self.font.render(f"👤 You ({self.listener_x:.1f}, {self.listener_y:.1f}, {self.listener_z:.1f})", True, BLUE)
        self.screen.blit(label, (listener_screen_x + 15, listener_screen_y + 10))
    
    def draw_distance_info(self):
        """Draw distance information."""
        # Calculate 3D distance
        dx = self.listener_x - self.source_x
        dy = self.listener_y - self.source_y
        dz = self.listener_z - self.source_z
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        # Draw distance line (2D projection)
        source_screen = self.world_to_screen(self.source_x, self.source_y)
        listener_screen = self.world_to_screen(self.listener_x, self.listener_y)
        pygame.draw.line(self.screen, YELLOW, source_screen, listener_screen, 2)
        
        # Distance text
        distance_text = self.font.render(f"3D Distance: {distance:.2f} units", True, WHITE)
        self.screen.blit(distance_text, (10, 10))
    
    def draw_info_panel(self):
        """Draw information panel."""
        info_y = 40
        line_height = 25
        
        # Current effect
        effect_name, effects_config, filters_config = self.effects[self.current_effect]
        
        # Show effect type info
        effect_info = f"Lazy Effect: {effect_name}"
        if effects_config and filters_config:
            effect_info += " (Effects + Filters)"
        elif effects_config:
            effect_info += " (Effects)"
        elif filters_config:
            effect_info += " (Filters)"
            
        effect_text = self.font.render(effect_info, True, WHITE)
        self.screen.blit(effect_text, (10, info_y))
        info_y += line_height
        
        # Audio status
        status = "Playing" if self.is_playing else "Stopped"
        status_color = GREEN if self.is_playing else RED
        status_text = self.font.render(f"Audio Status: {status}", True, status_color)
        self.screen.blit(status_text, (10, info_y))
        info_y += line_height * 2
        
        # Controls
        controls = [
            "Controls:",
            "← → : Move X-axis (left/right)",
            "↑ ↓ : Move Y-axis (forward/back)",
            "PgUp/PgDn : Move Z-axis (up/down)",
            "Space : Cycle lazy effects",
            "R : Reset position",
            "ESC : Exit",
            "",
            f"Effect {self.current_effect + 1}/{len(self.effects)}"
        ]
        
        for i, control in enumerate(controls):
            color = WHITE if i == 0 else LIGHT_GRAY
            font = self.font if i == 0 else self.small_font
            text = font.render(control, True, color)
            self.screen.blit(text, (10, info_y + i * 18))
    
    def handle_input(self):
        """Handle keyboard input."""
        keys = pygame.key.get_pressed()
        moved = False
        
        # Movement
        if keys[pygame.K_LEFT]:
            self.listener_x -= MOVE_SPEED
            moved = True
        if keys[pygame.K_RIGHT]:
            self.listener_x += MOVE_SPEED
            moved = True
        if keys[pygame.K_UP]:
            self.listener_y += MOVE_SPEED
            moved = True
        if keys[pygame.K_DOWN]:
            self.listener_y -= MOVE_SPEED
            moved = True
        if keys[pygame.K_PAGEUP]:
            self.listener_z += MOVE_SPEED
            moved = True
        if keys[pygame.K_PAGEDOWN]:
            self.listener_z -= MOVE_SPEED
            moved = True
        
        if moved:
            self.update_listener_position()
    
    def run(self):
        """Main game loop."""
        print("3D Audio Demo Started!")
        print(f"Audio file: {AUDIO_FILE}")
        print("Use arrow keys to move around the sound source...")
        
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.toggle_effect()
                    elif event.key == pygame.K_r:
                        self.reset_position()
            
            # Handle continuous input
            self.handle_input()
            
            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_sound_source()
            self.draw_listener()
            self.draw_distance_info()
            self.draw_info_panel()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # Cleanup
        if self.sound_item:
            self.manager.destroy(self.sound_item)
        self.manager.destroy_all()
        pygame.quit()

def main():
    """Main function."""
    print("3D Audio Positioning Demo - Now with LAZY EFFECTS!")
    print("=" * 50)
    print(f"Looking for audio file: {AUDIO_FILE}")
    
    # Check if audio file exists before starting
    if not os.path.exists(AUDIO_FILE):
        print(f"Warning: Audio file '{AUDIO_FILE}' not found!")
        print("You can:")
        print(f"1. Place an audio file named '{AUDIO_FILE}' in this directory")
        print("2. Or edit the AUDIO_FILE variable in the script to point to your audio file")
        print()
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            print("Exiting...")
            return
    
    print()
    print("Press SPACE to cycle through lazy effects like:")
    print("• Bathroom, Garage, Stadium reverbs")
    print("• Walkie-talkie, Robot voice filters") 
    print("• Crazy combos: Drunk, Time Warp, Nightmare!")
    print()
    
    try:
        demo = Audio3DDemo()
        demo.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Make sure you have:")
        print("1. pygame installed: pip install pygame")
        print("2. A valid audio file (test.ogg or update AUDIO_FILE)")
        print("3. OpenAL drivers installed")
        sys.exit(1)

if __name__ == "__main__":
    main()