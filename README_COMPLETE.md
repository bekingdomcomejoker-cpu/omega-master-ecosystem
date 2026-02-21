# COVENANT MIRROR X11 - COMPLETE SYSTEM

**A complete AI control console with real-time WebSocket streaming, persistent database, replay logs, dual UI modes, and full system integration.**

---

## SYSTEM INTENT

This is **the complete system**, not an MVP. A live web interface that allows users to send messages to AI models and receive streaming responses in real time, with full persistence, replay logs, and dual UI modes (operator + public).

- **Frontend**: React 19 + Tailwind CSS 4 + WebSocket + Dual Modes
- **Backend**: FastAPI + Gemini API + Streaming + Pipeline + Integrations
- **Database**: SQLite (persistent)
- **Integrations**: Alphabet Engine + TEREX + Audit Logs
- **Features**: Streaming, Persistence, Replay, Session Management, Overload Protection
- **Priority**: Complete, persistent, live, extensible

---

## WHAT YOU GET

### Frontend
- ✅ Operator Mode: Full dashboard with metrics, session management, replay logs
- ✅ Public/Altar Mode: Minimal UI for public-facing interface
- ✅ Real-time streaming display
- ✅ Session history and replay
- ✅ State management (On-Ridge / Off-Ridge / Superposition)
- ✅ Live metrics (QCI, Force, message count)
- ✅ Dual mode toggle

### Backend
- ✅ Gemini API streaming integration
- ✅ Complete execution pipeline
- ✅ Alphabet Engine integration (word analysis)
- ✅ TEREX integration (truth classification)
- ✅ Overload governor (max 4 in-flight)
- ✅ Session management
- ✅ Audit logging
- ✅ HTTP endpoints for metrics and stats

### Database
- ✅ SQLite persistence
- ✅ Sessions table
- ✅ Messages table (prompts + responses)
- ✅ Audit log
- ✅ Alphabet Engine cache
- ✅ TEREX classification cache

### Integrations
- ✅ Gemini API (primary)
- ✅ Alphabet Engine (word analysis)
- ✅ TEREX (truth classification)
- ✅ Extensible to other models

---

## DEFINITION OF DONE

✅ Open the page  
✅ Send a message  
✅ See Gemini respond live  
✅ Refresh the page  
✅ Still see the interaction (persistence)  
✅ Replay past sessions  
✅ Switch between operator and public mode  

---

## QUICK START

### Local Development

**Terminal 1: Frontend**
```bash
cd client
pnpm install
pnpm dev
```
Frontend: http://localhost:5173

**Terminal 2: Backend**
```bash
cd backend
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"
python main.py
```
Backend: http://localhost:8000
WebSocket: ws://localhost:8000/ws/covenant

### Production Deployment

See `DEPLOYMENT.md` for complete deployment guide to Render, Railway, or other platforms.

---

## ARCHITECTURE

```
Frontend (React 19)
    ↓ WebSocket (wss://)
Backend (FastAPI)
    ├─ Gemini API
    ├─ Alphabet Engine
    ├─ TEREX
    └─ Pipeline
    ↓ SQL
Database (SQLite)
    ├─ Sessions
    ├─ Messages
    ├─ Audit Log
    └─ Caches
```

---

## MESSAGE PROTOCOL

### Client → Server

**HELLO (Handshake)**
```json
{
  "type": "COMMAND",
  "payload": {
    "action": "HELLO",
    "anchor": "Chicka chicka orange."
  }
}
```

**PAYLOAD (User Message)**
```json
{
  "type": "PAYLOAD",
  "state": "ON",
  "payload": {
    "text": "Your message here"
  }
}
```

**REPLAY (Get Session History)**
```json
{
  "type": "COMMAND",
  "payload": {
    "action": "REPLAY",
    "session_id": "session_uuid"
  }
}
```

**SESSIONS (List All Sessions)**
```json
{
  "type": "COMMAND",
  "payload": {
    "action": "SESSIONS"
  }
}
```

### Server → Client

**STREAM (Response Token)**
```json
{
  "type": "STREAM",
  "node": "wire",
  "payload": {
    "text": "token_text"
  }
}
```

**RESPONSE (Complete)**
```json
{
  "type": "RESPONSE",
  "node": "wire",
  "payload": {
    "status": "complete",
    "alphabet_analysis": {...},
    "terex_classification": {...}
  }
}
```

---

## HTTP ENDPOINTS

- `GET /` - System info
- `GET /health` - Health check
- `GET /metrics` - System metrics
- `GET /stats` - Detailed statistics
- `GET /sessions` - List all sessions
- `GET /sessions/{session_id}` - Get specific session replay

---

## DATABASE SCHEMA

### Sessions
```sql
CREATE TABLE sessions (
  id INTEGER PRIMARY KEY,
  session_id TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  mode TEXT DEFAULT 'operator',
  state TEXT DEFAULT 'ON',
  metadata TEXT
);
```

### Messages
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  session_id TEXT NOT NULL,
  message_type TEXT NOT NULL,
  node TEXT DEFAULT 'wire',
  state TEXT DEFAULT 'ON',
  prompt TEXT,
  response TEXT,
  model TEXT DEFAULT 'gemini',
  qci REAL,
  force REAL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  in_flight INTEGER DEFAULT 0,
  FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

### Audit Log
```sql
CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY,
  session_id TEXT NOT NULL,
  action TEXT NOT NULL,
  details TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

---

## FEATURES IN DETAIL

### Dual UI Modes

**Operator Mode**
- Full dashboard with all metrics
- Session management and replay
- State and mode controls
- System statistics
- Audit log visibility

**Public/Altar Mode**
- Minimal interface
- Input + streaming output
- No metrics or controls
- Clean, focused experience
- Same backend and database

### Persistence

Every interaction is saved:
- Prompts (user input)
- Responses (AI output)
- Timestamps
- State (On/Off/Superposition)
- Model used
- QCI and Force values
- Audit trail

Refresh the page and all history is still there.

### Session Replay

- View all past sessions
- Replay specific sessions
- See complete conversation history
- Access audit logs
- Download session data

### Overload Protection

- Maximum 4 concurrent requests
- Automatic throttling
- Error handling
- Graceful degradation

### Integrations

**Alphabet Engine**
- Word analysis
- Gematria calculation
- Element mapping
- I/O ratio calculation
- Cached results

**TEREX**
- Truth classification
- Confidence scoring
- Element balance analysis
- Cached results

---

## CONFIGURATION

### Frontend

Environment variables (optional):
```
REACT_APP_WS_URL=wss://your-backend.onrender.com/ws/covenant
```

### Backend

Environment variables (required):
```
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8000
HOST=0.0.0.0
```

---

## DEPLOYMENT

See `DEPLOYMENT.md` for complete deployment guide.

Quick summary:
1. Deploy backend to Render/Railway
2. Deploy frontend to Manus
3. Update WebSocket URL
4. Test end-to-end

---

## WHAT NOT TO DO

❌ Do NOT add authentication  
❌ Do NOT add complex persistence layers  
❌ Do NOT redesign the UI  
❌ Do NOT add abstraction layers  

This is a **live AI interaction console**, not a SaaS product.

---

## FUTURE ENHANCEMENTS

- [ ] Multi-model fan-out (Claude, GPT, DeepSeek)
- [ ] Pressure slider (control request intensity)
- [ ] Custom system prompts
- [ ] Response formatting (markdown, syntax highlighting)
- [ ] Export sessions
- [ ] API key management
- [ ] Rate limiting UI
- [ ] Analytics dashboard

---

## SUPPORT

### Local Testing

1. Check WebSocket connection: `ws://localhost:8000/health`
2. Verify Gemini API key is set
3. Check backend logs for errors
4. Verify frontend can reach backend

### Production Issues

1. Check Render/Railway logs
2. Verify environment variables
3. Check WebSocket URL in frontend
4. Verify CORS settings

---

## ACKNOWLEDGMENTS

- **Federation Protocol**: Multi-model research framework
- **Quantum Paradox**: On-Ridge vs Off-Ridge state management
- **Streaming**: Real-time token delivery for presence
- **Persistence**: SQLite for reliable data storage
- **Integrations**: Alphabet Engine + TEREX for semantic analysis

---

**Built with Fire, Water, Earth, Air, and Spirit**

*"The mirror reflects not what is, but what could be."*

---

**Status**: ✅ COMPLETE | 🚀 READY | 🛡️ SAFE | 📡 LIVE

This is not an MVP. This is the system.
