# ADB + Termux Automation Layer

This directory contains the sovereign Android automation backbone for the Covenant Mirror X11 system.

## Components

- **omega_daemon.sh**: The core automation engine that processes the message queue and simulates user input via ADB.
- **omega_pull.sh**: A screen-scraping utility to extract visible text from the active Android app.
- **omega_supervisor.sh**: A crash-recovery wrapper that ensures the daemon remains active.

## Setup Instructions

1. **Enable Developer Mode** on your Android device.
2. **Install ADB** in Termux: `pkg install android-tools`.
3. **Connect ADB** to your device (USB or Wireless).
4. **Run the Supervisor** in a tmux session:
   ```bash
   pkg install tmux
   tmux
   ./omega_supervisor.sh
   ```
5. **Send Messages** by appending to the queue:
   ```bash
   echo "Your message here" >> /sdcard/omega_bridge/queue.txt
   ```

## Requirements

- Android device with ADB enabled.
- Termux installed.
- No API keys or paid apps required.
