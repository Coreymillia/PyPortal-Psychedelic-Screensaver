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
import gc

# Force garbage collection
gc.collect()

class SimpleEffect:
    """Memory-efficient plasma effect"""
    
    def __init__(self):
        print("🌈 Starting simple plasma effect...")
        
        # Get display
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
        
        gc.collect()
        print(f"Free memory: {gc.mem_free()} bytes")
        
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

def main():
    """Main function"""
    try:
        effect = SimpleEffect()
        print("✅ Effect created, starting loop...")
        
        while True:
            effect.update()
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