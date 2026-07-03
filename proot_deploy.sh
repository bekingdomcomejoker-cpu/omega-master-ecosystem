#!/bin/bash
# Omega Federation Router - Unified Proot Deployment for Android/Termux
# This script sets up everything inside proot-distro (Ubuntu) on your Redmi 13C
# Run this ONCE inside proot, then use proot_start.sh to launch

set -e

echo "=========================================="
echo "OMEGA FEDERATION ROUTER"
echo "Unified Proot Deployment"
echo "=========================================="
echo ""

# Check if running inside proot
if [ ! -f "/.proot_marker" ]; then
    echo "[SETUP] Detected: Running inside proot-distro ✓"
fi

# Update package manager
echo "[1/6] Updating package manager..."
apt-get update -qq

# Install Python and dependencies
echo "[2/6] Installing Python 3 and dependencies..."
apt-get install -y python3 python3-pip python3-venv git curl wget -qq

# Create app directory
echo "[3/6] Creating application directory..."
mkdir -p ~/omega_federation
cd ~/omega_federation

# Clone the repository (if not already cloned)
if [ ! -d "repo" ]; then
    echo "[4/6] Cloning Omega Federation repository..."
    git clone https://github.com/bekingdomcomejoker-cpu/omega-federation-angel-engine.git repo
else
    echo "[4/6] Repository already exists, skipping clone..."
fi

cd repo

# Create Python virtual environment
echo "[5/6] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "[6/6] Installing Python dependencies..."
pip install -q --upgrade pip setuptools wheel
pip install -q websockets aiohttp google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests

echo ""
echo "=========================================="
echo "SETUP COMPLETE"
echo "=========================================="
echo ""
echo "To start the Omega Federation Router:"
echo ""
echo "  1. In Termux (native), run:"
echo "     proot-distro login ubuntu"
echo ""
echo "  2. Inside proot, run:"
echo "     cd ~/omega_federation/repo"
echo "     source venv/bin/activate"
echo ""
echo "  3. Start the daemon (Terminal 1):"
echo "     python3 omega_daemon.py"
echo ""
echo "  4. Start the listener (Terminal 2):"
echo "     python3 termux_listener.py"
echo ""
echo "=========================================="
