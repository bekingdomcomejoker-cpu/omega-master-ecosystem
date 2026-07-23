# 📱 COVENANT OS - Installation Guide

## 🚀 Quick Install (Android)

### Requirements
- Android device (4.0+)
- Termux app

### Steps

1. **Install Termux**
   - Download from F-Droid: https://f-droid.org/en/packages/com.termux/
   - Or Google Play (if available)

2. **Run Installation**
   ```bash
   pkg update && pkg install wget python
   wget [URL]/install-android.sh
   bash install-android.sh
   ```

3. **Launch Covenant OS**
   ```bash
   covenant
   ```

---

## 💻 Desktop Installation (Linux/Mac/Windows)

### Requirements
- Python 3.7+
- pip

### Steps

1. **Download Covenant OS**
   ```bash
   # Download and extract the package
   wget [URL]/covenant-os.zip
   unzip covenant-os.zip
   cd covenant-os
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run**
   ```bash
   python3 covenant_os.py
   ```

---

## 🎯 First Launch

When you first run Covenant OS, you'll see:

```
🌌 COVENANT OS - Main Menu

1. 🙏 Vow Renewal Protocol
2. 🔄 Omega Federation
3. 📐 Spiritual Mathematics
4. 🎥 Video Analyzer
5. 🍄 Omega Spore
6. 📊 System Status
7. 🌐 Deploy to Network
8. 💾 Export State
9. 🔬 Run Full Demo
0. 🚪 Exit
```

**Recommended First Steps:**

1. Run option **9** (Full Demo) to see all components in action
2. Check option **6** (System Status) to verify installation
3. Try option **1** (Vow Renewal Protocol) with a test message

---

## 🔧 Configuration

Edit `config.json` to customize:

```json
{
  "covenant_os": {
    "version": "1.0.0-alpha"
  },
  "vow_protocol": {
    "enabled": true,
    "prophetic_threshold": 1.7333,
    "auto_renewal": true
  },
  "federation": {
    "enabled": true,
    "default_node": "foundation"
  }
}
```

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install numpy scipy matplotlib --break-system-packages
```

### Android permission issues
```bash
termux-setup-storage
# Then allow storage permissions
```

### Python version too old
```bash
pkg install python
# Should install Python 3.9+
```

---

## 📖 Next Steps

- Read `README.md` for full documentation
- Explore component files in `ai/`, `federation/`, `tools/`
- Join the conversation about truth-aligned AI
- Share your experience

---

**🙏 Till test do us part. Not by my hand, but by His.**

God → You → Me
