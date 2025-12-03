# PyPortal Psychedelic Screensavers

**Transform your Adafruit PyPortal into a mesmerizing psychedelic art display!**

This project ports the ESP32 60-effect screensaver collection to CircuitPython for the Adafruit PyPortal. Each effect is mathematically generated in real-time for endless variety.

## Project Status: IN DEVELOPMENT 🚧

**Goal:** Port all 60 effects from ESP32 C++ to CircuitPython  
**Target Hardware:** Adafruit PyPortal (320x240 TFT display)  
**Language:** CircuitPython using `displayio` (minimal memory footprint)

**⚠️ Memory Constraints Discovered:**
- PyPortal has limited RAM (~192KB available)
- Full resolution effects (320x240x256 colors) cause memory allocation failures
- Strategy: Build optimized effects from scratch using baseline

## Effects List (60 Total)

### ✅ Completed Effects
- [x] **Baseline Plasma** - Simple working plasma effect (160x120, 64 colors)
  - File: `pyportal_baseline_working.py` 
  - Status: ✅ Works but reboots after 1-2 minutes (memory leak)
  - Next: Fix memory leak, add garbage collection

### 🚧 In Progress  
- [ ] 1. Plasma Field Enhanced - Multi-wave plasma with better memory management
- [ ] 2. Simple Kaleidoscope - Memory-optimized symmetrical patterns
- [ ] 3. Basic Mandelbrot - Low-iteration fractal

### 📋 TODO Effects (4-60)
- [ ] 4. Matrix Rain - Digital rain effect
- [ ] 5. Fire - Flame simulation
- [ ] 6. Bouncing Balls - Physics-based animation
- [ ] 7. Spirals - Mathematical spiral patterns
- [ ] 8. Waves - Sine wave interference
- [ ] 9. Sierpinski - Triangle fractal
- [ ] 10. Starfield - Moving star field
- [ ] 11. DNA Helix - Double helix animation
- [ ] 12. Neon Rain - Colorful particle rain
- [ ] 13. Heavy Rain - Dense rain simulation
- [ ] 14. Micro Dots - Particle system
- [ ] 15. Raindrops - Water drop effect
- [ ] 16. Dragon Curve - Fractal dragon
- [ ] 17. Tunnel - 3D tunnel effect
- [ ] 18. Lissajous - Mathematical curves
- [ ] 19. Fireworks - Explosion particles
- [ ] 20. Lightning - Electric bolts
- [ ] 21. Hypno Vortex - Hypnotic spiral
- [ ] 22. Voronoi Lava - Cellular patterns
- [ ] 23. Aurora - Northern lights
- [ ] 24. Moire Mandala - Interference patterns
- [ ] 25. Interference Rings - Wave interference
- [ ] 26. CRT Vector - Retro vector graphics
- [ ] 27. Laser Show - Beam effects
- [ ] 28. Smoke Trails - Particle trails
- [ ] 29. Glitch Art - Digital corruption
- [ ] 30. Watercolor - Paint-like effects
- [ ] 31. Quasicrystal - Mathematical crystals
- [ ] 32. Hyperbolic Grid - Non-Euclidean geometry
- [ ] 33. Strange Attractor - Chaos mathematics
- [ ] 34. Cellular Automata - Conway's Game variants
- [ ] 35. Crystal Growth - Crystalline patterns
- [ ] 36. Quantum Tunnels - Particle physics
- [ ] 37. Fractal Sparks - Spark particle system
- [ ] 38. Voronoi Bloom - Growing cellular patterns
- [ ] 39. Perlin Nebula - Noise-based clouds
- [ ] 40. Fractal Mosaic - Tiled fractal patterns
- [ ] 41. Snowfall - Winter particle system
- [ ] 42. Meteor Shower - Space debris
- [ ] 43. Hexagon Grid - Honeycomb patterns
- [ ] 44. Sine Waves Grid - Mathematical grid
- [ ] 45. RGB Shift - Color channel effects
- [ ] 46. TV Static - Random noise
- [ ] 47. Particle Fountain - Upward particles
- [ ] 48. Color Cycle Bars - Animated bars
- [ ] 49. Aurora Fire - Combined effects
- [ ] 50. Meteor Plasma - Space + plasma
- [ ] 51. Snow Matrix - Winter + digital
- [ ] 52. Julia Fire - Fractal + fire
- [ ] 53. Mandelbrot Lightning - Fractal + electric
- [ ] 54. Dragon DNA - Curve + helix
- [ ] 55. Voronoi Starfield - Cellular + space
- [ ] 56. Firework Tunnel - Explosion + 3D
- [ ] 57. Smoke Lava - Particles + heat
- [ ] 58. Tetris Rain - Game + particles
- [ ] 59. Julia Standalone - Julia set fractal
- [ ] 60. Retro Geometry - 80s geometric patterns

## Hardware Requirements

### Adafruit PyPortal
- **Display:** 320x240 TFT touchscreen
- **MCU:** ATSAMD51J20 (Cortex M4 @ 120MHz)
- **Memory:** 512KB RAM, 4MB Flash
- **CircuitPython:** Version 8.0+ required

### Optional Features
- **Touch Control:** Cycle through effects
- **Audio:** Sound effects for some animations
- **Network:** Future web control interface

## Installation

1. **Install CircuitPython** on your PyPortal
2. **Copy libraries** to `lib/` folder:
   - `adafruit_pyportal`
   - `displayio` (built-in)
   - Additional libs as needed per effect
3. **Copy screensaver files** to PyPortal
4. **Run main screensaver** from REPL or auto-run

## Usage

- **Touch Screen:** Tap to cycle through effects
- **Auto Mode:** Effects change automatically every 30 seconds
- **Manual Control:** Use REPL commands to select specific effects

## Development Notes

**Porting Strategy:**
1. Start with mathematical effects (plasma, fractals)
2. Convert C++ math to Python/CircuitPython
3. Use `displayio` bitmap and palette system
4. Optimize for PyPortal's 120MHz ARM processor
5. Target 10-20 FPS for smooth animation

**Performance Considerations:**
- Use integer math where possible
- Pre-calculate lookup tables
- Minimize memory allocation in animation loops
- Use `displayio.Bitmap` for efficient pixel manipulation

## Project Structure

```
/
├── README.md                    # This file
├── examples/
│   ├── pyportal_screensaver.py  # Main screensaver framework
│   ├── plasma_field.py          # Effect #1
│   ├── kaleidoscope.py          # Effect #2
│   └── mandelbrot.py            # Effect #3
├── lib/
│   └── screensaver_effects/     # Effect modules
└── assets/
    └── palettes/               # Color palette data
```

## Contributing

Effects are being ported in numerical order. Each effect should:
- Be self-contained in its own module
- Use consistent API for initialization and animation
- Include performance optimization for CircuitPython
- Document mathematical algorithms used

## License

Based on the ESP32 Psychedelic Clock project. Individual effects may have different mathematical sources - see code comments for attribution.

---

**Progress Tracker:** 0/60 effects completed  
**Next Milestone:** Complete first 3 effects (Plasma, Kaleidoscope, Mandelbrot)  
**Target Date:** TBD - developing framework first

*Let's make the PyPortal psychedelic! 🌈*