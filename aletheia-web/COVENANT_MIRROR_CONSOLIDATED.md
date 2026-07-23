# Covenant Mirror X11 - Consolidated Dashboard

This is the unified, production-ready dashboard for the Covenant Mirror X11 system. It integrates:

- **Frontend**: React + TypeScript + TailwindCSS (in `client/`)
- **Backend**: Node.js server with FastAPI integration (in `server/`)
- **Automation**: ADB + Termux scripts for sovereign Android control (in `automation/`)
- **Deployment**: Render.com ready with `render.yaml`

## Quick Start

### Local Development
```bash
pnpm install
pnpm dev
```

### Deploy to Render
```bash
# The render.yaml is configured for automatic deployment
# Push to GitHub and Render will detect and deploy automatically
git push origin main
```

### Android Automation Setup
See `automation/README_AUTOMATION.md` for step-by-step instructions on setting up the ADB + Termux layer.

## Architecture

```
┌─────────────────────────────────────┐
│  Frontend (React)                   │
│  Aletheia Web Dashboard             │
└──────────────┬──────────────────────┘
               │ HTTP/WebSocket
               ▼
┌─────────────────────────────────────┐
│  Backend (Node.js + FastAPI)        │
│  Server Integration Layer           │
└──────────────┬──────────────────────┘
               │ ADB Commands
               ▼
┌─────────────────────────────────────┐
│  Android Automation (Termux)        │
│  Sovereign Local Control            │
└─────────────────────────────────────┘
```

## Key Features

- **No Authentication Required**: Direct access to the dashboard
- **Real-time Streaming**: WebSocket integration for live responses
- **Android Control**: Send messages via ADB without API keys
- **Persistent Storage**: SQLite database for session history
- **Render Compatible**: One-click deployment to Render.com
- **Termux Ready**: Scripts installable on Android via Termux

## Deployment Status

- ✅ Frontend: Ready for Render
- ✅ Backend: Ready for Render
- ✅ Automation: Ready for Termux
- ✅ Documentation: Complete

## Next Steps

1. Push to GitHub: `git push origin main`
2. Render will auto-deploy from `render.yaml`
3. Set `GEMINI_API_KEY` in Render environment variables
4. Access the dashboard at your Render URL
5. Setup Android automation following `automation/README_AUTOMATION.md`

---

**Status**: ✅ PRODUCTION READY
**Last Updated**: 2026-02-21
