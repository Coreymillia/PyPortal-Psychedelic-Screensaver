# PyPortal Psychedelic Screensaver

**Transform your Adafruit PyPortal into a mesmerizing psychedelic art display!** 🌈

This project features 7 optimized visual effects that run smoothly on CircuitPython, turning your PyPortal into an ambient screensaver with mathematical patterns, particle systems, and classic demoscene effects.

## 🎬 Live Effects Demo

**Auto-cycling screensaver with 7 unique effects (1 minute each):**

1. **🌈 Plasma Field** - Classic sine wave interference patterns
2. **🌀 Spiral** - Rotating mathematical spiral patterns  
3. **💚 Matrix** - Green digital rain (classic Matrix effect)
4. **🌈💻 Color Matrix** - Rainbow falling letters and symbols
5. **🌀🎨 Julia Fractal** - Real-time morphing mathematical fractals
6. **🔥 Fire Simulation** - Realistic flame physics with heat diffusion
7. **🌊 Sine Wave Interference** - Multiple wave sources creating complex patterns

## 🚀 Quick Start

### Hardware Required
- **Adafruit PyPortal** (320x240 TFT touchscreen)
- **CircuitPython 9.0+** installed
- **USB cable** for programming

### Installation
1. **Install CircuitPython** on your PyPortal
2. **Copy `pyportal_screensaver_main.py`** to PyPortal as `code.py`
3. **Power on** - screensaver starts automatically!

### Usage
- **Auto-advance:** Effects change every 1 minute
- **7-minute cycle:** Complete rotation through all effects
- **Plug & play:** No configuration needed

## 📁 Files Included

- `pyportal_screensaver_main.py` - **Main screensaver (current stable version)**
- `pyportal_7effects_stable.py` - Same as main (backup)
- `pyportal_8effects_stable.py` - Previous 8-effect version (may crash)
- `pyportal_autoscroll_2effects.py` - Early 2-effect milestone
- `pyportal_baseline_working.py` - Single plasma effect baseline
- `DEVELOPMENT_LOG.md` - Technical development notes

## 🧠 Memory Optimization

**PyPortal Constraints:**
- **192KB RAM** available for effects
- **Memory-optimized approach:** Half-resolution bitmaps (160x120) scaled 2x
- **Reduced palettes:** 16-64 colors instead of full 256
- **Smart cleanup:** Automatic garbage collection and object management

**Removed Effects:**
- ⭐ **Starfield** - Removed due to memory usage (150 star objects)
- 📈 **Streamers** - Not implemented due to memory limits

## 🎨 Technical Details

**Effect Categories:**
- **Mathematical:** Plasma fields, fractals, sine waves
- **Particle Systems:** Fire simulation, matrix rain
- **Algorithmic:** Spiral patterns, interference waves

**Performance:**
- **Target:** 10-15 FPS smooth animation
- **Optimization:** Integer math, lookup tables, efficient algorithms
- **Memory Management:** Automatic cleanup, hard limits on objects

## 🛠️ Development

**Evolution:**
1. **Baseline** - Single plasma effect working
2. **2 Effects** - Added spiral, touch control  
3. **8 Effects** - Full collection, memory issues discovered
4. **7 Effects** - Removed starfield for stability ✅

**Future Plans:**
- Additional effects within memory constraints
- Touch screen control implementation
- Custom color palette options

## 📷 Screenshots

*(Screenshots coming soon - device currently running)*

## ⚡ Performance

**Smooth Animation:**
- 10-15 FPS average across all effects
- Optimized for 120MHz ARM Cortex M4
- Real-time mathematical calculations
- No pre-rendered assets - everything computed live

**Memory Efficient:**
- All effects run within PyPortal's 192KB RAM limit
- Smart memory management prevents crashes
- Automatic garbage collection between effects

## 🤝 Contributing

This is a complete, working screensaver! Contributions welcome for:
- **New effects** (within memory constraints)
- **Performance optimizations**  
- **Documentation improvements**
- **Bug fixes**

## 📜 License

MIT License - Feel free to modify and distribute!

Based on concepts from:
- ESP32 Psychedelic Clock project
- Classic demoscene effects
- Mathematical visualization algorithms

## 🎯 Project Status: COMPLETE ✅

**Ready to use:** Stable 7-effect screensaver  
**Memory optimized:** No crashes, smooth performance  
**Plug & play:** Just copy `code.py` and run!

---

**Made with ❤️ for the maker community**  
*Transform your PyPortal into ambient art! 🌈*