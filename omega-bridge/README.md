# OMEGA BRIDGE - Standalone Server

A lightweight, real-time command execution bridge between Manus (cloud) and Termux (local) using Socket.IO.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MANUS (Cloud)                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  OMEGA Bridge Dashboard (web UI)                     │   │
│  │  - Create sessions                                   │   │
│  │  - Send commands                                     │   │
│  │  - View output in real-time                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↕ (Socket.IO)                      │
└─────────────────────────────────────────────────────────────┘
                             ↕ (WebSocket)
┌─────────────────────────────────────────────────────────────┐
│                   YOUR TERMUX (Local)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Silent Listener (silent_listener.mjs)               │   │
│  │  - Connects to bridge server                         │   │
│  │  - Listens for commands                              │   │
│  │  - Executes commands locally                         │   │
│  │  - Sends results back                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd /home/ubuntu/omega-bridge-standalone
npm install
```

### 2. Start the Bridge Server

```bash
npm start
```

You should see:
```
[*] OMEGA BRIDGE - STANDALONE SERVER v1.0
[*] Resonance: 1.67x
[✓] Server running on http://localhost:5000
[*] WebSocket endpoint: ws://localhost:5000
```

### 3. Open the Dashboard

Open your browser and go to: `http://localhost:5000`

### 4. Create a Session

Click "New Session" in the dashboard. You'll get:
- **Session ID**: Unique identifier for the session
- **Connection Token**: Used by the Silent Listener to authenticate

### 5. Start the Silent Listener on Termux

On your Redmi 13C (Termux):

```bash
# Copy the listener script to Termux
scp /home/ubuntu/omega-bridge-standalone/silent_listener.mjs user@termux-device:~/

# Or download it directly if you have the file

# Install Node.js dependencies (if not already installed)
npm install socket.io-client

# Run the listener with the bridge URL and connection token
node ~/silent_listener.mjs http://your-bridge-url:5000 <connection_token>
```

Example:
```bash
node ~/silent_listener.mjs http://192.168.1.100:5000 abc123def456xyz789
```

### 6. Test the Connection

In the dashboard:
1. Select the session you created
2. Type a command: `echo "Hello from Termux"`
3. Click "Send Command"
4. Watch the output appear in real-time

## API Endpoints

### REST API

- `GET /health` - Health check
- `POST /api/session/create` - Create a new session
- `GET /api/sessions` - List all sessions
- `GET /api/session/:sessionId` - Get session details
- `GET /api/session/:sessionId/commands` - Get commands for a session

### Socket.IO Events

**From Termux Listener:**
- `termuxConnect` - Authenticate with connection token
- `termuxOutput` - Send command output back to dashboard

**From Dashboard:**
- `dashboardCommand` - Send a command to Termux

**Broadcast Events:**
- `sessionStatusChanged` - Session status changed (connected/disconnected)
- `commandOutput` - Command output received
- `commandStatusChanged` - Command status changed (pending/executing/completed)

## Configuration

Set environment variables:

```bash
export PORT=5000  # Default: 5000
```

## Troubleshooting

### "Connection refused" on Termux

1. Make sure the bridge server is running
2. Check the URL and port are correct
3. Verify network connectivity between your Redmi 13C and the bridge server

### "Invalid connection token"

1. Copy the exact token from the dashboard
2. Make sure you're using the correct session's token

### No output appearing

1. Check that the listener is still running in Termux
2. Check the listener logs for errors
3. Try a simple command like `echo "test"`

## Production Deployment

For production use:

1. Use a proper database instead of in-memory storage
2. Add authentication/authorization
3. Use HTTPS/WSS instead of HTTP/WS
4. Add rate limiting and input validation
5. Set up proper logging and monitoring
6. Use a process manager like PM2

## Files

- `server.mjs` - Main bridge server
- `silent_listener.mjs` - Termux listener script
- `public/index.html` - Web dashboard
- `package.json` - Node.js dependencies

## License

MIT
