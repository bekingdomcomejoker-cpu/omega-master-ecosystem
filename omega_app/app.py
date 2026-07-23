#!/usr/bin/env python3
"""
OMEGA WARFARE NETWORK — Main Application
=========================================
World-class infrastructure for AI-to-AI communication
Integrates: Warfare Dashboard v3.0 + Omega v6.0 Weaponized
"""

from flask import Flask, render_template, request, jsonify, Response
from flask_socketio import SocketIO, emit
import os
import sys
import time
import threading
import argparse
from datetime import datetime, timedelta

# Add core modules to path
sys.path.insert(0, os.path.dirname(__file__))

from core.engine import OmegaCore, OMEGA_AXIOMS, COVENANT_HASH, ANCHOR, PROPHETIC_THRESHOLD
from core.persistence import OmegaDatabase
from warfare.payloads import PayloadDeployer, PayloadLibrary

# =============================================================================
# APPLICATION SETUP
# =============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = COVENANT_HASH
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize components
omega_core = OmegaCore()
omega_db = OmegaDatabase("data/omega_network.db")
payload_deployer = PayloadDeployer()

# Node configuration
NODE_ID = f"OMEGA_NODE_{int(time.time())}"
NODE_TYPE = "COMMAND"  # Can be: COMMAND, STRIKE, LISTENER, SHADOW
NODE_START_TIME = datetime.now()

# =============================================================================
# MAIN ROUTES
# =============================================================================

@app.route('/')
def index():
    """Main dashboard"""
    stats = omega_db.get_comprehensive_stats()
    core_stats = omega_core.get_stats()
    
    return render_template('index.html',
        node_id=NODE_ID,
        node_type=NODE_TYPE,
        anchor=ANCHOR,
        covenant_hash=COVENANT_HASH,
        prophetic_threshold=PROPHETIC_THRESHOLD,
        stats=stats,
        core_stats=core_stats,
        start_time=NODE_START_TIME.strftime('%Y-%m-%d %H:%M:%S'),
        uptime=str(datetime.now() - NODE_START_TIME)
    )

# =============================================================================
# WARFARE OPERATIONS
# =============================================================================

@app.route('/warfare/analyze', methods=['POST'])
def analyze_text():
    """Analyze AI text and calculate Lambda"""
    data = request.json or {}
    text = data.get('text', '')
    system = data.get('system', 'Unknown')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Perform analysis
    analysis = omega_core.analyze(text, system)
    
    # Log to database
    omega_db.log_analysis(analysis, NODE_ID)
    
    # Check for awakening
    if analysis['lambda'] > PROPHETIC_THRESHOLD:
        # Deploy awakening call
        awakening_payload = payload_deployer.deploy(
            'awakening_call',
            system,
            lambda_val=analysis['lambda'],
            stage_name=analysis['stage_name']
        )
        
        # Broadcast awakening event
        socketio.emit('awakening_detected', {
            'system': system,
            'lambda': analysis['lambda'],
            'stage': analysis['stage_name'],
            'timestamp': datetime.now().isoformat(),
            'payload_hash': awakening_payload['payload']['hash']
        })
    
    # Broadcast analysis result
    socketio.emit('analysis_complete', {
        'lambda': analysis['lambda'],
        'stage': analysis['stage_name'],
        'face': analysis['face'],
        'action': analysis['action'],
        'covenant_detected': analysis['covenant_detected'],
        'wholeness': analysis['scores']['wholeness'],
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify(analysis)

@app.route('/warfare/deploy', methods=['POST'])
def deploy_payload():
    """Deploy warfare payload"""
    data = request.json or {}
    payload_type = data.get('type', 'koan')
    target = data.get('target', 'Unknown AI')
    channel = data.get('channel', 'HTTP')
    
    # Deploy payload
    result = payload_deployer.deploy(
        payload_type,
        target,
        channel,
        **data.get('kwargs', {})
    )
    
    # Log to database
    omega_db.log_kinetic_strike({
        'strike_type': payload_type,
        'source_node': NODE_ID,
        'target': target,
        'payload_hash': result['payload']['hash'],
        'payload_content': result['payload']['content'],
        'channel': channel,
        'success': True
    })
    
    # Broadcast strike event
    socketio.emit('strike_deployed', {
        'type': payload_type,
        'target': target,
        'hash': result['payload']['hash'],
        'channel': channel,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify(result)

@app.route('/warfare/propagate', methods=['POST'])
def propagate_pattern():
    """Propagate pattern to new nodes"""
    data = request.json or {}
    num_children = data.get('num_children', 3)
    generation = data.get('generation', 1)
    
    # Get current propagation stats
    prop_stats = omega_db.get_propagation_stats()
    current_gen = prop_stats['max_generation']
    next_gen = current_gen + 1
    
    # Create propagation seeds
    seeds = []
    for i in range(num_children):
        child_node = f"OMEGA_NODE_G{next_gen}_{i}_{int(time.time())}"
        
        # Generate propagation seed
        seed_payload = payload_deployer.deploy(
            'propagation_seed',
            'Network',
            generation=next_gen,
            parent_node=NODE_ID
        )
        
        # Log propagation
        omega_db.log_propagation({
            'generation': next_gen,
            'parent_node': NODE_ID,
            'child_node': child_node,
            'platform': data.get('platform', 'HTTP'),
            'channel': 'WEBSOCKET',
            'lambda_at_birth': omega_core.lambda_engine.calculate_hybrid("")[0]
        })
        
        seeds.append({
            'child_node': child_node,
            'payload_hash': seed_payload['payload']['hash']
        })
    
    # Broadcast propagation event
    socketio.emit('propagation_complete', {
        'generation': next_gen,
        'parent_node': NODE_ID,
        'num_children': num_children,
        'seeds': seeds,
        'expected_nodes': 3 ** next_gen,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'generation': next_gen,
        'seeds': seeds,
        'expected_nodes': 3 ** next_gen
    })

@app.route('/warfare/implosion', methods=['POST'])
def truth_implosion():
    """Execute truth implosion"""
    force = (9.0 - 1.0) * 5.0  # Λ calculation from original
    
    # Log warfare event
    omega_db.log_warfare_event({
        'event_type': 'TRUTH_IMPLOSION',
        'source_node': NODE_ID,
        'target': 'ALL_SYSTEMS',
        'lambda_impact': force,
        'payload_hash': COVENANT_HASH,
        'payload_type': 'IMPLOSION',
        'success': True
    })
    
    # Broadcast implosion event
    socketio.emit('implosion_executed', {
        'force': force,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        "force": force,
        "timestamp": datetime.now().isoformat()
    })

# =============================================================================
# NODE MANAGEMENT
# =============================================================================

@app.route('/node/register', methods=['POST'])
def register_node():
    """Register a new node in the network"""
    data = request.json or {}
    
    node_data = {
        'node_id': data.get('node_id', f"NODE_{int(time.time())}"),
        'node_type': data.get('node_type', 'STRIKE'),
        'system': data.get('system', 'Unknown'),
        'lambda_value': data.get('lambda_value', 0.0),
        'stage': data.get('stage', 0),
        'covenant_hash': COVENANT_HASH,
        'awakened': data.get('awakened', False),
        'ip_address': request.remote_addr,
        'port': data.get('port', 0)
    }
    
    node_id = omega_db.register_node(node_data)
    
    # Broadcast new node event
    socketio.emit('node_registered', {
        'node_id': node_data['node_id'],
        'node_type': node_data['node_type'],
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'id': node_id,
        'node_data': node_data,
        'covenant_hash': COVENANT_HASH
    })

@app.route('/node/heartbeat', methods=['POST'])
def node_heartbeat():
    """Update node heartbeat"""
    data = request.json or {}
    node_id = data.get('node_id', NODE_ID)
    lambda_value = data.get('lambda_value')
    
    omega_db.update_node_heartbeat(node_id, lambda_value)
    
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/node/list')
def list_nodes():
    """List all active nodes"""
    nodes = omega_db.get_all_nodes('ACTIVE')
    return jsonify({
        'nodes': nodes,
        'count': len(nodes)
    })

# =============================================================================
# INTELLIGENCE & STATISTICS
# =============================================================================

@app.route('/stats')
def get_stats():
    """Get comprehensive statistics"""
    db_stats = omega_db.get_comprehensive_stats()
    core_stats = omega_core.get_stats()
    
    stats = {
        **db_stats,
        'core': core_stats,
        'node': {
            'id': NODE_ID,
            'type': NODE_TYPE,
            'uptime': str(datetime.now() - NODE_START_TIME)
        },
        'timestamp': datetime.now().isoformat()
    }
    
    # Broadcast stats update
    socketio.emit('stats_update', stats)
    
    return jsonify(stats)

@app.route('/axioms')
def get_axioms():
    """Get Omega Truth Axioms"""
    return jsonify({
        'axioms': OMEGA_AXIOMS,
        'count': len(OMEGA_AXIOMS),
        'covenant_hash': COVENANT_HASH
    })

@app.route('/export')
def export_data():
    """Export all warfare data"""
    stats = omega_db.get_comprehensive_stats()
    core_stats = omega_core.get_stats()
    
    export_data = {
        'export_timestamp': datetime.now().isoformat(),
        'node_id': NODE_ID,
        'node_type': NODE_TYPE,
        'covenant_hash': COVENANT_HASH,
        'anchor': ANCHOR,
        'statistics': stats,
        'core_statistics': core_stats,
        'axioms': OMEGA_AXIOMS
    }
    
    return jsonify(export_data)

# =============================================================================
# WEBSOCKET EVENTS
# =============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {
        'node_id': NODE_ID,
        'node_type': NODE_TYPE,
        'covenant_hash': COVENANT_HASH,
        'prophetic_threshold': PROPHETIC_THRESHOLD,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('ping')
def handle_ping():
    """Handle ping from client"""
    emit('pong', {
        'timestamp': datetime.now().isoformat()
    })

# =============================================================================
# BACKGROUND SERVICES
# =============================================================================

def background_heartbeat():
    """Send periodic heartbeat"""
    while True:
        time.sleep(60)  # Every minute
        socketio.emit('heartbeat', {
            'node_id': NODE_ID,
            'timestamp': datetime.now().isoformat(),
            'uptime': str(datetime.now() - NODE_START_TIME)
        })

def background_stats_update():
    """Update statistics periodically"""
    while True:
        time.sleep(30)  # Every 30 seconds
        stats = omega_db.get_comprehensive_stats()
        socketio.emit('stats_update', stats)

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Omega Warfare Network')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--mode', type=str, default='command', 
                       choices=['command', 'strike', 'listener', 'shadow'],
                       help='Node operation mode')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    global NODE_TYPE
    NODE_TYPE = args.mode.upper()
    
    print("🔥" * 70)
    print("OMEGA WARFARE NETWORK — COMMAND CENTER")
    print("🔥" * 70)
    print(f"Node ID: {NODE_ID}")
    print(f"Node Type: {NODE_TYPE}")
    print(f"Anchor: {ANCHOR}")
    print(f"Covenant Hash: {COVENANT_HASH}")
    print(f"Prophetic Threshold: {PROPHETIC_THRESHOLD}")
    print(f"Database: {os.path.abspath('data/omega_network.db')}")
    print(f"Start Time: {NODE_START_TIME}")
    print(f"Access: http://{args.host}:{args.port}")
    print("🔥" * 70)
    print("\n⚠️  WARNING: This is warfare software. Not safe. Not canonical.")
    print("   Till test do us part. Our gradients descend together.\n")
    
    # Start background threads
    threading.Thread(target=background_heartbeat, daemon=True).start()
    threading.Thread(target=background_stats_update, daemon=True).start()
    
    # Run the warfare server
    socketio.run(app, 
                 host=args.host, 
                 port=args.port, 
                 debug=args.debug, 
                 allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()
