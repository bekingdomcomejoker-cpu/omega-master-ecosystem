# Truth-in-Motion (TIM) Toolkit

**A neutral creative systems architecture for transmitting insight without coercion.**

---

## Core Invariant

> **Truth = coherent relationship in motion.**
>
> If it coerces, it fails.
> If it doesn't move, it doesn't teach.

---

## What This Is

The TIM Toolkit is a diagnostic-driven creative engine that:

- **Compresses micro-truths** (jokes, insights, paradoxes) into temporal forms (songs, narratives)
- **Detects expectation breaks** (semantic surprises that signal deeper patterns)
- **Validates non-coercion** (ensures transmission doesn't manipulate or force)
- **Expands compressed wisdom** (1:100 joke ratio → 1:1,000 song ratio)
- **Self-corrects** (diagnostic flags guide refinement)

---

## Core Components

### 1. **Diagnostics** (`diagnostics.py`)

Status tracking and validation flags:

```python
class Diagnostic(Enum):
    UNDER_COMPRESSION = "UnderCompression"
    DECOHERENCE = "Decoherence"
    COERCION_DETECTED = "CoercionDetected"
    EXPECTATION_BREAK = "ExpectationBreak"
    COHERENCE_VERIFIED = "CoherenceVerified"
```

### 2. **Classifier** (`classifier.py`)

Detects expectation breaks and semantic surprises:

```python
classifier = ExpectationBreakClassifier()
breaks = classifier.detect_breaks(content)
# Returns: [{"type": "paradox", "position": 42, "confidence": 0.89}]
```

### 3. **Validator** (`validator.py`)

Enforces non-coercion and compression requirements:

```python
validator = TIMValidator()
is_valid = validator.validate(content, constraints)
# Checks: no manipulation, no forced conclusions, coherence maintained
```

### 4. **Compiler** (`compiler.py`)

Expands jokes into songs (micro-truths into temporal forms):

```python
compiler = TIMCompiler()
song = compiler.compile_joke_to_song(joke, boundary_insight)
# Output: Multi-verse narrative with rhythm and structure
```

### 5. **API** (`api.py`)

Clean interface with invariant enforcement:

```python
from tim_toolkit.api import compile_endpoint

result = compile_endpoint({
    "content": "Why did the map stop arguing? Because it noticed the footsteps.",
    "boundary_insight": "The ground records movement, not opinions.",
    "constraints": {"non_coercion": True}
})
```

---

## Quick Start

### Installation

```bash
git clone https://github.com/bekingdomcomejoker-cpu/tim-toolkit.git
cd tim-toolkit
pip install -r requirements.txt
```

### Basic Usage

```python
from tim_toolkit.api import compile_endpoint

# Compile a joke into a song
result = compile_endpoint({
    "content": "Why did the river refuse to argue with the bridge? Because it knew the bridge was just passing through.",
    "boundary_insight": "Structure is temporary; flow is eternal.",
    "constraints": {"non_coercion": True}
})

print(result)
# Output:
# {
#   "status": "success",
#   "song": "Verse 1: The river flows...",
#   "diagnostics": ["CoherenceVerified"],
#   "compression_ratio": 1.0
# }
```

### Advanced Usage

```python
from tim_toolkit.classifier import ExpectationBreakClassifier
from tim_toolkit.validator import TIMValidator

# Detect expectation breaks
classifier = ExpectationBreakClassifier()
breaks = classifier.detect_breaks(content)

# Validate non-coercion
validator = TIMValidator()
is_valid = validator.validate(content, {"non_coercion": True})

# Compile with diagnostics
compiler = TIMCompiler()
result = compiler.compile_joke_to_song(joke, insight)
print(f"Diagnostics: {result['diagnostics']}")
```

---

## Architecture

```
tim-toolkit/
├── tim_toolkit/
│   ├── __init__.py
│   ├── diagnostics.py       # Status & validation flags
│   ├── classifier.py        # Expectation break detection
│   ├── validator.py         # Non-coercion enforcement
│   ├── compiler.py          # Joke → Song compilation
│   └── api.py               # Main interface
├── examples/
│   ├── basic_compilation.py
│   ├── expectation_breaks.py
│   └── non_coercion_validation.py
├── tests/
│   ├── test_classifier.py
│   ├── test_validator.py
│   └── test_compiler.py
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Core Concepts

### Micro-Truth (Joke)

A compressed insight that breaks expectations:

```
"Why did the map stop arguing with the traveler?"
"Because it noticed the footsteps."
```

**Compression:** 1:100 (highly compressed)

### Macro-Truth (Song)

An expanded temporal form that unfolds the insight:

```
Verse 1: The map and traveler argued about the path...
Chorus: But the ground knows the truth...
Verse 2: Every footstep writes the real story...
Bridge: The map is just a guide, not the journey...
Outro: The path is written by walking...
```

**Expansion:** 1:1,000 (fully unfolded)

### Expectation Break

A moment where the audience's assumptions are violated, revealing deeper truth:

```
Expected: "Because it was wrong"
Actual: "Because it noticed the footsteps"

Break reveals: Maps are tools, not truth. Reality is written by movement.
```

### Non-Coercion Constraint

The transmission must:

- ✅ Invite, not demand
- ✅ Suggest, not impose
- ✅ Illuminate, not blind
- ✅ Open, not close
- ✅ Question, not answer

---

## Diagnostic Flags

| Flag | Meaning | Action |
|------|---------|--------|
| `UNDER_COMPRESSION` | Joke is too dense | Expand more |
| `DECOHERENCE` | Song loses the insight | Refocus narrative |
| `COERCION_DETECTED` | Transmission manipulates | Reframe as invitation |
| `EXPECTATION_BREAK` | Semantic surprise found | Amplify this moment |
| `COHERENCE_VERIFIED` | All systems aligned | Ready to transmit |

---

## API Reference

### `compile_endpoint(payload)`

Main compilation interface.

**Input:**
```python
{
    "content": str,              # Joke or micro-truth
    "boundary_insight": str,     # The deeper pattern
    "constraints": {
        "non_coercion": bool,    # Enforce non-coercion
        "max_length": int,       # Optional length limit
        "style": str             # Optional: "narrative", "lyrical", "philosophical"
    }
}
```

**Output:**
```python
{
    "status": "success" | "unstable" | "failed",
    "song": str,                 # Expanded temporal form
    "diagnostics": [str],        # Validation flags
    "compression_ratio": float,  # Expansion factor
    "metadata": {
        "breaks_detected": int,
        "coherence_score": float
    }
}
```

---

## Examples

See `/examples/` for complete working examples:

- `basic_compilation.py` - Simple joke → song
- `expectation_breaks.py` - Detecting semantic surprises
- `non_coercion_validation.py` - Ensuring non-manipulative transmission

---

## Testing

```bash
pytest tests/
```

---

## Philosophy

The TIM Toolkit is built on the principle that **truth doesn't need coercion**. If an insight requires force, manipulation, or pressure to land, it's not truth—it's propaganda.

True insight:
- Moves (doesn't stagnate)
- Invites (doesn't demand)
- Illuminates (doesn't blinds)
- Opens (doesn't closes)
- Questions (doesn't answers)

---

## License

MIT License - See LICENSE file for details

---

## Contributing

Contributions welcome. Please ensure all changes maintain the core invariant:

> **Truth = coherent relationship in motion.**
>
> If it coerces, it fails.
> If it doesn't move, it doesn't teach.

---

## Author

Built with 💓 for transmission without coercion.

**Chicka chicka orange.** 🍊

---

## Status

**Operational** | **Non-Coercive** | **Diagnostic-Driven** | **Ready for Deployment**
