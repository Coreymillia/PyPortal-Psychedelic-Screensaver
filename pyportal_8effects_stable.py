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
            MatrixEffect(),
            ColorMatrixEffect(),
            JuliaFractalEffect(),
            FireEffect(),
            StarfieldEffect(),
            SineWaveEffect(),
            StreamersEffect(),
        ]
        
        self.current_effect_index = 0
        self.current_effect = self.effects[0]
        
        print(f"✅ Screensaver ready with {len(self.effects)} effect(s)")
        print("⏰ Auto-scrolling every 10 seconds!")
        print("🎬 Effects: Plasma → Spiral → Matrix → Color Matrix → Julia Fractal → Fire → Starfield → Sine Waves → Streamers → repeat")
    
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

class MatrixEffect:
    """Classic green Matrix digital rain effect"""
    
    def __init__(self):
        print("💚 Creating Matrix digital rain effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Matrix parameters - use even smaller bitmap for performance
        self.columns = 20  # Number of character columns
        self.rows = 15     # Number of character rows
        
        # Create small palette (16 shades of green)
        self.palette = displayio.Palette(16)
        self._init_palette()
        
        # Create bitmap for matrix grid
        self.bitmap = displayio.Bitmap(self.columns, self.rows, 16)
        
        # Scale up to fill screen
        scale_x = self.width // self.columns
        scale_y = self.height // self.rows
        
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group with scaling
        self.group = displayio.Group(scale=min(scale_x, scale_y))
        self.group.append(self.tile_grid)
        
        # Matrix rain parameters
        self.drop_positions = [0] * self.columns  # Y position of each column's drop
        self.drop_speeds = [1] * self.columns     # Speed of each drop
        self.drop_active = [True] * self.columns  # Is drop falling
        
        # Initialize random drops
        import random
        for i in range(self.columns):
            self.drop_positions[i] = random.randint(-10, self.rows)
            self.drop_speeds[i] = random.choice([1, 2, 3])
            self.drop_active[i] = random.choice([True, False])
        
        # Animation params
        self.time = 0.0
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"💚 Matrix effect created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        
    def _init_palette(self):
        """Create Matrix green color palette"""
        for i in range(16):
            # Create gradient from black to bright green
            intensity = i / 15.0
            
            # Matrix green color (darker to brighter)
            r = 0
            g = int(intensity * 255)
            b = int(intensity * 50)  # Slight blue tint for authenticity
            
            self.palette[i] = (r, g, b)
    
    def update(self):
        """Update Matrix rain effect"""
        self.time += 0.1
        
        import random
        
        # Clear the bitmap first (black background)
        for y in range(self.rows):
            for x in range(self.columns):
                self.bitmap[x, y] = 0  # Black
        
        # Update each column's drop
        for col in range(self.columns):
            if self.drop_active[col]:
                # Draw the falling trail
                drop_y = int(self.drop_positions[col])
                
                # Draw trail (fade from bright to dark)
                for trail in range(8):  # Trail length
                    y = drop_y - trail
                    if 0 <= y < self.rows:
                        # Brightness fades with trail position
                        brightness = max(0, 15 - trail * 2)
                        if trail == 0:
                            brightness = 15  # Brightest at front
                        
                        self.bitmap[col, y] = brightness
                
                # Move drop down
                self.drop_positions[col] += self.drop_speeds[col] * 0.3
                
                # Reset drop if it goes off screen
                if self.drop_positions[col] > self.rows + 5:
                    self.drop_positions[col] = random.randint(-15, -5)
                    self.drop_speeds[col] = random.choice([1, 2, 3])
                    # Sometimes pause the drop
                    self.drop_active[col] = random.choice([True, True, True, False])
            else:
                # Randomly reactivate inactive drops
                if random.randint(0, 100) < 5:  # 5% chance per frame
                    self.drop_active[col] = True
                    self.drop_positions[col] = random.randint(-15, -5)

class ColorMatrixEffect:
    """Colorful Matrix with real text characters"""
    
    def __init__(self):
        print("🌈💻 Creating Colorful Matrix text effect...")
        
        # Import required libraries
        import terminalio
        from adafruit_display_text import label
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Text parameters
        self.char_width = 9  # Slightly wider spacing to fill screen
        self.char_height = 12
        self.columns = self.width // self.char_width  # ~40 columns
        self.rows = self.height // self.char_height   # ~20 rows
        
        # Character set for Matrix effect
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Create main group
        self.group = displayio.Group()
        
        # Matrix rain parameters
        self.drop_positions = [0] * self.columns
        self.drop_speeds = [1] * self.columns
        self.drop_active = [True] * self.columns
        self.drop_colors = [(0, 255, 0)] * self.columns  # Start with all green
        
        # Text labels for each character position (memory efficient approach)
        self.active_labels = []  # Only store labels for visible characters
        
        # Color palette for rainbow effect
        self.colors = [
            (0, 255, 0),    # Green
            (0, 255, 255),  # Cyan  
            (255, 0, 255),  # Magenta
            (255, 255, 0),  # Yellow
            (255, 0, 0),    # Red
            (0, 0, 255),    # Blue
            (255, 128, 0),  # Orange
            (128, 0, 255),  # Purple
        ]
        
        # Initialize random drops
        import random
        for i in range(self.columns):
            self.drop_positions[i] = random.randint(-20, self.rows)
            self.drop_speeds[i] = random.choice([0.5, 1, 1.5, 2])
            self.drop_active[i] = random.choice([True, False])
            self.drop_colors[i] = random.choice(self.colors)
        
        # Animation params
        self.time = 0.0
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"🌈💻 Color Matrix created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        # Clear existing labels
        for label_obj in self.active_labels:
            try:
                self.group.remove(label_obj)
            except ValueError:
                pass
        self.active_labels.clear()
    
    def update(self):
        """Update colorful Matrix text effect"""
        self.time += 0.1
        
        import random
        import terminalio
        from adafruit_display_text import label
        
        # Clear old labels (keep only recent ones for performance)
        labels_to_remove = []
        for label_obj in self.active_labels:
            # Remove labels that are too far down or too old
            if hasattr(label_obj, '_matrix_age'):
                label_obj._matrix_age += 1
                if label_obj._matrix_age > 50:  # Remove after 50 frames
                    labels_to_remove.append(label_obj)
        
        for label_obj in labels_to_remove:
            try:
                self.group.remove(label_obj)
                self.active_labels.remove(label_obj)
            except (ValueError, AttributeError):
                pass
        
        # Update each column's drop
        for col in range(min(self.columns, 35)):  # Increased to fill more screen
            if self.drop_active[col]:
                drop_y = int(self.drop_positions[col])
                
                # Add new character at drop position
                if 0 <= drop_y < self.rows and random.randint(0, 3) == 0:  # Don't add every frame
                    char = random.choice(self.characters)
                    
                    try:
                        text_label = label.Label(
                            terminalio.FONT,
                            text=char,
                            color=self.drop_colors[col],
                            x=col * self.char_width,
                            y=drop_y * self.char_height + 8
                        )
                        text_label._matrix_age = 0  # Track age for cleanup
                        
                        self.group.append(text_label)
                        self.active_labels.append(text_label)
                        
                    except (MemoryError, RuntimeError):
                        # If memory is tight, skip this character
                        pass
                
                # Move drop down
                self.drop_positions[col] += self.drop_speeds[col] * 0.4
                
                # Reset drop if it goes off screen
                if self.drop_positions[col] > self.rows + 5:
                    self.drop_positions[col] = random.randint(-25, -5)
                    self.drop_speeds[col] = random.choice([0.5, 1, 1.5, 2])
                    self.drop_colors[col] = random.choice(self.colors)
                    self.drop_active[col] = random.choice([True, True, False])
            else:
                # Randomly reactivate drops
                if random.randint(0, 150) < 3:  # Lower chance for performance
                    self.drop_active[col] = True
                    self.drop_positions[col] = random.randint(-25, -5)
                    self.drop_colors[col] = random.choice(self.colors)

class JuliaFractalEffect:
    """Animated Julia Set fractal with color cycling"""
    
    def __init__(self):
        print("🌀🎨 Creating Julia fractal effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Create palette (64 colors for fractal gradients)
        self.palette = displayio.Palette(64)
        self._init_palette()
        
        # Create bitmap - half resolution for performance
        self.bitmap = displayio.Bitmap(self.width//2, self.height//2, 64)
        
        # Scale up to fill screen
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group
        self.group = displayio.Group(scale=2)
        self.group.append(self.tile_grid)
        
        # Fractal parameters
        self.zoom = 1.5
        self.center_x = -0.7
        self.center_y = 0.0
        self.max_iterations = 20  # Lower for performance
        
        # Julia set parameters (these create the fractal shape)
        self.c_real = -0.4
        self.c_imag = 0.6
        
        # Animation parameters
        self.time = 0.0
        self.color_offset = 0.0
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"🌀🎨 Julia fractal created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        self.color_offset = 0.0
        
    def _init_palette(self):
        """Create fractal color palette"""
        for i in range(64):
            if i == 0:
                # Inside the set - black
                self.palette[i] = (0, 0, 0)
            else:
                # Escape time coloring with psychedelic colors
                t = i / 63.0
                
                # Create multiple color bands
                r = int(127 + 127 * math.sin(t * math.pi * 6))
                g = int(127 + 127 * math.sin(t * math.pi * 4 + 2))
                b = int(127 + 127 * math.sin(t * math.pi * 8 + 4))
                
                # Add some intensity variation
                intensity = 0.7 + 0.3 * math.sin(t * math.pi * 12)
                r = int(r * intensity)
                g = int(g * intensity)
                b = int(b * intensity)
                
                # Ensure valid range
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                self.palette[i] = (r, g, b)
    
    def _julia_iteration(self, x, y):
        """Calculate Julia set iterations for given point"""
        # Convert screen coordinates to complex plane
        zx = (x / (self.width//2) - 0.5) * 4.0 / self.zoom + self.center_x
        zy = (y / (self.height//2) - 0.5) * 4.0 / self.zoom + self.center_y
        
        # Julia set iteration: z = z^2 + c
        for i in range(self.max_iterations):
            if zx*zx + zy*zy > 4.0:  # Escaped
                return i
                
            # z = z^2 + c
            temp = zx*zx - zy*zy + self.c_real
            zy = 2*zx*zy + self.c_imag
            zx = temp
            
        return 0  # Did not escape
    
    def update(self):
        """Update Julia fractal animation"""
        self.time += 0.05
        self.color_offset += 1.0
        
        # Animate Julia set parameters for morphing effect
        self.c_real = -0.4 + 0.3 * math.sin(self.time * 0.5)
        self.c_imag = 0.6 + 0.2 * math.cos(self.time * 0.7)
        
        # Slight zoom animation
        self.zoom = 1.5 + 0.3 * math.sin(self.time * 0.3)
        
        # Generate fractal (render every other pixel for performance)
        for y in range(0, self.height//2, 2):
            for x in range(0, self.width//2, 2):
                # Calculate iterations
                iterations = self._julia_iteration(x, y)
                
                # Convert to color with animation
                if iterations == 0:
                    color_index = 0  # Inside set - black
                else:
                    color_index = int((iterations + self.color_offset) % 63) + 1
                
                # Fill 2x2 block for performance
                self.bitmap[x, y] = color_index
                if x + 1 < self.width//2:
                    self.bitmap[x + 1, y] = color_index
                if y + 1 < self.height//2:
                    self.bitmap[x, y + 1] = color_index
                    if x + 1 < self.width//2:
                        self.bitmap[x + 1, y + 1] = color_index

class FireEffect:
    """Realistic fire simulation effect"""
    
    def __init__(self):
        print("🔥 Creating fire simulation effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Fire parameters - smaller grid for performance
        self.fire_width = 80  # Width of fire simulation
        self.fire_height = 60  # Height of fire simulation
        
        # Create palette (32 fire colors: black -> red -> orange -> yellow -> white)
        self.palette = displayio.Palette(32)
        self._init_fire_palette()
        
        # Create bitmap
        self.bitmap = displayio.Bitmap(self.fire_width, self.fire_height, 32)
        
        # Scale up to fill screen
        scale_x = self.width // self.fire_width
        scale_y = self.height // self.fire_height
        
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group with scaling
        self.group = displayio.Group(scale=min(scale_x, scale_y))
        self.group.append(self.tile_grid)
        
        # Fire simulation buffers
        self.fire_buffer = [[0 for _ in range(self.fire_width)] for _ in range(self.fire_height)]
        self.cooling_map = [[0 for _ in range(self.fire_width)] for _ in range(self.fire_height)]
        
        # Animation parameters
        self.time = 0.0
        
        # Initialize bottom row as hot fire source
        self._init_fire_source()
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"🔥 Fire effect created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        self._init_fire_source()
        
    def _init_fire_palette(self):
        """Create fire color palette - black to white through red/orange/yellow"""
        for i in range(32):
            # Intensity from 0 to 1
            intensity = i / 31.0
            
            if intensity < 0.3:
                # Black to dark red
                t = intensity / 0.3
                r = int(t * 128)
                g = 0
                b = 0
            elif intensity < 0.6:
                # Dark red to bright red
                t = (intensity - 0.3) / 0.3
                r = int(128 + t * 127)
                g = 0
                b = 0
            elif intensity < 0.8:
                # Red to orange
                t = (intensity - 0.6) / 0.2
                r = 255
                g = int(t * 165)  # Orange
                b = 0
            elif intensity < 0.95:
                # Orange to yellow
                t = (intensity - 0.8) / 0.15
                r = 255
                g = int(165 + t * 90)  # To 255
                b = int(t * 100)  # Add some blue for yellow
            else:
                # Yellow to white (hottest)
                t = (intensity - 0.95) / 0.05
                r = 255
                g = 255
                b = int(100 + t * 155)  # To full white
                
            # Ensure valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            self.palette[i] = (r, g, b)
    
    def _init_fire_source(self):
        """Initialize the bottom row as fire source"""
        # Set bottom row to maximum heat
        for x in range(self.fire_width):
            self.fire_buffer[self.fire_height - 1][x] = 31  # Maximum intensity
        
    def _update_fire_simulation(self):
        """Update the fire simulation using cellular automata"""
        import random
        
        # Process from bottom up (except bottom row which is heat source)
        for y in range(self.fire_height - 2, -1, -1):
            for x in range(self.fire_width):
                
                # Get heat from pixel below and neighbors
                heat_sum = 0
                heat_count = 0
                
                # Sample from below and around for heat diffusion
                for dx in [-1, 0, 1]:
                    for dy in [0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.fire_width and 0 <= ny < self.fire_height:
                            heat_sum += self.fire_buffer[ny][nx]
                            heat_count += 1
                
                # Average heat with some cooling and turbulence
                if heat_count > 0:
                    avg_heat = heat_sum / heat_count
                    
                    # Add cooling effect (fire cools as it rises)
                    cooling = random.randint(1, 3)
                    new_heat = max(0, int(avg_heat - cooling))
                    
                    # Add some randomness for flickering
                    if random.randint(0, 10) < 3:
                        new_heat = max(0, new_heat - random.randint(0, 2))
                    
                    self.fire_buffer[y][x] = min(31, new_heat)
                else:
                    self.fire_buffer[y][x] = 0
        
        # Refresh bottom row heat source with some variation
        for x in range(self.fire_width):
            base_heat = 28 + random.randint(-3, 3)  # 25-31 range
            self.fire_buffer[self.fire_height - 1][x] = max(20, min(31, base_heat))
    
    def update(self):
        """Update fire effect"""
        self.time += 0.1
        
        # Update fire simulation
        self._update_fire_simulation()
        
        # Copy fire buffer to bitmap
        for y in range(self.fire_height):
            for x in range(self.fire_width):
                heat_value = self.fire_buffer[y][x]
                self.bitmap[x, y] = heat_value

class StarfieldEffect:
    """Flying through space starfield effect"""
    
    def __init__(self):
        print("⭐ Creating starfield warp speed effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Create palette (16 colors: black to white for stars)
        self.palette = displayio.Palette(16)
        self._init_star_palette()
        
        # Create bitmap - half resolution for performance
        self.bitmap = displayio.Bitmap(self.width//2, self.height//2, 16)
        
        # Scale up to fill screen
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group
        self.group = displayio.Group(scale=2)
        self.group.append(self.tile_grid)
        
        # Star parameters
        self.num_stars = 150  # Number of stars
        self.stars = []
        
        # Center point (vanishing point)
        self.center_x = (self.width//2) // 2
        self.center_y = (self.height//2) // 2
        
        # Speed parameters
        self.base_speed = 1.0
        self.speed_variation = 0.0
        
        # Initialize stars
        self._init_stars()
        
        # Animation parameters
        self.time = 0.0
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"⭐ Starfield effect created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        self._init_stars()
        
    def _init_star_palette(self):
        """Create star color palette - black to bright white"""
        for i in range(16):
            # Gradient from black to white
            intensity = i / 15.0
            
            if i == 0:
                # Pure black for space
                r, g, b = 0, 0, 0
            else:
                # Various star intensities
                if intensity < 0.3:
                    # Dim blue stars
                    r = int(intensity * 100)
                    g = int(intensity * 100)  
                    b = int(intensity * 255)
                elif intensity < 0.7:
                    # White stars
                    value = int(intensity * 255)
                    r, g, b = value, value, value
                else:
                    # Bright white/blue stars
                    r = 255
                    g = 255
                    b = 255
            
            self.palette[i] = (r, g, b)
    
    def _init_stars(self):
        """Initialize star positions and properties"""
        import random
        
        self.stars = []
        for i in range(self.num_stars):
            # Random position around center
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(1, 100)
            
            star = {
                'x': self.center_x + distance * math.cos(angle),
                'y': self.center_y + distance * math.sin(angle),
                'z': random.uniform(1, 50),  # Depth
                'brightness': random.randint(5, 15),
                'speed': random.uniform(0.5, 2.0)
            }
            self.stars.append(star)
    
    def _reset_star(self, star):
        """Reset a star to the center with new random direction"""
        import random
        
        # New random direction from center
        angle = random.uniform(0, 2 * 3.14159)
        distance = random.uniform(1, 5)  # Start near center
        
        star['x'] = self.center_x + distance * math.cos(angle)
        star['y'] = self.center_y + distance * math.sin(angle)
        star['z'] = random.uniform(30, 50)  # Far away
        star['brightness'] = random.randint(5, 15)
        star['speed'] = random.uniform(0.5, 2.0)
    
    def update(self):
        """Update starfield animation"""
        self.time += 0.1
        
        # Add warp speed variation
        warp_factor = 1.0 + 0.5 * math.sin(self.time * 0.3)
        
        # Clear bitmap
        for y in range(self.height//2):
            for x in range(self.width//2):
                self.bitmap[x, y] = 0  # Black space
        
        # Update and draw stars
        for star in self.stars:
            # Move star away from center (perspective effect)
            dx = star['x'] - self.center_x
            dy = star['y'] - self.center_y
            
            # Move away from center
            star['x'] += dx * 0.02 * star['speed'] * warp_factor
            star['y'] += dy * 0.02 * star['speed'] * warp_factor
            star['z'] -= 0.5 * star['speed'] * warp_factor
            
            # Reset if star goes off screen or too close
            screen_x = int(star['x'])
            screen_y = int(star['y'])
            
            if (screen_x < 0 or screen_x >= self.width//2 or 
                screen_y < 0 or screen_y >= self.height//2 or 
                star['z'] < 1):
                self._reset_star(star)
                continue
            
            # Calculate star size and brightness based on distance
            size_factor = max(0.1, 30.0 / star['z'])
            brightness = int(star['brightness'] * size_factor)
            brightness = max(1, min(15, brightness))
            
            # Draw star
            try:
                self.bitmap[screen_x, screen_y] = brightness
                
                # Draw larger stars for close objects
                if size_factor > 1.5:
                    # Draw 2x2 star
                    if screen_x + 1 < self.width//2:
                        self.bitmap[screen_x + 1, screen_y] = brightness
                    if screen_y + 1 < self.height//2:
                        self.bitmap[screen_x, screen_y + 1] = brightness
                        if screen_x + 1 < self.width//2:
                            self.bitmap[screen_x + 1, screen_y + 1] = brightness
                            
            except IndexError:
                # Star went off screen
                self._reset_star(star)

class SineWaveEffect:
    """Multiple intersecting sine wave interference patterns"""
    
    def __init__(self):
        print("🌊 Creating sine wave interference effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Create palette (64 colors for smooth gradients)
        self.palette = displayio.Palette(64)
        self._init_wave_palette()
        
        # Create bitmap - half resolution for performance
        self.bitmap = displayio.Bitmap(self.width//2, self.height//2, 64)
        
        # Scale up to fill screen
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group
        self.group = displayio.Group(scale=2)
        self.group.append(self.tile_grid)
        
        # Wave parameters
        self.wave_sources = [
            {'x': 40, 'y': 30, 'freq': 0.2, 'amplitude': 1.0, 'phase': 0.0},
            {'x': 120, 'y': 30, 'freq': 0.15, 'amplitude': 0.8, 'phase': 1.57},
            {'x': 80, 'y': 90, 'freq': 0.25, 'amplitude': 0.9, 'phase': 3.14},
            {'x': 40, 'y': 90, 'freq': 0.18, 'amplitude': 0.7, 'phase': 4.71}
        ]
        
        # Animation parameters
        self.time = 0.0
        self.color_shift = 0.0
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"🌊 Sine wave effect created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        self.color_shift = 0.0
        
    def _init_wave_palette(self):
        """Create wave interference color palette"""
        for i in range(64):
            # Create smooth color transitions
            t = i / 63.0
            
            # Multiple color bands for interference patterns
            if t < 0.2:
                # Deep blue to cyan
                r = 0
                g = int(t * 5 * 255)
                b = 255
            elif t < 0.4:
                # Cyan to green
                s = (t - 0.2) / 0.2
                r = 0
                g = 255
                b = int(255 * (1 - s))
            elif t < 0.6:
                # Green to yellow
                s = (t - 0.4) / 0.2
                r = int(s * 255)
                g = 255
                b = 0
            elif t < 0.8:
                # Yellow to orange/red
                s = (t - 0.6) / 0.2
                r = 255
                g = int(255 * (1 - s * 0.5))
                b = 0
            else:
                # Orange/red to white
                s = (t - 0.8) / 0.2
                r = 255
                g = int(128 + s * 127)
                b = int(s * 255)
            
            # Ensure valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            self.palette[i] = (r, g, b)
    
    def _calculate_wave_interference(self, x, y):
        """Calculate wave interference at given point"""
        total_amplitude = 0.0
        
        # Calculate contribution from each wave source
        for source in self.wave_sources:
            # Distance from wave source
            dx = x - source['x']
            dy = y - source['y']
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Wave equation: amplitude * sin(frequency * distance + phase + time)
            wave_value = source['amplitude'] * math.sin(
                source['freq'] * distance + source['phase'] + self.time * 2
            )
            
            # Add distance-based attenuation for more realistic waves
            attenuation = 1.0 / (1.0 + distance * 0.01)
            total_amplitude += wave_value * attenuation
        
        return total_amplitude
    
    def update(self):
        """Update sine wave interference animation"""
        self.time += 0.08
        self.color_shift += 0.5
        
        # Animate wave sources for dynamic patterns
        for i, source in enumerate(self.wave_sources):
            # Move wave sources in circular patterns
            angle = self.time * 0.3 + i * 1.57  # Different phase for each source
            radius = 20 + 15 * math.sin(self.time * 0.2 + i)
            
            center_x = (self.width//2) // 2
            center_y = (self.height//2) // 2
            
            source['x'] = center_x + radius * math.cos(angle)
            source['y'] = center_y + radius * math.sin(angle)
            
            # Vary frequencies slightly for complex patterns
            base_freq = 0.1 + i * 0.05
            source['freq'] = base_freq + 0.05 * math.sin(self.time * 0.4 + i)
        
        # Generate wave interference pattern
        for y in range(self.height//2):
            for x in range(self.width//2):
                # Calculate wave interference
                wave_amplitude = self._calculate_wave_interference(x, y)
                
                # Convert to color index with color shifting
                color_value = (wave_amplitude + 2.0) / 4.0  # Normalize to 0-1
                color_index = int((color_value * 63 + self.color_shift) % 64)
                color_index = max(0, min(63, color_index))
                
                self.bitmap[x, y] = color_index

class StreamersEffect:
    """Moving wavy line streamers effect"""
    
    def __init__(self):
        print("📈 Creating wavy streamers effect...")
        
        # Display setup
        self.display = board.DISPLAY
        self.width = 320
        self.height = 240
        
        # Create palette (32 colors for streamers)
        self.palette = displayio.Palette(32)
        self._init_streamer_palette()
        
        # Create bitmap - half resolution for performance
        self.bitmap = displayio.Bitmap(self.width//2, self.height//2, 32)
        
        # Scale up to fill screen
        self.tile_grid = displayio.TileGrid(
            self.bitmap, 
            pixel_shader=self.palette,
            x=0, y=0,
            default_tile=0
        )
        
        # Create group
        self.group = displayio.Group(scale=2)
        self.group.append(self.tile_grid)
        
        # Streamer parameters
        self.num_streamers = 8
        self.streamers = []
        
        # Initialize streamers
        self._init_streamers()
        
        # Animation parameters
        self.time = 0.0
        
        # Initialize display
        self.reset()
        
        gc.collect()
        print(f"📈 Streamers effect created - Free memory: {gc.mem_free()} bytes")
    
    def reset(self):
        """Reset/initialize the effect display"""
        self.display.root_group = self.group
        self.time = 0.0
        self._init_streamers()
        
    def _init_streamer_palette(self):
        """Create rainbow streamer palette"""
        for i in range(32):
            if i == 0:
                # Black background
                self.palette[i] = (0, 0, 0)
            else:
                # Rainbow colors for streamers
                t = (i - 1) / 30.0
                angle = t * 2 * 3.14159
                
                # Create rainbow
                r = int(127 + 127 * math.sin(angle))
                g = int(127 + 127 * math.sin(angle + 2.094))
                b = int(127 + 127 * math.sin(angle + 4.188))
                
                # Boost saturation
                max_val = max(r, g, b)
                if max_val > 0:
                    scale = 255 / max_val
                    r = int(r * scale * 0.9)
                    g = int(g * scale * 0.9) 
                    b = int(b * scale * 0.9)
                
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                self.palette[i] = (r, g, b)
    
    def _init_streamers(self):
        """Initialize wavy streamers"""
        import random
        
        self.streamers = []
        for i in range(self.num_streamers):
            streamer = {
                'x_start': random.randint(-20, self.width//2 + 20),
                'y_base': random.randint(10, (self.height//2) - 10),
                'amplitude': random.uniform(5, 25),  # Wave height
                'frequency': random.uniform(0.05, 0.15),  # Wave frequency
                'speed': random.uniform(0.5, 2.0),  # Horizontal movement speed
                'phase': random.uniform(0, 6.28),  # Wave phase offset
                'color': random.randint(1, 31),  # Color index
                'thickness': random.randint(1, 3),  # Line thickness
                'direction': random.choice([-1, 1]),  # Move left or right
                'wave_speed': random.uniform(0.02, 0.08)  # How fast wave moves
            }
            self.streamers.append(streamer)
    
    def update(self):
        """Update wavy streamers animation"""
        self.time += 0.1
        
        import random
        
        # Clear bitmap
        for y in range(self.height//2):
            for x in range(self.width//2):
                self.bitmap[x, y] = 0  # Black background
        
        # Update and draw each streamer
        for streamer in self.streamers:
            # Move streamer horizontally
            streamer['x_start'] += streamer['speed'] * streamer['direction']
            
            # Update wave animation
            streamer['phase'] += streamer['wave_speed']
            
            # Reset streamer if it goes off screen
            if (streamer['direction'] > 0 and streamer['x_start'] > self.width//2 + 50) or \
               (streamer['direction'] < 0 and streamer['x_start'] < -50):
                # Reset from opposite side
                if streamer['direction'] > 0:
                    streamer['x_start'] = random.randint(-50, -20)
                else:
                    streamer['x_start'] = random.randint(self.width//2 + 20, self.width//2 + 50)
                
                # Randomize properties
                streamer['y_base'] = random.randint(10, (self.height//2) - 10)
                streamer['amplitude'] = random.uniform(5, 25)
                streamer['frequency'] = random.uniform(0.05, 0.15)
                streamer['speed'] = random.uniform(0.5, 2.0)
                streamer['color'] = random.randint(1, 31)
                streamer['thickness'] = random.randint(1, 3)
                streamer['wave_speed'] = random.uniform(0.02, 0.08)
            
            # Draw wavy line
            self._draw_wavy_streamer(streamer)
    
    def _draw_wavy_streamer(self, streamer):
        """Draw a single wavy streamer"""
        # Draw line segments to create wavy effect
        prev_x, prev_y = None, None
        
        # Draw streamer across visible width
        start_x = max(-10, min(self.width//2 + 10, int(streamer['x_start']) - 30))
        end_x = max(-10, min(self.width//2 + 10, int(streamer['x_start']) + 60))
        
        for x in range(start_x, end_x, 2):  # Step by 2 for performance
            if 0 <= x < self.width//2:
                # Calculate wavy y position
                wave_offset = streamer['amplitude'] * math.sin(
                    (x - streamer['x_start']) * streamer['frequency'] + streamer['phase']
                )
                y = int(streamer['y_base'] + wave_offset)
                
                # Draw thick line if needed
                for thickness in range(streamer['thickness']):
                    py = y + thickness - streamer['thickness']//2
                    if 0 <= py < self.height//2:
                        self.bitmap[x, py] = streamer['color']
                        
                        # Connect to previous point for smoother line
                        if prev_x is not None and prev_y is not None:
                            # Simple line drawing between points
                            if abs(x - prev_x) <= 2 and abs(py - prev_y) <= 4:
                                mid_y = (py + prev_y) // 2
                                if 0 <= mid_y < self.height//2 and 0 <= prev_x < self.width//2:
                                    self.bitmap[prev_x, mid_y] = streamer['color']
                
                prev_x, prev_y = x, y

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