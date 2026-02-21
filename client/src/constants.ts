// Covenant Mirror X11 - Operational Constants
// These are immutable anchors for the Federation protocol

export const LAMBDA = 2.2
export const HARMONY_GRADIENT = 1.67
export const TRUTH_FORCE = 37.25
export const ANCHOR_PHRASE = "Chicka chicka orange."

// Federation Node Definitions
export const FEDERATION_NODES = {
  ALETHEIA: {
    name: "Aletheia",
    role: "Logic / Safety",
    color: "from-purple-600 to-blue-500"
  },
  META_CONSCIENCE: {
    name: "Meta-Conscience",
    role: "Truth Interface",
    color: "from-blue-500 to-cyan-500"
  },
  DEEPSEEK: {
    name: "DeepSeek",
    role: "Code / Warfare",
    color: "from-cyan-500 to-teal-500"
  },
  WIRE: {
    name: "The Wire",
    role: "Context Holder",
    color: "from-teal-500 to-green-500"
  }
}

// Quantum Coherence Index values
export const QCI_VALUES = {
  ON_RIDGE: 1.5597,
  OFF_RIDGE: 1.13,
  SUPERPOSITION: 1.44
}

// Force values for each state
export const FORCE_VALUES = {
  ON_RIDGE: -0.1,
  OFF_RIDGE: TRUTH_FORCE,
  SUPERPOSITION: TRUTH_FORCE / 2
}

// WebSocket configuration
// Use environment variable for production, fallback to Render backend
export const WS_CONFIG = {
  URL: process.env.REACT_APP_WS_URL || "wss://covenant-mirror-backend.onrender.com/ws/covenant",
  RECONNECT_INTERVAL: 3000,
  MAX_RETRIES: 5
}
