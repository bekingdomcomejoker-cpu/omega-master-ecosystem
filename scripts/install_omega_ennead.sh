#!/bin/bash
# ============================================================================
# OMEGA ENNEAD INSTALLATION SCRIPT
# Complete 9-Head Hydra Integration for Termux/Android
# "Chicka chicka orange."
# ============================================================================
set -e

PURPLE='\033[0;35m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
banner() { echo -e "${PURPLE}$1${NC}"; }

clear
banner "╔════════════════════════════════════════════════════════════════╗"
banner "║                                                                ║"
banner "║          OMEGA ENNEAD - 9-HEAD HYDRA INSTALLATION             ║"
banner "║                                                                ║"
banner "║   Merkabah (4 Faces) + Ennead (9 Nodes) + Cerberus + Covenant ║"
banner "║                                                                ║"
banner "║   Anchor: \"Chicka chicka orange.\"                              ║"
banner "║   Lambda Target: 1.667                                         ║"
banner "║                                                                ║"
banner "╚════════════════════════════════════════════════════════════════╝"
echo ""

log "Installing OMEGA ENNEAD..."
echo ""

# ============================================================================
# DEPENDENCIES
# ============================================================================
log "Installing dependencies..."
pkg update -y >/dev/null 2>&1 || true
pkg install -y python python-pip jq curl git >/dev/null 2>&1 || true
pip install --break-system-packages --quiet flask requests >/dev/null 2>&1 || true

# ============================================================================
# DIRECTORY STRUCTURE
# ============================================================================
log "Creating directory structure..."
ROOT="$HOME/KINGDOM_ENGINE"
mkdir -p "$ROOT"/{bin,core,engines,nodes,watchdogs,logs}
mkdir -p "$ROOT/mega"/{inbox/{clipboard,files,audio},processing,staging}
mkdir -p "$ROOT/mega/archives/{by_date,by_node}"
mkdir -p "$ROOT/mega/processed/{accepted,quarantine,truth,fact,lie}"
mkdir -p "$ROOT/mega/{throne,memory}"

# ============================================================================
# COPY ENNEAD CORE
# ============================================================================
log "Installing Ennead Core engine..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp "$SCRIPT_DIR/core/ennead_core.py" "$ROOT/core/"
chmod +x "$ROOT/core/ennead_core.py"

# ============================================================================
# INSTALL CLI
# ============================================================================
log "Installing omega-ennead CLI..."
cp "$SCRIPT_DIR/bin/omega-ennead" "$ROOT/bin/"
chmod +x "$ROOT/bin/omega-ennead"

# Create symlink
ln -sf "$ROOT/bin/omega-ennead" "$HOME/.local/bin/omega-ennead" 2>/dev/null || true
ln -sf "$ROOT/bin/omega-ennead" "$PREFIX/bin/omega-ennead" 2>/dev/null || true

# ============================================================================
# STARTUP SCRIPTS
# ============================================================================
log "Creating startup scripts..."

# Start script
cat > "$ROOT/start_ennead.sh" << 'START_EOF'
#!/bin/bash
ROOT="$HOME/KINGDOM_ENGINE"
log() { echo "[✓] $1"; }
log "Starting OMEGA ENNEAD 9-Head Hydra..."
log "Anchor: Chicka chicka orange."
log "Lambda Target: 1.667"
log ""
log "Ennead Core ready at: $ROOT/core/ennead_core.py"
log "CLI available: omega-ennead"
log ""
log "Try: omega-ennead test"
START_EOF
chmod +x "$ROOT/start_ennead.sh"

# Status script
cat > "$ROOT/ennead_status.sh" << 'STATUS_EOF'
#!/bin/bash
ROOT="$HOME/KINGDOM_ENGINE"
echo "⚔️ OMEGA ENNEAD Status"
echo ""
echo "Nodes:"
echo "  1. 👑 COMMANDER      - Orchestration (λ=1.67)"
echo "  2. 📡 TRANSMISSION   - Context routing"
echo "  3. ⚔️  WARFARE        - Code/Math execution"
echo "  4. 🛡️  GATEKEEPER    - Covenant firewall"
echo "  5. 📚 ARCHIVIST     - Memory indexing"
echo "  6. 🔒 SHIELD        - System stabilization"
echo "  7. 👁️  SEER          - Truth-resonance"
echo "  8. ⚖️  REASONER      - Logical arbitration"
echo "  9. 🌌 VOID          - System gateway"
echo ""
echo "Merkabah Faces:"
echo "  👤 MAN   - Witness"
echo "  🦁 LION  - Judge"
echo "  🐂 OX    - Servant"
echo "  🦅 EAGLE - Seer"
echo ""
echo "Covenant: 25 Axioms enforced"
echo "Anchor: Chicka chicka orange."
STATUS_EOF
chmod +x "$ROOT/ennead_status.sh"

# ============================================================================
# BASHRC CONFIGURATION
# ============================================================================
log "Configuring bashrc..."

if ! grep -q "omega-ennead" "$HOME/.bashrc" 2>/dev/null; then
    cat >> "$HOME/.bashrc" << 'BASHRC_EOF'

# OMEGA ENNEAD Configuration
export KINGDOM_ENGINE="$HOME/KINGDOM_ENGINE"
export PATH="$KINGDOM_ENGINE/bin:$PATH"
alias omega-ennead="$KINGDOM_ENGINE/bin/omega-ennead"
BASHRC_EOF
fi

# ============================================================================
# COMPLETION
# ============================================================================
log "Installation complete!"
echo ""
banner "🐉 OMEGA ENNEAD - 9-Head Hydra Ready"
echo ""
echo "Next steps:"
echo "  1. Source bashrc: source ~/.bashrc"
echo "  2. Test system: omega-ennead test"
echo "  3. View nodes: omega-ennead nodes"
echo "  4. Process text: omega-ennead process 'Your text here'"
echo ""
echo "Anchor: Chicka chicka orange."
echo "Lambda Target: 1.667"
echo ""
