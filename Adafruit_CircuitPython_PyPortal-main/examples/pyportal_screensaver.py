# SPDX-FileCopyrightText: 2024 Psychedelic Screensaver Project
# SPDX-License-Identifier: MIT

"""
PyPortal Psychedelic Screensaver Framework
==========================================

Main screensaver that cycles through 60 visual effects.
Touch screen to advance to next effect.
"""

import board
import time
import digitalio
import touchio
import displayio
from adafruit_pyportal import PyPortal

# Import effect modules
from screensaver_effects.plasma_field import PlasmaField
from screensaver_effects.kaleidoscope import Kaleidoscope  
from screensaver_effects.mandelbrot import Mandelbrot

class PyPortalScreensaver:
    """Main screensaver class that manages effects and user interaction"""
    
    def __init__(self):
        """Initialize the screensaver system"""
        print("🌈 Initializing PyPortal Psychedelic Screensaver...")
        
        # Initialize PyPortal
        self.pyportal = PyPortal(status_neopixel=board.NEOPIXEL)
        self.display = board.DISPLAY
        
        # Screen dimensions
        self.width = self.display.width   # 320
        self.height = self.display.height # 240
        
        # Touch screen setup
        self.touch = touchio.TouchIn(board.TOUCH_XL)
        self.last_touch_time = 0
        self.touch_debounce = 0.5  # 500ms debounce
        
        # Effect management
        self.effects = [
            PlasmaField(self.display),
            Kaleidoscope(self.display),
            Mandelbrot(self.display)
        ]
        
        self.current_effect_index = 0
        self.current_effect = self.effects[0]
        
        # Timing
        self.auto_advance_time = 30.0  # Auto-advance every 30 seconds
        self.last_advance_time = time.monotonic()
        self.frame_time = 1.0 / 15.0   # Target 15 FPS
        self.last_frame_time = 0
        
        print(f"✅ Screensaver initialized with {len(self.effects)} effects")
        print("Touch screen to cycle effects, auto-advance every 30s")
        
    def handle_touch(self):
        """Handle touch screen input to advance effects"""
        current_time = time.monotonic()
        
        if self.touch.value and (current_time - self.last_touch_time) > self.touch_debounce:
            self.advance_effect()
            self.last_touch_time = current_time
            
    def advance_effect(self):
        """Advance to the next effect"""
        self.current_effect_index = (self.current_effect_index + 1) % len(self.effects)
        self.current_effect = self.effects[self.current_effect_index]
        self.current_effect.reset()
        self.last_advance_time = time.monotonic()
        
        effect_name = self.current_effect.__class__.__name__
        print(f"🎨 Switched to effect {self.current_effect_index + 1}: {effect_name}")
        
    def update(self):
        """Main update loop - call this continuously"""
        current_time = time.monotonic()
        
        # Handle touch input
        self.handle_touch()
        
        # Auto-advance effects
        if (current_time - self.last_advance_time) > self.auto_advance_time:
            self.advance_effect()
            
        # Update current effect at target framerate
        if (current_time - self.last_frame_time) >= self.frame_time:
            self.current_effect.update()
            self.last_frame_time = current_time
            
    def run(self):
        """Run the screensaver (blocking loop)"""
        print("🚀 Starting screensaver loop...")
        
        try:
            while True:
                self.update()
                time.sleep(0.01)  # Small sleep to prevent watchdog issues
                
        except KeyboardInterrupt:
            print("\n🛑 Screensaver stopped by user")
            
        except Exception as e:
            print(f"❌ Error in screensaver: {e}")
            raise


class EffectBase:
    """Base class for all visual effects"""
    
    def __init__(self, display):
        """Initialize effect with display reference"""
        self.display = display
        self.width = display.width
        self.height = display.height
        
        # Create bitmap and palette for this effect
        self.bitmap = displayio.Bitmap(self.width, self.height, 256)
        self.palette = displayio.Palette(256)
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        
        # Create display group
        self.group = displayio.Group()
        self.group.append(self.tile_grid)
        
        # Animation parameters
        self.time = 0.0
        self.frame_count = 0
        
        # Set initial display group
        self.display.root_group = self.group
        
    def reset(self):
        """Reset effect parameters (called when switching to this effect)"""
        self.time = 0.0
        self.frame_count = 0
        self.display.root_group = self.group
        
    def update(self):
        """Update one frame of animation - override in subclasses"""
        self.time += 0.1
        self.frame_count += 1
        # Subclasses should implement their animation here
        

def main():
    """Main function to run the screensaver"""
    screensaver = PyPortalScreensaver()
    screensaver.run()


if __name__ == "__main__":
    main()