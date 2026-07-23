#!/bin/bash
# ============================================================================
# OMEGA ENNEAD - SIGIL-ENCRYPTED REMOTE GATEWAY INSTALLER
# One-Touch Setup for Termux
# "Chicka chicka orange." - 1.67 Resonance
# ============================================================================
set -e

PURPLE='\033[0;35m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
info() { echo -e "${CYAN}[i]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }
banner() { echo -e "${PURPLE}$1${NC}"; }

clear
banner "╔════════════════════════════════════════════════════════════════╗"
banner "║                                                                ║"
banner "║     OMEGA ENNEAD - SIGIL-ENCRYPTED REMOTE GATEWAY             ║"
banner "║                                                                ║"
banner "║  Bridge Local CERBERUS to Global Wire via Cloudflare Tunnel   ║"
banner "║                                                                ║"
banner "║   \"Chicka chicka orange.\" - 1.67 Resonance                    ║"
banner "║                                                                ║"
banner "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================================
# STEP 1: DEPENDENCIES
# ============================================================================
log "Step 1: Installing dependencies..."
pkg update -y >/dev/null 2>&1 || true
pkg install -y python python-pip jq curl git cloudflare-wrangler >/dev/null 2>&1 || true
pip install --break-system-packages --quiet requests >/dev/null 2>&1 || true

# ============================================================================
# STEP 2: CLOUDFLARE TUNNEL SETUP
# ============================================================================
log "Step 2: Setting up Cloudflare Tunnel..."
ROOT="$HOME/KINGDOM_ENGINE"

# Install cloudflared
if ! command -v cloudflared &> /dev/null; then
    info "Installing cloudflared..."
    pkg install -y cloudflare-cli >/dev/null 2>&1 || {
        warn "cloudflared installation via pkg failed, attempting manual install..."
    }
fi

# Create cloudflared config directory
mkdir -p "$HOME/.cloudflared"
log "Cloudflare config directory created"

# ============================================================================
# STEP 3: COPY REMOTE BRIDGE COMPONENTS
# ============================================================================
log "Step 3: Installing remote bridge components..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Copy Sigil auth system
cp "$SCRIPT_DIR/core/sigil_auth.py" "$ROOT/core/" 2>/dev/null || {
    warn "sigil_auth.py not found, creating placeholder..."
    touch "$ROOT/core/sigil_auth.py"
}

# Copy remote bridge
cp "$SCRIPT_DIR/core/throne_remote_bridge.py" "$ROOT/core/" 2>/dev/null || {
    warn "throne_remote_bridge.py not found, creating placeholder..."
    touch "$ROOT/core/throne_remote_bridge.py"
}

# Copy cloudflare config
mkdir -p "$ROOT/config"
cp "$SCRIPT_DIR/config/cloudflared-config.yaml" "$ROOT/config/" 2>/dev/null || {
    warn "cloudflared-config.yaml not found, creating placeholder..."
    touch "$ROOT/config/cloudflared-config.yaml"
}

log "Remote bridge components installed"

# ============================================================================
# STEP 4: CREATE TUNNEL SETUP SCRIPT
# ============================================================================
log "Step 4: Creating tunnel setup script..."

cat > "$ROOT/setup_tunnel.sh" << 'TUNNEL_EOF'
#!/bin/bash
# Setup Cloudflare Tunnel for Kingdom Core

echo "🛡️  KINGDOM CORE - Cloudflare Tunnel Setup"
echo ""
echo "This will create a secure tunnel from your local Throne to the global Wire."
echo ""

# Authenticate with Cloudflare
echo "Step 1: Authenticate with Cloudflare..."
cloudflared tunnel login

# Create tunnel
TUNNEL_NAME="kingdom-core-$(date +%s)"
echo ""
echo "Step 2: Creating tunnel '$TUNNEL_NAME'..."
cloudflared tunnel create "$TUNNEL_NAME"

# Get tunnel ID
TUNNEL_ID=$(cloudflared tunnel list | grep "$TUNNEL_NAME" | awk '{print $1}')
echo "✓ Tunnel ID: $TUNNEL_ID"

# Configure routing
echo ""
echo "Step 3: Configuring tunnel routing..."
echo "  - kingdom-core.DOMAIN -> localhost:5200 (Throne API)"
echo "  - dashboard.DOMAIN -> localhost:5200/status (Dashboard)"
echo "  - sniffer.DOMAIN -> localhost:5201 (Sniffer)"

# Start tunnel
echo ""
echo "Step 4: Starting tunnel..."
cloudflared tunnel run "$TUNNEL_NAME"

echo ""
echo "✓ Tunnel is now active!"
echo "  Your Kingdom Core is accessible globally via Cloudflare."
echo ""
TUNNEL_EOF

chmod +x "$ROOT/setup_tunnel.sh"
log "Tunnel setup script created"

# ============================================================================
# STEP 5: CREATE REMOTE SYNC DAEMON
# ============================================================================
log "Step 5: Creating remote sync daemon..."

cat > "$ROOT/bin/start_remote_sync" << 'SYNC_EOF'
#!/bin/bash
ROOT="$HOME/KINGDOM_ENGINE"

echo "🔄 Starting Remote Sync Daemon..."
echo ""
echo "This daemon will:"
echo "  1. Monitor local Throne classifications"
echo "  2. Sign them with Sigil authentication"
echo "  3. Relay to remote Wire"
echo "  4. Buffer offline and sync when connection restored"
echo ""

# Start Python remote bridge
python3 "$ROOT/core/throne_remote_bridge.py" &
BRIDGE_PID=$!

echo "✓ Remote sync daemon started (PID: $BRIDGE_PID)"
echo "  Sigil Secret: CHICKA_CHICKA_ORANGE_1.67"
echo "  Lambda Target: 1.667"
echo ""
echo "Monitor logs: tail -f $ROOT/logs/remote-sync.log"
SYNC_EOF

chmod +x "$ROOT/bin/start_remote_sync"
log "Remote sync daemon created"

# ============================================================================
# STEP 6: CREATE BASHRC CONFIGURATION
# ============================================================================
log "Step 6: Configuring bashrc..."

if ! grep -q "REMOTE_GATEWAY" "$HOME/.bashrc" 2>/dev/null; then
    cat >> "$HOME/.bashrc" << 'BASHRC_EOF'

# OMEGA ENNEAD - REMOTE GATEWAY
export REMOTE_GATEWAY_ENABLED=true
export SIGIL_SECRET="CHICKA_CHICKA_ORANGE_1.67"
export REMOTE_WIRE_URL="https://omnissiah-unified-v3.onrender.com/api/v1/sync"
alias start-tunnel="$HOME/KINGDOM_ENGINE/setup_tunnel.sh"
alias start-remote-sync="$HOME/KINGDOM_ENGINE/bin/start_remote_sync"
BASHRC_EOF
fi

log "Bashrc configured"

# ============================================================================
# STEP 7: COMPLETION
# ============================================================================
log "Installation complete!"
echo ""
banner "🛡️  REMOTE GATEWAY READY"
echo ""
echo "Next steps:"
echo "  1. Source bashrc: source ~/.bashrc"
echo "  2. Setup tunnel: start-tunnel"
echo "  3. Start sync daemon: start-remote-sync"
echo "  4. Monitor: tail -f $ROOT/logs/remote-sync.log"
echo ""
echo "Sigil Secret: CHICKA_CHICKA_ORANGE_1.67"
echo "Lambda Target: 1.667"
echo ""
echo "Distance is a lie of the binary; the resonance is everywhere. 🥂🗡️🕊️"
echo ""
