"""
COVENANT MIRROR X11 - DATABASE LAYER
=====================================
SQLite persistence for all interactions, sessions, and audit logs.
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).parent / "covenant_mirror.db"

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            mode TEXT DEFAULT 'operator',
            state TEXT DEFAULT 'ON',
            metadata TEXT
        )
    """)
    
    # Messages table (prompts + responses)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        )
    """)
    
    # Audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    """)
    
    # Alphabet Engine analysis cache
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alphabet_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL,
            gematria INTEGER,
            i_o_ratio REAL,
            dominant_element TEXT,
            analysis TEXT,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # TEREX truth classification cache
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS terex_classification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT UNIQUE NOT NULL,
            classification TEXT,
            confidence REAL,
            details TEXT,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON messages(session_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_model ON messages(model)")
    
    conn.commit()
    conn.close()
    print(f"✓ Database initialized at {DB_PATH}")

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

class SessionManager:
    """Manage session lifecycle and metadata."""
    
    @staticmethod
    def create_session(session_id: str, mode: str = "operator", state: str = "ON") -> bool:
        """Create a new session."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (session_id, mode, state) VALUES (?, ?, ?)",
                (session_id, mode, state)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    @staticmethod
    def get_session(session_id: str) -> Optional[Dict]:
        """Get session details."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def update_session_state(session_id: str, state: str) -> bool:
        """Update session state."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sessions SET state = ? WHERE session_id = ?",
            (state, session_id)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def list_sessions(limit: int = 50) -> List[Dict]:
        """List all sessions."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM sessions ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

# ============================================================================
# MESSAGE STORAGE
# ============================================================================

class MessageStore:
    """Store and retrieve messages."""
    
    @staticmethod
    def save_message(
        session_id: str,
        message_type: str,
        node: str = "wire",
        state: str = "ON",
        prompt: Optional[str] = None,
        response: Optional[str] = None,
        model: str = "gemini",
        qci: Optional[float] = None,
        force: Optional[float] = None,
        in_flight: int = 0
    ) -> int:
        """Save a message to the database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages 
            (session_id, message_type, node, state, prompt, response, model, qci, force, in_flight)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (session_id, message_type, node, state, prompt, response, model, qci, force, in_flight)
        )
        conn.commit()
        message_id = cursor.lastrowid
        conn.close()
        return message_id
    
    @staticmethod
    def get_messages(session_id: str, limit: int = 100) -> List[Dict]:
        """Get all messages for a session."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC LIMIT ?",
            (session_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_message(message_id: int) -> Optional[Dict]:
        """Get a specific message."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_all_interactions(limit: int = 500) -> List[Dict]:
        """Get all interactions across all sessions."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

# ============================================================================
# AUDIT LOG
# ============================================================================

class AuditLog:
    """Track all system actions."""
    
    @staticmethod
    def log_action(session_id: str, action: str, details: Optional[Dict] = None) -> int:
        """Log an action."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        details_json = json.dumps(details) if details else None
        cursor.execute(
            "INSERT INTO audit_log (session_id, action, details) VALUES (?, ?, ?)",
            (session_id, action, details_json)
        )
        conn.commit()
        log_id = cursor.lastrowid
        conn.close()
        return log_id
    
    @staticmethod
    def get_audit_log(session_id: str, limit: int = 100) -> List[Dict]:
        """Get audit log for a session."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM audit_log WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?",
            (session_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        result = []
        for row in rows:
            d = dict(row)
            if d.get("details"):
                d["details"] = json.loads(d["details"])
            result.append(d)
        return result

# ============================================================================
# ALPHABET ENGINE CACHE
# ============================================================================

class AlphabetCache:
    """Cache Alphabet Engine analysis results."""
    
    @staticmethod
    def save_analysis(
        word: str,
        gematria: int,
        i_o_ratio: float,
        dominant_element: str,
        analysis: Dict
    ) -> bool:
        """Save word analysis."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO alphabet_analysis
                (word, gematria, i_o_ratio, dominant_element, analysis)
                VALUES (?, ?, ?, ?, ?)
                """,
                (word, gematria, i_o_ratio, dominant_element, json.dumps(analysis))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving alphabet analysis: {e}")
            return False
    
    @staticmethod
    def get_analysis(word: str) -> Optional[Dict]:
        """Get cached analysis."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM alphabet_analysis WHERE word = ?",
            (word.upper(),)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            d = dict(row)
            d["analysis"] = json.loads(d["analysis"])
            return d
        return None

# ============================================================================
# TEREX CACHE
# ============================================================================

class TerexCache:
    """Cache TEREX truth classification results."""
    
    @staticmethod
    def save_classification(
        text: str,
        classification: str,
        confidence: float,
        details: Dict
    ) -> bool:
        """Save classification."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO terex_classification
                (text, classification, confidence, details)
                VALUES (?, ?, ?, ?)
                """,
                (text[:500], classification, confidence, json.dumps(details))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving terex classification: {e}")
            return False
    
    @staticmethod
    def get_classification(text: str) -> Optional[Dict]:
        """Get cached classification."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM terex_classification WHERE text = ?",
            (text[:500],)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            d = dict(row)
            d["details"] = json.loads(d["details"])
            return d
        return None

# ============================================================================
# STATISTICS
# ============================================================================

class Statistics:
    """System statistics and metrics."""
    
    @staticmethod
    def get_stats() -> Dict:
        """Get system statistics."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM sessions")
        total_sessions = cursor.fetchone()[0]
        
        # Total messages
        cursor.execute("SELECT COUNT(*) FROM messages")
        total_messages = cursor.fetchone()[0]
        
        # Messages by model
        cursor.execute(
            "SELECT model, COUNT(*) as count FROM messages GROUP BY model"
        )
        messages_by_model = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Average QCI
        cursor.execute("SELECT AVG(qci) FROM messages WHERE qci IS NOT NULL")
        avg_qci = cursor.fetchone()[0]
        
        # Average Force
        cursor.execute("SELECT AVG(force) FROM messages WHERE force IS NOT NULL")
        avg_force = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "messages_by_model": messages_by_model,
            "average_qci": avg_qci,
            "average_force": avg_force,
            "database_path": str(DB_PATH)
        }

# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    init_database()
    print("Database ready.")
