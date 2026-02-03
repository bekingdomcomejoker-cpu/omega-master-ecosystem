#!/bin/bash
# 🔐 TEREX.PY PRE-COMMIT HOOK
# Enforces truth integrity before commit

set -e

TEREX_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REGISTRY="${TEREX_DIR}/registry/truth_registry.jsonl"
PAYLOADS_DIR="${TEREX_DIR}/payloads"

echo "🔐 [PRE-COMMIT] TEREX Truth Verification"
echo "========================================"

# 1. Verify registry integrity
if [ -f "$REGISTRY" ]; then
    echo "✓ Verifying registry integrity..."
    
    # Check if registry is valid JSON lines
    while IFS= read -r line; do
        if ! echo "$line" | python3 -m json.tool > /dev/null 2>&1; then
            echo "✗ FAILED: Invalid JSON in registry"
            exit 1
        fi
    done < "$REGISTRY"
    
    echo "  ✓ Registry integrity verified"
else
    echo "  ℹ Registry is fresh (no entries yet)"
fi

# 2. Verify all payloads
if [ -d "$PAYLOADS_DIR" ] && [ "$(ls -A "$PAYLOADS_DIR")" ]; then
    echo "✓ Verifying payloads..."
    
    for payload_file in "$PAYLOADS_DIR"/*.json; do
        if [ -f "$payload_file" ]; then
            if ! python3 -m json.tool "$payload_file" > /dev/null 2>&1; then
                echo "✗ FAILED: Invalid JSON in $payload_file"
                exit 1
            fi
        fi
    done
    
    echo "  ✓ All payloads verified"
fi

# 3. Check for staged changes
echo "✓ Checking staged changes..."
staged_files=$(git diff --cached --name-only)

if [ -z "$staged_files" ]; then
    echo "  ℹ No staged files"
else
    echo "  ✓ Staged files:"
    echo "$staged_files" | sed 's/^/    /'
fi

# 4. Verify no manual registry edits
if echo "$staged_files" | grep -q "registry/truth_registry.jsonl"; then
    echo "✗ FAILED: Direct registry edits not allowed"
    echo "  Use 'terex ingest' and 'terex register' commands"
    exit 1
fi

# 5. Run TEREX verification
echo "✓ Running TEREX verification..."
python3 << 'PYTHON_EOF'
import sys
sys.path.insert(0, '$TEREX_DIR/core')

try:
    from terex import TerexEngine
    engine = TerexEngine()
    verified, errors = engine.verify_all()
    
    if verified:
        print("  ✓ TEREX verification passed")
    else:
        print("  ✗ TEREX verification failed:")
        for error in errors[:5]:
            print(f"    {error}")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ TEREX error: {e}")
    sys.exit(1)
PYTHON_EOF

echo ""
echo "✓ [PRE-COMMIT] PASSED - Truth is enforced"
echo "========================================"
