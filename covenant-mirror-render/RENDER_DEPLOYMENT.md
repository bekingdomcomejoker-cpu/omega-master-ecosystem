# COVENANT MIRROR X11 - RENDER DEPLOYMENT GUIDE

**Complete step-by-step guide to deploy the backend to Render and connect the frontend.**

---

## 🎯 WHAT WE'RE DOING

1. Deploy FastAPI backend to Render
2. Configure Gemini API key as environment variable
3. Update frontend to connect to live Render backend
4. Verify end-to-end system works

---

## 📋 PREREQUISITES

- GitHub account with repository access
- Render account (https://render.com - free tier available)
- Gemini API key (https://aistudio.google.com/app/apikeys)

---

## STEP 1: PREPARE GITHUB REPOSITORY

### 1.1 Push code to GitHub

```bash
cd /home/ubuntu/covenant-mirror-x11
git add -A
git commit -m "feat: Complete Covenant Mirror X11 with multi-model support and markdown rendering"
git push origin main
```

### 1.2 Verify repository structure

Your GitHub repo should have:
```
covenant-mirror-x11/
├── client/                 # React frontend
├── backend/                # FastAPI backend
│   ├── main.py            # Main server
│   ├── database.py        # SQLite persistence
│   ├── pipeline_v2.py     # Multi-model pipeline
│   ├── multi_model.py     # Model adapters
│   └── requirements.txt    # Python dependencies
├── RENDER_DEPLOYMENT.md   # This file
└── README_COMPLETE.md     # System documentation
```

---

## STEP 2: CREATE RENDER ACCOUNT & WEB SERVICE

### 2.1 Go to Render Dashboard

1. Visit https://render.com
2. Sign up or log in
3. Go to Dashboard

### 2.2 Create New Web Service

1. Click "New +" button
2. Select "Web Service"
3. Connect GitHub repository
   - Click "Connect GitHub Account" if needed
   - Search for "covenant-mirror-x11"
   - Click "Connect"

### 2.3 Configure Service

**Basic Settings:**
- **Name**: `covenant-mirror-backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && python main.py`
- **Plan**: Free (or paid if you prefer)

### 2.4 Add Environment Variables

Click "Advanced" and add:

| Key | Value | Notes |
|-----|-------|-------|
| `GEMINI_API_KEY` | `your_gemini_api_key_here` | Get from https://aistudio.google.com/app/apikeys |
| `PORT` | `8000` | Default port |
| `HOST` | `0.0.0.0` | Listen on all interfaces |

**IMPORTANT**: Never commit API keys to GitHub. Always use environment variables.

### 2.5 Deploy

1. Click "Create Web Service"
2. Render will automatically start building
3. Wait for deployment to complete (usually 2-3 minutes)
4. You'll see a URL like: `https://covenant-mirror-backend.onrender.com`

### 2.6 Verify Backend is Running

```bash
curl https://covenant-mirror-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "uptime_seconds": 123.45,
  "active_sessions": 0
}
```

---

## STEP 3: UPDATE FRONTEND CONFIGURATION

### 3.1 Update WebSocket URL

Edit `client/src/constants.ts`:

```typescript
export const WS_CONFIG = {
  URL: process.env.REACT_APP_WS_URL || "wss://covenant-mirror-backend.onrender.com/ws/covenant",
  RECONNECT_INTERVAL: 3000,
  MAX_RETRIES: 5
}
```

### 3.2 Create `.env.local` for local testing

Create `client/.env.local`:

```
REACT_APP_WS_URL=wss://covenant-mirror-backend.onrender.com/ws/covenant
```

### 3.3 Test locally first

```bash
cd client
pnpm dev
```

Open http://localhost:5173 and test:
1. Click "Hello AI"
2. Type a message
3. Click "Speak"
4. Verify response streams from Render backend

---

## STEP 4: DEPLOY FRONTEND TO MANUS

### 4.1 Update Manus project

The frontend is already initialized in Manus. Just update the WebSocket URL:

Edit in Manus Management UI or via:
```bash
# Update the constants file
cd /home/ubuntu/covenant-mirror-x11/client/src
# Edit constants.ts with new WebSocket URL
```

### 4.2 Save checkpoint

```bash
webdev_save_checkpoint --description "Update WebSocket URL to Render backend"
```

### 4.3 Publish to Manus

1. Go to Management UI
2. Click "Publish" button
3. Frontend will be live at: `https://covenant-mirror-x11.manus.space` (or your custom domain)

---

## STEP 5: VERIFY END-TO-END SYSTEM

### 5.1 Test from Manus Frontend

1. Open `https://covenant-mirror-x11.manus.space`
2. Verify connection status shows "Connected"
3. Send a message
4. Verify response streams from Render backend
5. Refresh page
6. Verify interaction is still visible (persistence)

### 5.2 Test Session Replay

1. Click "Operator Mode"
2. Click "Load Sessions"
3. Click on a previous session
4. Verify replay shows all interactions

### 5.3 Test Mode Switching

1. Click "Public / Altar" mode
2. Verify minimal UI
3. Send a message
4. Verify it works
5. Switch back to "Operator Mode"
6. Verify full dashboard

---

## 🔧 TROUBLESHOOTING

### WebSocket Connection Failed

**Problem**: "WebSocket connection failed"

**Solution**:
1. Check Render backend status: https://render.com/dashboard
2. Verify backend is running: `curl https://covenant-mirror-backend.onrender.com/health`
3. Check browser console for exact error
4. Verify WebSocket URL in constants.ts is correct
5. Check CORS is enabled (it is by default in main.py)

### Gemini API Error

**Problem**: "GEMINI_API_KEY environment variable not set"

**Solution**:
1. Go to Render dashboard
2. Select your service
3. Go to "Environment"
4. Verify `GEMINI_API_KEY` is set
5. Restart service: Click "Manual Deploy"

### Database Locked

**Problem**: "database is locked"

**Solution**:
1. This is normal on free tier (SQLite on ephemeral storage)
2. Render restarts services periodically
3. Data will be lost on restart (use paid tier for persistence)
4. To keep data, upgrade to paid tier or use PostgreSQL

### Slow Responses

**Problem**: Responses take a long time

**Solution**:
1. Free tier Render instances spin down after inactivity
2. First request after idle will be slow (cold start)
3. Upgrade to paid tier for always-on
4. Check Gemini API quota: https://aistudio.google.com/app/apikeys

---

## 📊 MONITORING

### Check Backend Logs

1. Go to Render dashboard
2. Select your service
3. Click "Logs"
4. See real-time server output

### Check Metrics

```bash
curl https://covenant-mirror-backend.onrender.com/metrics
```

### Check Statistics

```bash
curl https://covenant-mirror-backend.onrender.com/stats
```

---

## 🚀 NEXT STEPS

### Optional: Add Custom Domain

1. Go to Render dashboard
2. Select your service
3. Go to "Settings"
4. Add custom domain
5. Update DNS records

### Optional: Enable Paid Tier

1. Free tier has limitations:
   - Spins down after 15 minutes of inactivity
   - Data lost on restart
   - Limited resources
2. Upgrade to paid for:
   - Always-on service
   - Persistent storage
   - Better performance

### Optional: Add PostgreSQL

For production-grade persistence:
1. Create PostgreSQL database on Render
2. Update `database.py` to use PostgreSQL instead of SQLite
3. Update connection string in environment variables

---

## 📝 FINAL CHECKLIST

Before considering deployment complete:

- [ ] Backend deployed to Render
- [ ] Gemini API key configured as environment variable
- [ ] Backend health check passes
- [ ] Frontend updated with Render WebSocket URL
- [ ] Frontend deployed to Manus
- [ ] WebSocket connection works
- [ ] Can send message and receive response
- [ ] Response streams in real-time
- [ ] Page refresh shows persistent data
- [ ] Session replay works
- [ ] Mode switching works
- [ ] State switching works

---

## 🎯 DEFINITION OF DONE

✅ Open the page → Frontend loads from Manus  
✅ Send a message → WebSocket connects to Render backend  
✅ See Gemini respond live → Streaming works  
✅ Refresh the page → Still see the interaction (SQLite persistence)  
✅ Replay past sessions → Session history works  
✅ Switch between modes → Operator/Public toggle works  

---

## 📞 SUPPORT

### Common Issues

| Issue | Solution |
|-------|----------|
| WebSocket fails | Check Render backend status, verify URL |
| Gemini error | Check API key in Render environment variables |
| Slow first request | Free tier spins down, upgrade for always-on |
| Data lost on restart | Use paid tier or PostgreSQL for persistence |
| CORS error | Already enabled in main.py, check browser console |

### Getting Help

1. Check Render logs: https://render.com/dashboard
2. Check browser console: F12 → Console tab
3. Check backend health: `curl https://covenant-mirror-backend.onrender.com/health`
4. Check Gemini API status: https://aistudio.google.com/app/apikeys

---

## 🎓 ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────┐
│  Frontend (Manus)                   │
│  https://covenant-mirror-x11.       │
│  manus.space                        │
│  (React 19 + WebSocket)             │
└──────────────┬──────────────────────┘
               │ wss://
               ▼
┌─────────────────────────────────────┐
│  Backend (Render)                   │
│  https://covenant-mirror-backend.   │
│  onrender.com                       │
│  (FastAPI + Gemini + Multi-model)   │
└──────────────┬──────────────────────┘
               │ SQL
               ▼
┌─────────────────────────────────────┐
│  Database (Render Ephemeral)        │
│  SQLite (or PostgreSQL on paid)     │
│  covenant_mirror.db                 │
└─────────────────────────────────────┘
```

---

**Status**: ✅ READY FOR DEPLOYMENT

This is the complete system. Deploy it to Render and it will be live.
