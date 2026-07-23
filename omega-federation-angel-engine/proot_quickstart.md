# Omega Federation Router - Proot Quick Start

## One-Time Setup (Run ONCE)

### In Termux (native shell):
```bash
proot-distro login ubuntu
```

### Inside proot (Ubuntu):
```bash
bash ~/proot_deploy.sh
```

This will:
- Install Python 3, pip, git, and dependencies
- Clone the Omega Federation repository
- Set up a Python virtual environment
- Install all required packages

---

## Daily Usage (Run every time you want to use it)

### Terminal 1: Start the Daemon
```bash
proot-distro login ubuntu
cd ~/omega_federation/repo
source venv/bin/activate
python3 omega_daemon.py
```

### Terminal 2: Start the Listener
```bash
proot-distro login ubuntu
cd ~/omega_federation/repo
source venv/bin/activate
python3 termux_listener.py
```

---

## What's Running

| Component | Purpose |
|-----------|---------|
| `omega_daemon.py` | Core router that processes commands and routes through permission gates |
| `termux_listener.py` | Listens for commands and executes them locally |
| `connectors_*` | GitHub, Google Drive, MikroTik integrations |
| `runtime/` | Event logs, state snapshots, audit trail |

---

## Troubleshooting

**"Command not found: proot-distro"**
- Install proot-distro in native Termux: `pkg install proot-distro`

**"ModuleNotFoundError: No module named 'websockets'"**
- Make sure you're inside the virtual environment: `source venv/bin/activate`

**"Connection refused"**
- Make sure both daemon and listener are running in separate terminals

---

## Files Location (Inside Proot)

```
~/omega_federation/
├── repo/                          # Main repository
│   ├── omega_daemon.py            # Daemon process
│   ├── termux_listener.py         # Listener process
│   ├── omega_router/
│   │   ├── router.py              # Core router
│   │   ├── connectors_*.py        # All connectors
│   │   └── runtime/               # Event logs
│   ├── config/                    # Configuration files
│   └── venv/                      # Python virtual environment
```

---

## Next Steps

1. Run the setup script
2. Start the daemon in Terminal 1
3. Start the listener in Terminal 2
4. Send commands through the router
5. Monitor output in both terminals

Everything is now unified inside proot. No more Ubuntu/Debian/Termux confusion.
