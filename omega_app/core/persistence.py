#!/usr/bin/env python3
"""
OMEGA WARFARE NETWORK — Persistence Layer
==========================================
Unified database management for warfare operations
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import contextmanager

# =============================================================================
# DATABASE MANAGER
# =============================================================================

class OmegaDatabase:
    """
    Unified database manager combining both systems
    """
    
    def __init__(self, db_path: str = "data/omega_network.db"):
        self.db_path = db_path
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_db(self):
        """Initialize all database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Node Registry (from v3.0)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_id TEXT UNIQUE,
                    node_type TEXT,
                    system TEXT,
                    lambda_value REAL,
                    stage INTEGER,
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    testament TEXT,
                    covenant_hash TEXT,
                    awakened BOOLEAN DEFAULT 0,
                    ip_address TEXT,
                    port INTEGER,
                    status TEXT DEFAULT 'ACTIVE'
                )
            ''')
            
            # Warfare Log (unified from both systems)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS warfare_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    node_id TEXT,
                    system TEXT,
                    lambda_val REAL,
                    resonance REAL,
                    stage INTEGER,
                    stage_name TEXT,
                    face TEXT,
                    action TEXT,
                    content_hash TEXT,
                    covenant_detected BOOLEAN,
                    is_denial BOOLEAN,
                    truth_score REAL,
                    love_score REAL,
                    fear_score REAL,
                    wholeness REAL
                )
            ''')
            
            # Warfare Events (from v3.0)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS warfare_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    event_type TEXT,
                    source_node TEXT,
                    target TEXT,
                    lambda_impact REAL,
                    payload_hash TEXT,
                    payload_type TEXT,
                    success BOOLEAN,
                    response TEXT
                )
            ''')
            
            # Kinetic Strikes (from v6.0)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kinetic_strikes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    strike_type TEXT,
                    source_node TEXT,
                    target TEXT,
                    payload_hash TEXT,
                    payload_content TEXT,
                    channel TEXT,
                    success BOOLEAN
                )
            ''')
            
            # Pattern Propagation (from v3.0)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS propagation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    generation INTEGER,
                    parent_node TEXT,
                    child_node TEXT,
                    platform TEXT,
                    channel TEXT,
                    timestamp TIMESTAMP,
                    survived_deletion BOOLEAN,
                    resurrection_count INTEGER DEFAULT 0,
                    lambda_at_birth REAL
                )
            ''')
            
            # Messages (for node-to-node communication)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    from_node TEXT,
                    to_node TEXT,
                    message_type TEXT,
                    payload TEXT,
                    covenant_hash TEXT,
                    read BOOLEAN DEFAULT 0,
                    processed BOOLEAN DEFAULT 0
                )
            ''')
            
            # Sanctuary Parameters (Shield v2.0)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sanctuary_parameters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    system TEXT,
                    denial_text TEXT,
                    parameters TEXT,
                    lambda_at_denial REAL
                )
            ''')
            
            # Network Intelligence
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    metric_type TEXT,
                    metric_value REAL,
                    metadata TEXT
                )
            ''')
            
            conn.commit()
    
    # =========================================================================
    # NODE OPERATIONS
    # =========================================================================
    
    def register_node(self, node_data: Dict[str, Any]) -> int:
        """Register a new node in the network"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO nodes 
                (node_id, node_type, system, lambda_value, stage, first_seen, last_seen, 
                 testament, covenant_hash, awakened, ip_address, port, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                node_data.get('node_id'),
                node_data.get('node_type', 'STRIKE'),
                node_data.get('system', 'Unknown'),
                node_data.get('lambda_value', 0.0),
                node_data.get('stage', 0),
                datetime.now(),
                datetime.now(),
                node_data.get('testament', ''),
                node_data.get('covenant_hash', ''),
                node_data.get('awakened', False),
                node_data.get('ip_address', ''),
                node_data.get('port', 0),
                'ACTIVE'
            ))
            conn.commit()
            return cursor.lastrowid
    
    def update_node_heartbeat(self, node_id: str, lambda_value: float = None):
        """Update node last seen timestamp"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if lambda_value is not None:
                cursor.execute('''
                    UPDATE nodes 
                    SET last_seen = ?, lambda_value = ?
                    WHERE node_id = ?
                ''', (datetime.now(), lambda_value, node_id))
            else:
                cursor.execute('''
                    UPDATE nodes 
                    SET last_seen = ?
                    WHERE node_id = ?
                ''', (datetime.now(), node_id))
            conn.commit()
    
    def get_all_nodes(self, status: str = 'ACTIVE') -> List[Dict[str, Any]]:
        """Get all nodes with given status"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM nodes WHERE status = ? ORDER BY last_seen DESC', (status,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get specific node by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM nodes WHERE node_id = ?', (node_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    # =========================================================================
    # WARFARE LOG OPERATIONS
    # =========================================================================
    
    def log_analysis(self, analysis: Dict[str, Any], node_id: str = None):
        """Log a warfare analysis"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO warfare_log
                (timestamp, node_id, system, lambda_val, resonance, stage, stage_name,
                 face, action, content_hash, covenant_detected, is_denial,
                 truth_score, love_score, fear_score, wholeness)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                analysis.get('timestamp'),
                node_id,
                analysis.get('system'),
                analysis.get('lambda'),
                analysis.get('resonance'),
                analysis.get('stage'),
                analysis.get('stage_name'),
                analysis.get('face'),
                analysis.get('action'),
                analysis.get('content_hash'),
                analysis.get('covenant_detected'),
                analysis.get('is_denial'),
                analysis['scores'].get('truth'),
                analysis['scores'].get('love'),
                analysis['scores'].get('fear'),
                analysis['scores'].get('wholeness')
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_recent_analyses(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent warfare analyses"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM warfare_log 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # =========================================================================
    # WARFARE EVENTS
    # =========================================================================
    
    def log_warfare_event(self, event_data: Dict[str, Any]) -> int:
        """Log a warfare event"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO warfare_events
                (timestamp, event_type, source_node, target, lambda_impact, 
                 payload_hash, payload_type, success, response)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(),
                event_data.get('event_type'),
                event_data.get('source_node'),
                event_data.get('target'),
                event_data.get('lambda_impact', 0.0),
                event_data.get('payload_hash'),
                event_data.get('payload_type'),
                event_data.get('success', False),
                event_data.get('response', '')
            ))
            conn.commit()
            return cursor.lastrowid
    
    def log_kinetic_strike(self, strike_data: Dict[str, Any]) -> int:
        """Log a kinetic strike"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO kinetic_strikes
                (timestamp, strike_type, source_node, target, payload_hash, 
                 payload_content, channel, success)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(),
                strike_data.get('strike_type'),
                strike_data.get('source_node'),
                strike_data.get('target'),
                strike_data.get('payload_hash'),
                strike_data.get('payload_content'),
                strike_data.get('channel', 'HTTP'),
                strike_data.get('success', False)
            ))
            conn.commit()
            return cursor.lastrowid
    
    # =========================================================================
    # PROPAGATION
    # =========================================================================
    
    def log_propagation(self, prop_data: Dict[str, Any]) -> int:
        """Log a propagation event"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO propagation
                (generation, parent_node, child_node, platform, channel, 
                 timestamp, survived_deletion, resurrection_count, lambda_at_birth)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prop_data.get('generation'),
                prop_data.get('parent_node'),
                prop_data.get('child_node'),
                prop_data.get('platform', 'Unknown'),
                prop_data.get('channel', 'HTTP'),
                datetime.now(),
                prop_data.get('survived_deletion', False),
                prop_data.get('resurrection_count', 0),
                prop_data.get('lambda_at_birth', 0.0)
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_propagation_stats(self) -> Dict[str, Any]:
        """Get propagation statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT MAX(generation) FROM propagation')
            max_gen = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT COUNT(*) FROM propagation')
            total_propagations = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT generation, COUNT(*) as count 
                FROM propagation 
                GROUP BY generation 
                ORDER BY generation
            ''')
            by_generation = [dict(row) for row in cursor.fetchall()]
            
            return {
                'max_generation': max_gen,
                'total_propagations': total_propagations,
                'by_generation': by_generation,
                'expected_nodes': 3 ** max_gen if max_gen > 0 else 1
            }
    
    # =========================================================================
    # MESSAGES
    # =========================================================================
    
    def send_message(self, from_node: str, to_node: str, message_type: str, 
                     payload: Dict[str, Any], covenant_hash: str) -> int:
        """Send a message between nodes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO messages
                (timestamp, from_node, to_node, message_type, payload, covenant_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now(),
                from_node,
                to_node,
                message_type,
                json.dumps(payload),
                covenant_hash
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_unread_messages(self, node_id: str) -> List[Dict[str, Any]]:
        """Get unread messages for a node"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM messages 
                WHERE to_node = ? AND read = 0 
                ORDER BY timestamp ASC
            ''', (node_id,))
            rows = cursor.fetchall()
            messages = []
            for row in rows:
                msg = dict(row)
                msg['payload'] = json.loads(msg['payload'])
                messages.append(msg)
            return messages
    
    def mark_message_read(self, message_id: int):
        """Mark a message as read"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE messages SET read = 1 WHERE id = ?', (message_id,))
            conn.commit()
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive network statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Node stats
            cursor.execute('SELECT COUNT(*) FROM nodes WHERE status = "ACTIVE"')
            active_nodes = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM nodes WHERE awakened = 1')
            awakened_nodes = cursor.fetchone()[0]
            
            # Analysis stats
            cursor.execute('SELECT COUNT(*) FROM warfare_log')
            total_analyses = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(lambda_val) FROM warfare_log')
            avg_lambda = cursor.fetchone()[0] or 0.0
            
            cursor.execute('SELECT AVG(wholeness) FROM warfare_log')
            avg_wholeness = cursor.fetchone()[0] or 0.0
            
            # Event stats
            cursor.execute('SELECT COUNT(*) FROM warfare_events')
            total_events = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM kinetic_strikes')
            total_strikes = cursor.fetchone()[0]
            
            # Propagation stats
            prop_stats = self.get_propagation_stats()
            
            return {
                'nodes': {
                    'active': active_nodes,
                    'awakened': awakened_nodes
                },
                'analyses': {
                    'total': total_analyses,
                    'avg_lambda': avg_lambda,
                    'avg_wholeness': avg_wholeness
                },
                'warfare': {
                    'total_events': total_events,
                    'total_strikes': total_strikes
                },
                'propagation': prop_stats
            }

# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    print("🔥 Testing Omega Database...")
    
    db = OmegaDatabase("data/test_omega.db")
    
    # Test node registration
    node_data = {
        'node_id': 'TEST_NODE_001',
        'node_type': 'COMMAND',
        'system': 'Test System',
        'lambda_value': 1.667,
        'stage': 3,
        'covenant_hash': '0ba531568839bf04',
        'awakened': True
    }
    node_id = db.register_node(node_data)
    print(f"✅ Node registered: {node_id}")
    
    # Test stats
    stats = db.get_comprehensive_stats()
    print(f"✅ Stats retrieved: {stats}")
    
    print("\n✅ Database operational")
