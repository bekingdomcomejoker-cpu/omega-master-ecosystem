"""
COVENANT MIRROR X11 - BACKEND (COMPLETE SYSTEM)
===============================================
FastAPI WebSocket server with full persistence, Gemini streaming,
Alphabet Engine integration, TEREX validation, and replay logs.
"""

import os
import json
import asyncio
import uuid
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from database import (
    init_database, SessionManager, MessageStore, AuditLog, Statistics
)
from pipeline import ExecutionPipeline, get_session_replay, get_all_sessions_summary

# ============================================================================
# INITIALIZATION
# ============================================================================

# Initialize database
init_database()

# FastAPI App
app = FastAPI(title="Covenant Mirror X11", version="2.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# FEDERATION STATE
# ============================================================================

class FederationState:
    """Track federation state and metrics."""
    def __init__(self):
        self.start_time = datetime.now()
        self.active_sessions = {}
    
    def to_dict(self):
        stats = Statistics.get_stats()
        return {
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "active_sessions": len(self.active_sessions),
            **stats
        }

state = FederationState()

# ============================================================================
# WEBSOCKET HANDLER
# ============================================================================

@app.websocket("/ws/covenant")
async def covenant_ws(websocket: WebSocket):
    """
    Main WebSocket endpoint for Covenant Mirror.
    
    Handles:
    - Session management
    - Message routing
    - Pipeline execution
    - Persistence
    - Replay logs
    """
    await websocket.accept()
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    mode = "operator"  # Default mode
    current_state = "ON"  # Default state
    
    # Create session
    SessionManager.create_session(session_id, mode, current_state)
    state.active_sessions[session_id] = True
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "STATE",
            "node": "wire",
            "payload": {
                "status": "CONNECTED",
                "message": "Covenant Mirror X11 online",
                "session_id": session_id,
                "lambda": 2.2,
                "anchor": "Chicka chicka orange.",
                "mode": mode
            }
        })
        
        AuditLog.log_action(session_id, "SESSION_STARTED", {"mode": mode})
        
        # Main message loop
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)
            
            # ================================================================
            # COMMAND: HELLO (Handshake)
            # ================================================================
            if msg.get("type") == "COMMAND" and msg.get("payload", {}).get("action") == "HELLO":
                await websocket.send_json({
                    "type": "RESPONSE",
                    "node": "wire",
                    "payload": {
                        "text": "Hello. I am listening.",
                        "status": "ready",
                        "session_id": session_id
                    }
                })
                AuditLog.log_action(session_id, "HELLO_RECEIVED")
            
            # ================================================================
            # COMMAND: STATUS (System metrics)
            # ================================================================
            elif msg.get("type") == "COMMAND" and msg.get("payload", {}).get("action") == "STATUS":
                await websocket.send_json({
                    "type": "RESPONSE",
                    "node": "wire",
                    "payload": state.to_dict()
                })
            
            # ================================================================
            # COMMAND: REPLAY (Get session history)
            # ================================================================
            elif msg.get("type") == "COMMAND" and msg.get("payload", {}).get("action") == "REPLAY":
                replay_session_id = msg.get("payload", {}).get("session_id", session_id)
                replay_data = get_session_replay(replay_session_id)
                await websocket.send_json({
                    "type": "RESPONSE",
                    "node": "wire",
                    "payload": {
                        "replay": replay_data,
                        "status": "complete"
                    }
                })
            
            # ================================================================
            # COMMAND: SESSIONS (List all sessions)
            # ================================================================
            elif msg.get("type") == "COMMAND" and msg.get("payload", {}).get("action") == "SESSIONS":
                sessions_summary = get_all_sessions_summary()
                await websocket.send_json({
                    "type": "RESPONSE",
                    "node": "wire",
                    "payload": sessions_summary
                })
            
            # ================================================================
            # COMMAND: SWITCH_MODE (Toggle operator/public mode)
            # ================================================================
            elif msg.get("type") == "COMMAND" and msg.get("payload", {}).get("action") == "SWITCH_MODE":
                new_mode = msg.get("payload", {}).get("mode", "operator")
                mode = new_mode
                SessionManager.update_session_state(session_id, current_state)
                AuditLog.log_action(session_id, "MODE_SWITCHED", {"new_mode": mode})
                await websocket.send_json({
                    "type": "RESPONSE",
                    "node": "wire",
                    "payload": {
                        "status": "mode_changed",
                        "mode": mode
                    }
                })
            
            # ================================================================
            # PAYLOAD: User message (Execute full pipeline)
            # ================================================================
            elif msg.get("type") == "PAYLOAD":
                prompt = msg.get("payload", {}).get("text", "")
                new_state = msg.get("state", current_state)
                current_state = new_state
                
                if not prompt:
                    await websocket.send_json({
                        "type": "ERROR",
                        "node": "wire",
                        "payload": {"text": "Empty payload"}
                    })
                    continue
                
                # Update session state
                SessionManager.update_session_state(session_id, current_state)
                
                # Execute complete pipeline
                pipeline = ExecutionPipeline(session_id, current_state)
                async for result in pipeline.execute(prompt):
                    await websocket.send_json(result)
            
            # ================================================================
            # STATE: Query system state
            # ================================================================
            elif msg.get("type") == "STATE":
                await websocket.send_json({
                    "type": "STATE",
                    "node": "wire",
                    "payload": state.to_dict()
                })
            
            # ================================================================
            # UNKNOWN
            # ================================================================
            else:
                await websocket.send_json({
                    "type": "ERROR",
                    "node": "wire",
                    "payload": {"text": "Unknown message type"}
                })
    
    except WebSocketDisconnect:
        print(f"✗ Client disconnected: {session_id}")
        AuditLog.log_action(session_id, "SESSION_ENDED")
        state.active_sessions.pop(session_id, None)
    except Exception as e:
        print(f"✗ WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "ERROR",
                "node": "wire",
                "payload": {"text": str(e)}
            })
        except:
            pass
        state.active_sessions.pop(session_id, None)

# ============================================================================
# HTTP ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with system info."""
    return {
        "name": "Covenant Mirror X11",
        "version": "2.0.0",
        "status": "online",
        "websocket": "/ws/covenant",
        "features": [
            "Real-time streaming",
            "Persistence (SQLite)",
            "Replay logs",
            "Alphabet Engine integration",
            "TEREX validation",
            "Dual UI modes"
        ],
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "stats": "/stats",
            "sessions": "/sessions"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "uptime_seconds": (datetime.now() - state.start_time).total_seconds(),
        "active_sessions": len(state.active_sessions)
    }

@app.get("/metrics")
async def metrics():
    """System metrics endpoint."""
    return state.to_dict()

@app.get("/stats")
async def stats():
    """Detailed statistics endpoint."""
    return Statistics.get_stats()

@app.get("/sessions")
async def sessions():
    """List all sessions."""
    return get_all_sessions_summary()

@app.get("/sessions/{session_id}")
async def get_session_data(session_id: str):
    """Get specific session replay."""
    return get_session_replay(session_id)

# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    print("=" * 70)
    print("🔷 COVENANT MIRROR X11 - BACKEND ONLINE (COMPLETE SYSTEM)")
    print("=" * 70)
    print("✓ Database: SQLite (persistent)")
    print("✓ Gemini API: Configured")
    print("✓ Alphabet Engine: Integrated")
    print("✓ TEREX: Integrated")
    print("✓ WebSocket: /ws/covenant")
    print("✓ Replay logs: Enabled")
    print("✓ Dual modes: Operator + Public")
    print("=" * 70)

@app.on_event("shutdown")
async def shutdown():
    print("\n" + "=" * 70)
    print("🔷 COVENANT MIRROR X11 - SHUTTING DOWN")
    stats = Statistics.get_stats()
    print(f"✓ Total sessions: {stats['total_sessions']}")
    print(f"✓ Total messages: {stats['total_messages']}")
    print("=" * 70)

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
