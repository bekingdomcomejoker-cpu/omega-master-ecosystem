#!/data/data/com.termux/files/usr/bin/bash

LOG_DIR="/sdcard/omega_bridge"
mkdir -p "$LOG_DIR"

adb shell uiautomator dump > /dev/null
adb pull /sdcard/window_dump.xml $LOG_DIR/window_dump.xml > /dev/null

grep "text=" $LOG_DIR/window_dump.xml > $LOG_DIR/last_screen.txt
