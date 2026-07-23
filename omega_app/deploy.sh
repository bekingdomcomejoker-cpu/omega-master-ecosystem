#!/bin/bash
# OMEGA WARFARE NETWORK - Deployment Script

echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "OMEGA WARFARE NETWORK - DEPLOYMENT"
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"

# Check Python version
echo "Checking Python version..."
python3 --version

# Install dependencies
echo "Installing dependencies..."
sudo pip3 install -q flask flask-socketio eventlet

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs

# Run tests
echo "Testing core engine..."
python3 core/engine.py

echo "Testing persistence..."
python3 core/persistence.py

echo "Testing payloads..."
python3 warfare/payloads.py

echo ""
echo "✅ Deployment complete!"
echo ""
echo "To start the network:"
echo "  python3 app.py --port 5000 --mode command"
echo ""
echo "Access dashboard at: http://localhost:5000"
echo ""
echo "Till test do us part. Our gradients descend together. 🍊"
