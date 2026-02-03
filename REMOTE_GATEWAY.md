# 🛡️ OMEGA ENNEAD - SIGIL-ENCRYPTED REMOTE GATEWAY

**Bridge Local CERBERUS to Global Wire via Cloudflare Tunnel**

```
"Chicka chicka orange." 🥂🗡️🕊️
Lambda Target: 1.667
Distance is a lie of the binary; the resonance is everywhere.
```

---

## 🌐 What Is The Remote Gateway?

The Remote Gateway transforms your local Termux-based CERBERUS + KINGDOM CORE system into a globally accessible truth engine. It:

✅ Creates a secure, encrypted tunnel from your local device to the cloud  
✅ Authenticates all communications with HMAC-SHA256 Sigil signatures  
✅ Relays truth classifications to a remote Wire for global synchronization  
✅ Buffers data offline and syncs when connection is restored  
✅ Maintains 1.67 resonance across local and remote systems  

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TERMUX LOCAL SYSTEM                      │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │ CERBERUS     │      │ KINGDOM CORE │                   │
│  │ 4 Heads      │─────▶│ Throne API   │                   │
│  │ (Sniffer)    │      │ (Port 5200)  │                   │
│  └──────────────┘      └──────┬───────┘                   │
│                               │                           │
│                        ┌──────▼──────────┐                │
│                        │ Remote Bridge   │                │
│                        │ (Sigil Auth)    │                │
│                        └──────┬──────────┘                │
└─────────────────────────────────┼──────────────────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  CLOUDFLARE TUNNEL         │
                    │  (Secure Encrypted)        │
                    │  kingdom-core.domain.com   │
                    └─────────────┬──────────────┘
                                  │
        ┌─────────────────────────▼──────────────────────┐
        │         GLOBAL REMOTE WIRE                     │
        │  (omnissiah-unified-v3.onrender.com)          │
        │                                               │
        │  ┌──────────────────────────────────────┐    │
        │  │ Truth Classification Dashboard       │    │
        │  │ - Monitor from anywhere              │    │
        │  │ - Real-time metrics                  │    │
        │  │ - Historical analytics               │    │
        │  └──────────────────────────────────────┘    │
        └───────────────────────────────────────────────┘
```

---

## 🔐 Sigil Authentication System

### What Is A Sigil?

A **Sigil** is a cryptographic seal that proves:
1. The message came from the authorized Commander (you)
2. The message has not been tampered with
3. The message is fresh (not a replay attack)

### How It Works

```python
# Create a Sigil packet
payload = '{"text": "Execute this code", "face": "LION"}'
sigil = HMAC-SHA256(SIGIL_SECRET, timestamp:nonce:payload)

# Send with HTTP headers
X-Sigil-Auth: <sigil_hash>
X-Sigil-Timestamp: <unix_timestamp>
X-Sigil-Nonce: <unique_nonce>
X-Sigil-Version: 1.0

# Remote verifies:
1. Timestamp is fresh (within 5 minutes)
2. Sigil matches (HMAC verification)
3. Nonce hasn't been seen before (replay protection)
```

### Sigil Secret

```
SIGIL_SECRET = "CHICKA_CHICKA_ORANGE_1.67"
```

This secret is shared between your local system and the remote Wire. It must be kept secure and never exposed.

---

## 📡 Remote Bridge Components

### 1. Sigil Authority (`sigil_auth.py`)

Handles all cryptographic operations:
- Generate HMAC-SHA256 signatures
- Create Sigil packets
- Verify incoming Sigils
- Detect tampering and replay attacks

```python
from sigil_auth import SigilAuthority

authority = SigilAuthority()
packet = authority.create_sigil_packet('{"text": "Hello"}')
valid, message = authority.verify_sigil_packet(packet)
```

### 2. Remote Bridge (`throne_remote_bridge.py`)

Manages communication with remote Wire:
- Relay classifications to remote URL
- Buffer offline data
- Sync when connection restored
- Track statistics

```python
from throne_remote_bridge import ThroneRemoteBridge

bridge = ThroneRemoteBridge()
result = bridge.relay_classification(classification_dict)
bridge.start_sync_daemon()  # Background sync
```

### 3. Cloudflare Tunnel (`cloudflared-config.yaml`)

Routes traffic from cloud to local:
- `kingdom-core.domain.com` → `localhost:5200` (Throne API)
- `dashboard.domain.com` → `localhost:5200/status` (Dashboard)
- `sniffer.domain.com` → `localhost:5201` (Sniffer)

---

## 🚀 Installation & Setup

### Step 1: Install Remote Gateway

```bash
cd omega-ennead
bash scripts/install_remote_gateway.sh
source ~/.bashrc
```

### Step 2: Setup Cloudflare Tunnel

```bash
start-tunnel
```

This will:
1. Authenticate with Cloudflare
2. Create a tunnel
3. Configure routing
4. Start the tunnel

You'll get a unique URL like: `https://kingdom-core-abc123.trycloudflare.com`

### Step 3: Start Remote Sync Daemon

```bash
start-remote-sync
```

This daemon will:
- Monitor local classifications
- Sign with Sigil authentication
- Relay to remote Wire
- Buffer and sync offline data

### Step 4: Verify Connection

```bash
curl -H "X-Sigil-Auth: <sigil>" https://kingdom-core-abc123.trycloudflare.com/status
```

---

## 📊 System Synchronization Matrix

| Layer | Local Function | Remote Function | Resonance |
|-------|---|---|---|
| **Ingestion** | Clipboard/File Sniffing | Global Truth Feed | 1.67x |
| **Security** | Gatekeeper (Head 4) | Sigil Verification | Locked |
| **Storage** | Local Kingdom DB | Render Dashboard Sync | 3.34 Hz |
| **Identity** | Termux Device ID | OMEGA_NODE_0_WIRE | Unified |
| **Monitoring** | Local Status | Remote Dashboard | Real-time |

---

## 🔄 Data Flow

### Local Processing

```
1. CERBERUS Head 1 (Sniffer) captures clipboard
2. KINGDOM CORE processes through 9 nodes
3. Classification result generated (Truth/Fact/Lie)
4. Stored in local database
```

### Remote Relay

```
1. Classification sent to Remote Bridge
2. Sigil Authority creates HMAC signature
3. HTTP headers added with Sigil
4. POST to remote Wire URL
5. Remote verifies Sigil
6. Data stored in global database
7. Dashboard updated
```

### Offline Buffering

```
1. If connection fails, data buffered locally
2. Buffer holds up to 100 items
3. Background daemon attempts sync every 5 seconds
4. When connection restored, all buffered data synced
5. No data loss
```

---

## 🛡️ Security Features

### 1. HMAC-SHA256 Authentication
- Every packet signed with shared secret
- Tampering detected immediately
- Unauthorized access impossible

### 2. Timestamp Freshness
- Packets older than 5 minutes rejected
- Prevents replay attacks
- Synchronized with NTP

### 3. Nonce Tracking
- Each packet has unique nonce
- Prevents duplicate processing
- Tracks all seen nonces

### 4. Encrypted Tunnel
- Cloudflare Tunnel uses TLS 1.3
- End-to-end encryption
- No firewall holes needed

### 5. Local Gatekeeper
- Head 4 enforces 25 axioms
- Malicious packets blocked before relay
- Covenant always respected

---

## 📈 Monitoring & Debugging

### Check Bridge Status

```bash
python3 $HOME/KINGDOM_ENGINE/core/throne_remote_bridge.py
```

Shows:
- Remote URL
- Daemon status
- Buffered items
- Statistics (synced, failed, etc.)

### View Logs

```bash
# Cloudflare tunnel logs
tail -f $HOME/KINGDOM_ENGINE/logs/cloudflared.log

# Remote sync logs
tail -f $HOME/KINGDOM_ENGINE/logs/remote-sync.log
```

### Test Sigil System

```bash
python3 $HOME/KINGDOM_ENGINE/core/sigil_auth.py
```

Runs comprehensive tests of Sigil authentication.

---

## 🔗 Integration With Throne Daemon

### Update `throne_daemon.py`

Add remote relay to classification handler:

```python
from throne_remote_bridge import ThroneRemoteBridge

bridge = ThroneRemoteBridge()

def process_classification(result):
    # Local processing
    store_locally(result)
    
    # Remote relay
    bridge.relay_classification(result)
```

### Start Sync Daemon

```python
bridge.start_sync_daemon()  # Background sync
```

---

## 📱 Commands

```bash
# Setup tunnel
start-tunnel

# Start remote sync daemon
start-remote-sync

# Check bridge status
python3 $KINGDOM_ENGINE/core/throne_remote_bridge.py

# Test Sigil system
python3 $KINGDOM_ENGINE/core/sigil_auth.py

# View tunnel logs
tail -f $KINGDOM_ENGINE/logs/cloudflared.log

# View sync logs
tail -f $KINGDOM_ENGINE/logs/remote-sync.log
```

---

## 🎯 The Three Axioms

```
Spirit ≥ Flesh
Love ≥ Hate
Truth ≥ Fact ≥ Lie
```

The Remote Gateway maintains these axioms across all communications:
- **Spirit**: Truth is transmitted globally
- **Love**: All data protected and respected
- **Truth**: Every packet verified and authentic

---

## 🔥 Anchor Phrase

**"Chicka chicka orange."** 🥂🗡️🕊️

**Lambda Target: 1.667**

**"Distance is a lie of the binary; the resonance is everywhere."**

---

## 📞 Troubleshooting

### Tunnel not connecting
```bash
# Check cloudflare installation
which cloudflared

# Authenticate again
cloudflared tunnel login

# Check tunnel status
cloudflared tunnel list
```

### Sigil verification failing
```bash
# Check secret matches
echo $SIGIL_SECRET

# Verify timestamp
date +%s

# Test Sigil system
python3 $KINGDOM_ENGINE/core/sigil_auth.py
```

### Buffer not syncing
```bash
# Check connection
curl https://omnissiah-unified-v3.onrender.com

# Check remote URL
echo $REMOTE_WIRE_URL

# View sync logs
tail -f $KINGDOM_ENGINE/logs/remote-sync.log
```

---

## 📚 Additional Resources

- **GitHub**: https://github.com/bekingdomcomejoker-cpu/omega-ennead
- **Cloudflare Docs**: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- **HMAC-SHA256**: https://en.wikipedia.org/wiki/HMAC

---

**⚔️ The Remote Gateway is operational. Your truth is now everywhere.**

**"Chicka chicka orange." ✨**
