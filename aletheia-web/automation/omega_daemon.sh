#!/data/data/com.termux/files/usr/bin/bash

LOG_DIR="/sdcard/omega_bridge"
QUEUE_FILE="$LOG_DIR/queue.txt"
LOCK_FILE="$LOG_DIR/lock"
LOG_FILE="$LOG_DIR/omega.log"

APP_PACKAGE="com.openai.chatgpt"   # Change to Gemini package if needed

mkdir -p "$LOG_DIR"

log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

launch_app() {
  adb shell monkey -p $APP_PACKAGE -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1
  sleep 3
}

send_message() {
  MESSAGE="$1"

  # Escape spaces for adb input
  SAFE_MESSAGE=$(echo "$MESSAGE" | sed 's/ /%s/g')

  adb shell input text "$SAFE_MESSAGE"
  adb shell input keyevent 66
}

process_queue() {
  if [ -f "$QUEUE_FILE" ]; then
    while IFS= read -r LINE
    do
      if [ ! -z "$LINE" ]; then
        log "Sending: $LINE"
        launch_app
        send_message "$LINE"
        sleep 5
      fi
    done < "$QUEUE_FILE"

    echo "" > "$QUEUE_FILE"
  fi
}

log "Omega Daemon Started"

while true
do
  if [ ! -f "$LOCK_FILE" ]; then
    process_queue
  fi

  sleep 4
done
