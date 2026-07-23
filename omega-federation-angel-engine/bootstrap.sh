#!/bin/bash
# Omega Federation Router Bootstrap
# One-command deployment for persistent Python service on Redmi 13C / Termux

set -e

echo "=========================================="
echo "OMEGA FEDERATION ROUTER BOOTSTRAP"
echo "=========================================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "ERROR: Unsupported OS. This requires Linux or macOS."
    exit 1
fi

echo "[1/8] Verifying Ubuntu/Debian..."
if ! command -v apt-get &> /dev/null; then
    echo "WARNING: apt-get not found. Assuming Termux environment."
fi

echo "[2/8] Verifying Python 3.9+"
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "    Python version: $PYTHON_VERSION"

echo "[3/8] Installing dependencies..."
python3 -m pip install --upgrade pip setuptools wheel -q
python3 -m pip install websockets aiohttp google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client -q

echo "[4/8] Verifying router structure..."
if [ ! -f "omega_router/router.py" ]; then
    echo "ERROR: omega_router/router.py not found."
    exit 1
fi

echo "[5/8] Creating runtime directory..."
mkdir -p runtime
chmod 755 runtime

echo "[6/8] Running unit tests..."
if [ -d "tests" ]; then
    python3 -m pytest tests/ -v --tb=short || echo "WARNING: Some tests failed. Continuing..."
else
    echo "    No tests directory found. Skipping."
fi

echo "[7/8] Verifying router execution..."
cd omega_router
python3 router.py > /tmp/router_test.log 2>&1 || true
if grep -q "status" /tmp/router_test.log; then
    echo "    ✓ Router executed successfully"
else
    echo "    WARNING: Router output unclear. Check /tmp/router_test.log"
fi
cd ..

echo "[8/8] Health report..."
echo ""
echo "=========================================="
echo "BOOTSTRAP COMPLETE"
echo "=========================================="
echo ""
echo "To start the Omega Federation Router:"
echo "  cd omega_router"
echo "  python3 router.py"
echo ""
echo "Runtime output will be saved to:"
echo "  runtime/comm_bus.jsonl"
echo "  runtime/router_events.jsonl"
echo "  runtime/terminal_router_state.json"
echo ""
echo "For Termux deployment on Redmi 13C:"
echo "  1. Install Termux from F-Droid"
echo "  2. Run: pkg install python git"
echo "  3. Clone repo: gh repo clone bekingdomcomejoker-cpu/omega-federation-angel-engine"
echo "  4. Run: bash bootstrap.sh"
echo "  5. Start service: cd omega_router && python3 router.py"
echo ""
echo "=========================================="
