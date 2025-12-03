# SPDX-FileCopyrightText: 2024 Psychedelic Screensaver Project
# SPDX-License-Identifier: MIT

"""
Mandelbrot Fractal Effect - Real-time Fractal Generation
========================================================

Animated Mandelbrot set with zooming and color cycling.
Optimized for real-time rendering on CircuitPython.
"""

import math
import displayio

class Mandelbrot:
    """Real-time animated Mandelbrot fractal"""
    
    def __init__(self, display):
        """Initialize Mandelbrot effect"""
        self.display = display
        self.width = display.width
        self.height = display.height
        
        # Create bitmap and palette
        self.bitmap = displayio.Bitmap(self.width, self.height, 256)
        self.palette = displayio.Palette(256)
        
        # Initialize fractal palette
        self._init_mandelbrot_palette()
        
        # Create display elements
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        self.group = displayio.Group()
        self.group.append(self.tile_grid)
        
        # Mandelbrot parameters
        self.zoom = 1.0
        self.zoom_speed = 1.02
        self.center_x = -0.5
        self.center_y = 0.0
        self.max_iterations = 32  # Reduced for performance
        
        # Animation parameters
        self.time = 0.0
        self.color_offset = 0.0
        
        # Zoom animation parameters
        self.zoom_center_x = -0.235125
        self.zoom_center_y = 0.827215
        self.zoom_cycle_time = 200  # Frames before zoom reset
        self.frame_count = 0
        
        print("🌀 Mandelbrot fractal effect initialized")
        
    def _init_mandelbrot_palette(self):
        """Initialize the Mandelbrot color palette"""
        for i in range(256):
            if i == 0:
                # Set color for points inside the set (black)
                self.palette[i] = (0, 0, 0)
            else:
                # Create gradient for escape time coloring
                t = i / 255.0
                
                # Multiple color bands for psychedelic effect
                r = int(127 + 127 * math.sin(t * math.pi * 4))
                g = int(127 + 127 * math.sin(t * math.pi * 4 + 2.094))
                b = int(127 + 127 * math.sin(t * math.pi * 4 + 4.188))
                
                # Add some variation
                r = int(r * (0.8 + 0.4 * math.sin(t * math.pi * 8)))
                g = int(g * (0.8 + 0.4 * math.sin(t * math.pi * 6)))
                b = int(b * (0.8 + 0.4 * math.sin(t * math.pi * 10)))
                
                # Ensure valid range
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                self.palette[i] = (r, g, b)
    
    def reset(self):
        """Reset effect parameters"""
        self.time = 0.0
        self.zoom = 1.0
        self.frame_count = 0
        self.color_offset = 0.0
        self.display.root_group = self.group
        
    def _mandelbrot_iteration(self, cx, cy):
        """Calculate Mandelbrot iterations for given complex point"""
        x, y = 0.0, 0.0
        
        for i in range(self.max_iterations):
            if x*x + y*y > 4.0:  # Escaped
                return i
                
            # z = z^2 + c
            temp = x*x - y*y + cx
            y = 2*x*y + cy
            x = temp
            
        return 0  # Did not escape (inside set)
    
    def _screen_to_complex(self, screen_x, screen_y):
        """Convert screen coordinates to complex plane coordinates"""
        # Calculate the complex plane bounds
        aspect_ratio = self.width / self.height
        plane_width = 4.0 / self.zoom
        plane_height = plane_width / aspect_ratio
        
        # Convert screen coordinates to complex plane
        cx = self.center_x + (screen_x / self.width - 0.5) * plane_width
        cy = self.center_y + (screen_y / self.height - 0.5) * plane_height
        
        return cx, cy
    
    def update(self):
        """Update one frame of Mandelbrot animation"""
        self.time += 0.1
        self.frame_count += 1
        
        # Animate zoom
        if self.frame_count < self.zoom_cycle_time:
            self.zoom *= self.zoom_speed
            # Move center towards interesting point
            t = self.frame_count / self.zoom_cycle_time
            self.center_x += (self.zoom_center_x - self.center_x) * 0.01
            self.center_y += (self.zoom_center_y - self.center_y) * 0.01
        else:
            # Reset zoom cycle
            self.frame_count = 0
            self.zoom = 1.0
            self.center_x = -0.5
            self.center_y = 0.0
            
        # Animate color palette
        self.color_offset += 2.0
        
        # Generate Mandelbrot fractal (optimized - render every other pixel for speed)
        for y in range(0, self.height, 2):
            for x in range(0, self.width, 2):
                # Convert screen coordinates to complex plane
                cx, cy = self._screen_to_complex(x, y)
                
                # Calculate iterations
                iterations = self._mandelbrot_iteration(cx, cy)
                
                # Convert to color index with animation
                if iterations == 0:
                    color_index = 0  # Inside set - black
                else:
                    color_index = int((iterations + self.color_offset) % 255) + 1
                    
                # Set pixel and fill 2x2 block for performance
                self.bitmap[x, y] = color_index
                if x + 1 < self.width:
                    self.bitmap[x + 1, y] = color_index
                if y + 1 < self.height:
                    self.bitmap[x, y + 1] = color_index
                    if x + 1 < self.width:
                        self.bitmap[x + 1, y + 1] = color_index