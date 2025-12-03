# SPDX-FileCopyrightText: 2024 Psychedelic Screensaver Project  
# SPDX-License-Identifier: MIT

"""
Kaleidoscope Effect - Symmetrical Pattern Generator
==================================================

Rotating kaleidoscope with mirrored patterns and dynamic colors.
Creates symmetrical mandala-like patterns.
"""

import math
import displayio

class Kaleidoscope:
    """Symmetrical kaleidoscope pattern generator"""
    
    def __init__(self, display):
        """Initialize kaleidoscope effect"""
        self.display = display
        self.width = display.width
        self.height = display.height
        
        # Create bitmap and palette
        self.bitmap = displayio.Bitmap(self.width, self.height, 256)
        self.palette = displayio.Palette(256)
        
        # Initialize kaleidoscope palette
        self._init_kaleidoscope_palette()
        
        # Create display elements
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        self.group = displayio.Group()
        self.group.append(self.tile_grid)
        
        # Animation parameters
        self.time = 0.0
        self.rotation_speed = 0.02
        self.color_shift = 0.0
        self.symmetry_order = 6  # 6-fold symmetry
        
        # Center point
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        print("🔮 Kaleidoscope effect initialized")
        
    def _init_kaleidoscope_palette(self):
        """Initialize the kaleidoscope color palette"""
        for i in range(256):
            # Create vibrant kaleidoscope colors
            angle = (i / 255.0) * 4 * math.pi  # Multiple cycles for variety
            
            # Multiple color harmonics
            r = int(127 + 127 * math.sin(angle * 1.3))
            g = int(127 + 127 * math.sin(angle * 0.8 + math.pi/2))
            b = int(127 + 127 * math.sin(angle * 1.7 + math.pi))
            
            # Boost saturation for more vivid colors
            max_val = max(r, g, b)
            if max_val > 0:
                scale = 255 / max_val
                r = int(r * scale * 0.8)  # Slightly reduce to avoid oversaturation
                g = int(g * scale * 0.8)
                b = int(b * scale * 0.8)
            
            # Ensure valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            self.palette[i] = (r, g, b)
    
    def reset(self):
        """Reset effect parameters"""
        self.time = 0.0
        self.color_shift = 0.0
        self.display.root_group = self.group
        
    def _get_kaleidoscope_value(self, x, y):
        """Calculate kaleidoscope pattern value at given coordinates"""
        # Translate to center
        dx = x - self.center_x
        dy = y - self.center_y
        
        # Convert to polar coordinates
        radius = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        # Apply rotation
        angle += self.time
        
        # Create symmetrical pattern
        # Map angle to one segment and mirror
        segment_angle = (2 * math.pi) / self.symmetry_order
        angle_in_segment = angle % segment_angle
        
        # Mirror every other segment for kaleidoscope effect
        segment_num = int(angle // segment_angle) % (2 * self.symmetry_order)
        if segment_num % 2 == 1:
            angle_in_segment = segment_angle - angle_in_segment
            
        # Calculate pattern based on mirrored coordinates
        mirrored_x = radius * math.cos(angle_in_segment)
        mirrored_y = radius * math.sin(angle_in_segment)
        
        # Create complex pattern using multiple frequencies
        pattern1 = math.sin(mirrored_x * 0.1 + self.time * 2)
        pattern2 = math.cos(mirrored_y * 0.08 + self.time * 1.5)
        pattern3 = math.sin((mirrored_x + mirrored_y) * 0.06 + self.time)
        pattern4 = math.cos(radius * 0.05 + self.time * 0.8)
        
        # Combine patterns
        combined = (pattern1 + pattern2 + pattern3 + pattern4) / 4.0
        
        # Add radial component for more interesting structure
        radial = math.sin(radius * 0.02 + self.time * 0.5)
        combined = (combined + radial) / 2.0
        
        return combined
        
    def update(self):
        """Update one frame of kaleidoscope animation"""
        self.time += self.rotation_speed
        self.color_shift += 0.5
        
        # Generate kaleidoscope pattern
        for y in range(self.height):
            for x in range(self.width):
                # Get kaleidoscope pattern value
                pattern_value = self._get_kaleidoscope_value(x, y)
                
                # Convert to color index with color shifting
                color_base = (pattern_value + 1.0) * 127.5
                color_index = int((color_base + self.color_shift) % 256)
                color_index = max(0, min(255, color_index))
                
                # Set pixel
                self.bitmap[x, y] = color_index