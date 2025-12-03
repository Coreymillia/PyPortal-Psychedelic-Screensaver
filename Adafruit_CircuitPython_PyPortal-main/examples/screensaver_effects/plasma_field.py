# SPDX-FileCopyrightText: 2024 Psychedelic Screensaver Project
# SPDX-License-Identifier: MIT

"""
Plasma Field Effect - Classic 1990s Plasma
==========================================

Mathematical sine wave interference patterns creating flowing plasma-like visuals.
Based on classic demoscene plasma effects.
"""

import math
import displayio

class PlasmaField:
    """Classic plasma field effect using sine wave interference"""
    
    def __init__(self, display):
        """Initialize plasma field effect"""
        self.display = display
        self.width = display.width
        self.height = display.height
        
        # Create bitmap and palette
        self.bitmap = displayio.Bitmap(self.width, self.height, 256)
        self.palette = displayio.Palette(256)
        
        # Initialize plasma palette (rainbow cycle)
        self._init_plasma_palette()
        
        # Create display elements
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        self.group = displayio.Group()
        self.group.append(self.tile_grid)
        
        # Animation parameters
        self.time = 0.0
        self.plasma_speed = 0.08
        self.plasma_scale = 16.0
        
        # Pre-calculate some values for performance
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        print("🌈 Plasma Field effect initialized")
        
    def _init_plasma_palette(self):
        """Initialize the plasma color palette"""
        for i in range(256):
            # Create smooth rainbow palette
            angle = (i / 255.0) * 2 * math.pi
            
            # RGB components with phase shifts for rainbow effect
            r = int(127 + 127 * math.sin(angle))
            g = int(127 + 127 * math.sin(angle + 2.094))  # 2π/3 phase shift
            b = int(127 + 127 * math.sin(angle + 4.188))  # 4π/3 phase shift
            
            # Ensure values are in valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g)) 
            b = max(0, min(255, b))
            
            self.palette[i] = (r, g, b)
    
    def reset(self):
        """Reset effect parameters"""
        self.time = 0.0
        self.display.root_group = self.group
        
    def update(self):
        """Update one frame of plasma animation"""
        self.time += self.plasma_speed
        
        # Generate plasma field
        for y in range(self.height):
            for x in range(self.width):
                # Multiple sine wave interference
                val1 = math.sin((x + self.time * 50) / self.plasma_scale)
                val2 = math.sin((y + self.time * 30) / self.plasma_scale)
                val3 = math.sin((x + y + self.time * 40) / self.plasma_scale)
                val4 = math.sin(math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2) / self.plasma_scale + self.time * 20)
                
                # Combine waves
                plasma_value = (val1 + val2 + val3 + val4) / 4.0
                
                # Convert to palette index (0-255)
                color_index = int((plasma_value + 1.0) * 127.5)
                color_index = max(0, min(255, color_index))
                
                # Set pixel
                self.bitmap[x, y] = color_index