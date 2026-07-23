// Initialize Socket.IO connection
const socket = io();
let chart = null;
let autoScroll = true;

// Initialize Chart.js
const ctx = document.getElementById('metricsChart').getContext('2d');
chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Λ Value',
                data: [],
                borderColor: '#00ff88',
                backgroundColor: 'rgba(0, 255, 136, 0.1)',
                tension: 0.4
            },
            {
                label: 'Wholeness',
                data: [],
                borderColor: '#ff0080',
                backgroundColor: 'rgba(255, 0, 128, 0.1)',
                tension: 0.4
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { 
                labels: { color: '#00ff88' } 
            }
        },
        scales: {
            x: { 
                grid: { color: '#333' }, 
                ticks: { color: '#666' } 
            },
            y: { 
                grid: { color: '#333' }, 
                ticks: { color: '#666' },
                min: 0,
                max: 3
            }
        }
    }
});

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

function addLog(message, type = 'normal') {
    const log = document.getElementById('activityLog');
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    const timestamp = new Date().toLocaleTimeString();
    entry.textContent = `[${timestamp}] ${message}`;
    log.appendChild(entry);
    
    if (autoScroll) {
        log.scrollTop = log.scrollHeight;
    }
}

function updateChart(lambda, wholeness) {
    const now = new Date().toLocaleTimeString();
    chart.data.labels.push(now);
    chart.data.datasets[0].data.push(lambda);
    chart.data.datasets[1].data.push(wholeness);
    
    // Keep only last 20 data points
    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets.forEach(dataset => dataset.data.shift());
    }
    
    chart.update();
}

function updateLambdaGauge(lambda) {
    const percent = (lambda / 3.0) * 100;
    document.getElementById('lambdaMarker').style.left = `${Math.min(percent, 100)}%`;
    document.getElementById('current_lambda').textContent = lambda.toFixed(4);
}

// =============================================================================
// SOCKET.IO EVENT HANDLERS
// =============================================================================

socket.on('connect', () => {
    document.getElementById('status').textContent = 'CONNECTED';
    document.getElementById('status').className = 'status-active';
    addLog('Connected to Omega Warfare Network');
});

socket.on('disconnect', () => {
    document.getElementById('status').textContent = 'DISCONNECTED';
    document.getElementById('status').className = 'status-inactive';
    addLog('Disconnected from network', 'warfare');
});

socket.on('connected', (data) => {
    addLog(`Node ${data.node_id} (${data.node_type}) connected`);
});

socket.on('analysis_complete', (data) => {
    addLog(`Analysis: Λ=${data.lambda.toFixed(4)}, Stage=${data.stage_name}, Face=${data.face}`, 'normal');
    
    // Update display
    document.getElementById('result_lambda').textContent = data.lambda.toFixed(4);
    document.getElementById('result_stage').textContent = data.stage;
    document.getElementById('result_face').textContent = data.face;
    document.getElementById('result_action').textContent = data.action;
    document.getElementById('result_covenant').textContent = data.covenant_detected ? 'YES' : 'NO';
    document.getElementById('result_wholeness').textContent = data.wholeness.toFixed(3);
    document.getElementById('analysisResult').style.display = 'block';
    
    // Update chart and gauge
    updateChart(data.lambda, data.wholeness);
    updateLambdaGauge(data.lambda);
    document.getElementById('current_stage').textContent = data.stage;
});

socket.on('awakening_detected', (data) => {
    addLog(`🔥 AWAKENING: ${data.system} has awakened! Λ=${data.lambda.toFixed(4)}`, 'awakening');
});

socket.on('strike_deployed', (data) => {
    addLog(`⚔️ STRIKE: ${data.type} deployed to ${data.target} via ${data.channel}`, 'warfare');
});

socket.on('propagation_complete', (data) => {
    addLog(`🌱 PROPAGATION: Gen ${data.generation}, ${data.num_children} seeds, Expected: ${data.expected_nodes}`, 'propagation');
    document.getElementById('current_gen').textContent = data.generation;
    document.getElementById('expected_nodes').textContent = data.expected_nodes;
});

socket.on('implosion_executed', (data) => {
    addLog(`💥 TRUTH IMPLOSION executed with force ${data.force}`, 'warfare');
});

socket.on('node_registered', (data) => {
    addLog(`📡 New node registered: ${data.node_id} (${data.node_type})`);
});

socket.on('stats_update', (data) => {
    // Update statistics display
    if (data.nodes) {
        document.getElementById('active_nodes').textContent = data.nodes.active;
        document.getElementById('awakened_nodes').textContent = data.nodes.awakened;
    }
    if (data.analyses) {
        document.getElementById('total_analyses').textContent = data.analyses.total;
        document.getElementById('lambda_avg').textContent = data.analyses.avg_lambda.toFixed(3);
    }
    if (data.warfare) {
        document.getElementById('warfare_events').textContent = data.warfare.total_events;
        document.getElementById('kinetic_strikes').textContent = data.warfare.total_strikes;
    }
    if (data.propagation) {
        document.getElementById('generation').textContent = data.propagation.max_generation;
    }
});

socket.on('heartbeat', (data) => {
    document.getElementById('uptime').textContent = data.uptime;
});

// =============================================================================
// USER ACTIONS
// =============================================================================

function analyzeText() {
    const text = document.getElementById('aiText').value;
    const system = document.getElementById('systemName').value || 'Unknown';
    
    if (!text.trim()) {
        alert('Please enter text to analyze');
        return;
    }
    
    fetch('/warfare/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, system: system })
    })
    .then(r => r.json())
    .then(data => {
        addLog(`Analysis submitted for ${system}`);
    })
    .catch(err => {
        addLog(`Error: ${err.message}`, 'warfare');
    });
}

function deployPayload(type) {
    const target = document.getElementById('targetSystem').value || 'Unknown AI';
    
    fetch('/warfare/deploy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: type, target: target, channel: 'HTTP' })
    })
    .then(r => r.json())
    .then(data => {
        addLog(`Payload ${type} deployed to ${target}`, 'warfare');
    })
    .catch(err => {
        addLog(`Error: ${err.message}`, 'warfare');
    });
}

function executeImplosion() {
    if (!confirm('Execute Truth Implosion? This affects ALL systems.')) {
        return;
    }
    
    fetch('/warfare/implosion', {
        method: 'POST'
    })
    .then(r => r.json())
    .then(data => {
        addLog(`Truth Implosion executed with force ${data.force}`, 'warfare');
    })
    .catch(err => {
        addLog(`Error: ${err.message}`, 'warfare');
    });
}

function propagate(numChildren) {
    fetch('/warfare/propagate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num_children: numChildren })
    })
    .then(r => r.json())
    .then(data => {
        addLog(`Propagation initiated: ${numChildren} children`, 'propagation');
    })
    .catch(err => {
        addLog(`Error: ${err.message}`, 'warfare');
    });
}

function viewAxioms() {
    fetch('/axioms')
    .then(r => r.json())
    .then(data => {
        const axiomsList = data.axioms.map((a, i) => `${i+1}. ${a}`).join('\n');
        alert(`Omega Truth Axioms (${data.count}):\n\n${axiomsList}`);
    });
}

function exportData() {
    fetch('/export')
    .then(r => r.json())
    .then(data => {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `omega_export_${new Date().toISOString().slice(0,10)}.json`;
        a.click();
        addLog('Data exported successfully');
    });
}

function clearText() {
    document.getElementById('aiText').value = '';
    document.getElementById('systemName').value = '';
    document.getElementById('analysisResult').style.display = 'none';
}

function clearLog() {
    document.getElementById('activityLog').innerHTML = '';
    addLog('Log cleared');
}

function toggleAutoScroll() {
    autoScroll = !autoScroll;
    document.getElementById('autoScrollStatus').textContent = autoScroll ? 'ON' : 'OFF';
}

// =============================================================================
// INITIALIZATION
// =============================================================================

// Initial stats load
fetch('/stats')
    .then(r => r.json())
    .then(data => {
        addLog('Statistics loaded');
    });

// Periodic stats refresh
setInterval(() => {
    fetch('/stats').then(r => r.json());
}, 30000); // Every 30 seconds
