# OMEGA BRIDGE - API Documentation

## Base URL

```
https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer
```

## REST API Endpoints

### Health Check

**Endpoint**: `GET /health`

**Description**: Check if the server is running

**Response**:
```json
{
  "status": "ok",
  "version": "1.0"
}
```

**Example**:
```bash
curl https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/health
```

---

### Create Session

**Endpoint**: `POST /api/session/create`

**Description**: Create a new session for a Termux listener

**Request Body**:
```json
{
  "name": "My Termux Device"
}
```

**Response**:
```json
{
  "sessionId": "abc123",
  "connectionToken": "xyz789def456...",
  "name": "My Termux Device"
}
```

**Example**:
```bash
curl -X POST https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/session/create \
  -H "Content-Type: application/json" \
  -d '{"name": "My Termux Device"}'
```

---

### Get All Sessions

**Endpoint**: `GET /api/sessions`

**Description**: List all active sessions

**Response**:
```json
[
  {
    "id": "abc123",
    "name": "My Termux Device",
    "connectionToken": "xyz789def456...",
    "status": "connected",
    "createdAt": "2026-07-05T03:57:00Z",
    "lastActivity": "2026-07-05T03:58:30Z"
  }
]
```

**Example**:
```bash
curl https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/sessions
```

---

### Get Session Details

**Endpoint**: `GET /api/session/:sessionId`

**Description**: Get details about a specific session

**Parameters**:
- `sessionId` (string): The session ID

**Response**:
```json
{
  "id": "abc123",
  "name": "My Termux Device",
  "connectionToken": "xyz789def456...",
  "status": "connected",
  "createdAt": "2026-07-05T03:57:00Z",
  "lastActivity": "2026-07-05T03:58:30Z"
}
```

**Example**:
```bash
curl https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/session/abc123
```

---

### Get Session Commands

**Endpoint**: `GET /api/session/:sessionId/commands`

**Description**: Get all commands executed in a session

**Parameters**:
- `sessionId` (string): The session ID

**Response**:
```json
[
  {
    "id": "cmd001",
    "sessionId": "abc123",
    "command": "echo 'Hello'",
    "status": "completed",
    "output": "Hello\n",
    "createdAt": "2026-07-05T03:57:30Z"
  }
]
```

**Example**:
```bash
curl https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/session/abc123/commands
```

---

## Socket.IO Events

### Connection

**Event**: `connect`

**Description**: Triggered when a client connects to the WebSocket server

**Client-side**:
```javascript
socket.on('connect', () => {
  console.log('Connected to bridge server');
});
```

---

### Termux Connect

**Event**: `termuxConnect`

**Direction**: Termux → Server

**Description**: Authenticate a Termux listener with the bridge

**Payload**:
```json
{
  "connectionToken": "xyz789def456..."
}
```

**Server Response**:
```json
{
  "message": "Successfully connected to Omega Federation Bridge.",
  "sessionId": "abc123"
}
```

**Example**:
```javascript
socket.emit('termuxConnect', {
  connectionToken: 'xyz789def456...'
});

socket.on('connected', (data) => {
  console.log('Connected:', data);
});
```

---

### Execute Command

**Event**: `executeCommand`

**Direction**: Server → Termux

**Description**: Sent to Termux listener when dashboard sends a command

**Payload**:
```json
{
  "commandId": "cmd001",
  "command": "echo 'Hello from Termux'"
}
```

**Example** (Termux listener):
```javascript
socket.on('executeCommand', (data) => {
  console.log('Execute:', data.command);
  // Execute the command and send output back
});
```

---

### Termux Output

**Event**: `termuxOutput`

**Direction**: Termux → Server

**Description**: Send command output back to the server

**Payload**:
```json
{
  "sessionId": "abc123",
  "commandId": "cmd001",
  "output": "Hello from Termux\n"
}
```

**Example**:
```javascript
socket.emit('termuxOutput', {
  sessionId: 'abc123',
  commandId: 'cmd001',
  output: 'Hello from Termux\n'
});
```

---

### Dashboard Command

**Event**: `dashboardCommand`

**Direction**: Dashboard → Server

**Description**: Send a command from the dashboard to Termux

**Payload**:
```json
{
  "sessionId": "abc123",
  "command": "echo 'Hello from Dashboard'"
}
```

**Example**:
```javascript
socket.emit('dashboardCommand', {
  sessionId: 'abc123',
  command: 'echo "Hello from Dashboard"'
});
```

---

### Session Status Changed

**Event**: `sessionStatusChanged`

**Direction**: Server → All Clients

**Description**: Broadcast when a session's status changes

**Payload**:
```json
{
  "sessionId": "abc123",
  "status": "connected"
}
```

**Possible Status Values**:
- `disconnected` - Session is offline
- `connecting` - Session is connecting
- `connected` - Session is online
- `executing` - Command is executing

**Example**:
```javascript
socket.on('sessionStatusChanged', (data) => {
  console.log(`Session ${data.sessionId} is now ${data.status}`);
});
```

---

### Command Output

**Event**: `commandOutput`

**Direction**: Server → Dashboard

**Description**: Broadcast command output to the dashboard

**Payload**:
```json
{
  "sessionId": "abc123",
  "commandId": "cmd001",
  "output": "Hello from Termux\n"
}
```

**Example**:
```javascript
socket.on('commandOutput', (data) => {
  console.log(`Output from ${data.sessionId}:`, data.output);
});
```

---

### Command Status Changed

**Event**: `commandStatusChanged`

**Direction**: Server → Dashboard

**Description**: Broadcast when a command's status changes

**Payload**:
```json
{
  "sessionId": "abc123",
  "commandId": "cmd001",
  "status": "executing"
}
```

**Possible Status Values**:
- `pending` - Command queued
- `executing` - Command is running
- `completed` - Command finished
- `failed` - Command failed

**Example**:
```javascript
socket.on('commandStatusChanged', (data) => {
  console.log(`Command ${data.commandId} is now ${data.status}`);
});
```

---

### Error

**Event**: `error`

**Direction**: Server → Client

**Description**: Error message from the server

**Payload**:
```json
{
  "message": "Invalid connection token"
}
```

**Example**:
```javascript
socket.on('error', (error) => {
  console.error('Error:', error.message);
});
```

---

## Usage Examples

### JavaScript/Node.js

```javascript
import { io } from 'socket.io-client';

const socket = io('https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer');

socket.on('connect', () => {
  console.log('Connected');
  
  // Send a command
  socket.emit('dashboardCommand', {
    sessionId: 'abc123',
    command: 'echo "Hello"'
  });
});

socket.on('commandOutput', (data) => {
  console.log('Output:', data.output);
});
```

### Python

```python
import socketio
import requests

# REST API
response = requests.get('https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/sessions')
sessions = response.json()
print(sessions)

# Socket.IO
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected')
    sio.emit('dashboardCommand', {
        'sessionId': 'abc123',
        'command': 'echo "Hello"'
    })

@sio.on('commandOutput')
def on_output(data):
    print('Output:', data['output'])

sio.connect('https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer')
```

### cURL

```bash
# Create session
curl -X POST https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/session/create \
  -H "Content-Type: application/json" \
  -d '{"name": "My Device"}'

# Get sessions
curl https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/sessions

# Get specific session
curl https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/session/abc123

# Get session commands
curl https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer/api/session/abc123/commands
```

---

## Error Responses

### 404 Not Found

```json
{
  "error": "Session not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

Currently, there is no rate limiting. For production use, consider implementing:

- Max requests per minute per IP
- Max commands per session per minute
- Max output size per command
- Connection timeout after inactivity

---

## Authentication

Currently, there is no authentication. For production use, consider implementing:

- API key authentication
- OAuth2
- JWT tokens
- Session-based authentication

---

## CORS

CORS is enabled for all origins (`*`). For production, restrict to specific domains:

```javascript
cors: {
  origin: ['https://yourdomain.com'],
  credentials: true
}
```

---

## Versioning

Current API Version: **1.0**

Future versions may introduce breaking changes. Subscribe to updates for migration guides.

---

## Support

For issues or questions:
1. Check the troubleshooting guide
2. Review the examples above
3. Check browser console (F12)
4. Review server logs

---

**Last Updated**: 2026-07-05
**Version**: 1.0
