# SPDX-FileCopyrightText: 2024 Psychedelic Screensaver Project
# SPDX-License-Identifier: MIT

"""
PyPortal Simple Plasma Effect - Memory Optimized
===============================================

Simplified plasma effect optimized for PyPortal's limited memory.
"""

import board
import time
import math
import displayio
import touchio
import gc

# Force garbage collection
gc.collect()

class ScreensaverManager:
    """Manages multiple effects with touch control"""
    
    def __init__(self):
        print("🌈 Starting PyPortal Screensaver with touch control...")
        
        # Get display
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Auto-scroll setup (no touch for now)
        self.auto_scroll_time = 10.0  # 10 seconds between effects
        self.last_scroll_time = time.monotonic()
        
        # Effects list
        self.effects = [
            PlasmaEffect(),
            SpiralEffect(),
        ]
        
        self.current_effect_index = 0
        self.current_effect = self.effects[0]
        
        print(f"✅ Screensaver ready with {len(self.effects)} effect(s)")
        print("⏰ Auto-scrolling every 10 seconds!")
    
    def handle_auto_scroll(self):
        """Handle automatic effect scrolling"""
        current_time = time.monotonic()
        
        if (current_time - self.last_scroll_time) >= self.auto_scroll_time:
            self.next_effect()
            self.last_scroll_time = current_time
    
    def next_effect(self):
        """Switch to next effect"""
        self.current_effect_index = (self.current_effect_index + 1) % len(self.effects)
        self.current_effect = self.effects[self.current_effect_index]
        
        effect_name = self.current_effect.__class__.__name__
        print(f"🎨 Switched to: {effect_name}")
        
        # Reset the effect
        self.current_effect.reset()
    
    def update(self):
        """Main update loop"""
        self.handle_auto_scroll()
        self.current_effect.update()

class PlasmaEffect:
    """Memory-efficient plasma effect"""
    
    def __init__(self):
        print("🌊 Creating plasma effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Create small palette (64 colors instead of 256)
        self.palette = displayio.Palette(64)
        self._init_palette()
        
        # Create smaller bitmap 
        self.bitmap = displayio.Bitmap(self.width//2, self.height//2, 64)
        
        # Scale up the bitmap to fill screen
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group
        self.group = displayio.Group(scale=2)  # Scale 2x to fill screen
        self.group.append(self.tile_grid)
        
        self.display.root_group = self.group
        
        # Animation params
        self.time = 0.0
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"🧠 Plasma effect created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        
    def _init_palette(self):
        """Create rainbow palette with 64 colors"""
        for i in range(64):
            angle = (i / 63.0) * 2 * math.pi
            r = int(127 + 127 * math.sin(angle))
            g = int(127 + 127 * math.sin(angle + 2.094))
            b = int(127 + 127 * math.sin(angle + 4.188))
            self.palette[i] = (r, g, b)
    
    def update(self):
        """Update plasma effect"""
        self.time += 0.1
        
        # Render to smaller bitmap for performance
        for y in range(self.height//2):
            for x in range(self.width//2):
                # Simplified plasma calculation
                val = math.sin(x * 0.2 + self.time) + math.sin(y * 0.15 + self.time * 0.8)
                color_idx = int((val + 2.0) * 15.5) % 64
                self.bitmap[x, y] = color_idx

class SpiralEffect:
    """Rotating spiral effect"""
    
    def __init__(self):
        print("🌀 Creating spiral effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Create small palette (32 colors for variety)
        self.palette = displayio.Palette(32)
        self._init_palette()
        
        # Create smaller bitmap 
        self.bitmap = displayio.Bitmap(self.width//2, self.height//2, 32)
        
        # Scale up the bitmap to fill screen
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group
        self.group = displayio.Group(scale=2)  # Scale 2x to fill screen
        self.group.append(self.tile_grid)
        
        # Animation params
        self.time = 0.0
        self.rotation = 0.0
        
        # Center point
        self.center_x = (self.width//2) // 2
        self.center_y = (self.height//2) // 2
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"🌀 Spiral effect created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        self.rotation = 0.0
        
    def _init_palette(self):
        """Create spiral color palette"""
        for i in range(32):
            # Create blue-to-purple-to-pink gradient
            t = i / 31.0
            
            # Smooth color transitions
            r = int(50 + 205 * t * t)  # Starts low, ramps up
            g = int(20 + 100 * math.sin(t * math.pi))  # Bell curve
            b = int(255 - 100 * t)  # Starts high, drops
            
            # Ensure valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            self.palette[i] = (r, g, b)
    
    def update(self):
        """Update spiral effect"""
        self.time += 0.08
        self.rotation += 0.05
        
        # Render spiral pattern
        for y in range(self.height//2):
            for x in range(self.width//2):
                # Calculate distance from center
                dx = x - self.center_x
                dy = y - self.center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Calculate angle
                angle = math.atan2(dy, dx)
                
                # Create spiral pattern
                spiral_value = math.sin(distance * 0.3 - self.time * 3 + angle * 2 + self.rotation)
                
                # Add some radial component
                radial = math.cos(distance * 0.1 + self.time)
                
                # Combine patterns
                combined = (spiral_value + radial) / 2.0
                
                # Convert to color index
                color_idx = int((combined + 1.0) * 15.5) % 32
                
                self.bitmap[x, y] = color_idx

def main():
    """Main function"""
    try:
        manager = ScreensaverManager()
        print("🚀 Starting screensaver loop...")
        
        while True:
            manager.update()
            time.sleep(0.1)  # ~10 FPS
            
    except MemoryError as e:
        print(f"❌ Memory Error: {e}")
        print(f"Free memory: {gc.mem_free()} bytes")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)

# Auto-run
main()