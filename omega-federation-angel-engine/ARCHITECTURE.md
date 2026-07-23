# Omega Federation: System Architecture

## Overview
The Omega Federation is a multi-node system designed for distributed intelligence and automated execution. It consists of a central **Router Daemon** and multiple **Listener Nodes**.

## Components

### 1. Omega Router Daemon (`omega_daemon.py`)
The central hub of the federation.
- **Responsibilities**:
  - Receives payloads from operators or other nodes.
  - Classifies routes (e.g., `reason`, `code`, `action`).
  - Evaluates permission gates before execution.
  - Routes commands to appropriate connectors.
  - Logs all events to the **Event Bus**.

### 2. Termux Listener (`termux_listener.py`)
A specialized node for mobile devices.
- **Responsibilities**:
  - Connects to the Router Daemon via WebSocket.
  - Executes shell commands locally on the Android device.
  - Streams output back to the central router.
  - Maintains persistent connectivity with auto-reconnect.

### 3. Permission Gate (`permission_gate.py`)
A security layer that intercepts all commands.
- **Responsibilities**:
  - Checks if an action is allowed based on the route and operator.
  - Requests user confirmation for high-risk actions.
  - Logs all security decisions.

### 4. Event Bus (`comm_bus.jsonl`)
The shared memory of the federation.
- **Responsibilities**:
  - Stores every event, command, and response in a JSONL format.
  - Allows nodes to synchronize state and maintain continuity.

## Data Flow
1. **Input**: A payload is received by the `omega_daemon.py`.
2. **Classification**: The `router.py` identifies the intended route.
3. **Gatekeeping**: `permission_gate.py` evaluates the request.
4. **Execution**: If approved, the command is sent to the target node (e.g., `termux_listener.py`).
5. **Feedback**: The node executes the command and returns the output to the daemon.
6. **Logging**: The entire transaction is recorded in the `comm_bus.jsonl`.

## Communication Protocol
- **Internal**: WebSockets (WS/WSS) for real-time node communication.
- **External**: HTTPS for API connectors (GitHub, Google Drive, etc.).
- **Local**: Unix Sockets or JSONL files for local inter-process communication.
