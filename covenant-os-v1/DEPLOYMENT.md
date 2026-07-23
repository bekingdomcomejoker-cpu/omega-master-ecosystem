# 🚀 Covenant OS Deployment Guide

This guide covers deploying Covenant OS to GitHub and Render.

---

## 📦 Package Contents

```
covenant-os/
├── ai/                      # Vow Renewal Protocol
├── federation/              # Omega Federation
├── tools/                   # All analyzers (YouTube, Facebook, etc.)
├── core/                    # Omega Spore
├── covenant_os.py           # Main launcher
├── demo.py                  # Interactive demo
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
├── INSTALL.md               # Installation guide
├── DEPLOYMENT.md            # This file
├── LICENSE                  # Covenant License
├── .gitignore               # Git ignore rules
├── Procfile                 # Render deployment
└── render.yaml              # Render config
```

---

## 🌐 Deploy to GitHub

### Step 1: Create GitHub Repository

```bash
# On GitHub.com:
# 1. Click "New Repository"
# 2. Name: covenant-os
# 3. Description: The Operating System that Runs on Truth
# 4. Public or Private (your choice)
# 5. DO NOT initialize with README (we have one)
# 6. Click "Create repository"
```

### Step 2: Push to GitHub

```bash
# Extract the zip file
unzip covenant-os.zip
cd covenant-os

# Initialize git
git init
git add .
git commit -m "Initial commit: Covenant OS v1.0"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/covenant-os.git

# Push
git branch -M main
git push -u origin main
```

### Step 3: Done! 🎉

Your repository is now live at:
`https://github.com/YOUR_USERNAME/covenant-os`

---

## ☁️ Deploy to Render

### Method 1: Deploy from GitHub (Recommended)

**Step 1:** Push to GitHub (see above)

**Step 2:** Connect to Render

1. Go to https://render.com
2. Sign up or log in
3. Click "New +" → "Web Service"
4. Connect your GitHub account
5. Select your `covenant-os` repository
6. Configure:
   - **Name:** covenant-os
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 covenant_os.py`
   - **Instance Type:** Free (or paid for production)

**Step 3:** Click "Create Web Service"

Render will automatically deploy your app!

### Method 2: Deploy from Git Repository

```bash
# On Render:
# 1. New + → Web Service
# 2. "Public Git repository"
# 3. Paste your GitHub repo URL
# 4. Follow same config as Method 1
```

### Method 3: Manual Deploy (if needed)

```bash
# Create a Render account
# Install Render CLI
npm install -g @render/cli

# Login
render login

# Create service
render services create

# Deploy
render deploy
```

---

## ⚙️ Environment Variables (Optional)

If you need to add API keys or config:

On Render:
1. Go to your service dashboard
2. Click "Environment"
3. Add variables:
   - `GEMINI_API_KEY` (for video analysis)
   - `FACEBOOK_TOKEN` (for Facebook analyzer)
   - `TELEGRAM_TOKEN` (for Telegram analyzer)
   - etc.

---

## 🧪 Test Your Deployment

### Test GitHub:
```bash
git clone https://github.com/YOUR_USERNAME/covenant-os.git
cd covenant-os
pip install -r requirements.txt
python3 covenant_os.py status
```

### Test Render:
```bash
# Your app will be at:
https://covenant-os.onrender.com

# Or whatever URL Render gives you
```

---

## 📊 Monitoring

### On Render:
- View logs in real-time
- Monitor resource usage
- Set up alerts
- Auto-deploy on git push

### Health Check:
```bash
curl https://your-app.onrender.com/status
```

---

## 🔄 Update Deployment

### Update on GitHub:
```bash
git add .
git commit -m "Update: description of changes"
git push
```

### Update on Render:
If connected to GitHub, Render auto-deploys on push!

Or manually:
```bash
render deploy
```

---

## 🛠️ Troubleshooting

### Build fails on Render:
- Check Python version (3.9+)
- Verify requirements.txt has all dependencies
- Check logs in Render dashboard

### App crashes:
- Check Render logs
- Verify environment variables
- Test locally first

### Port issues:
Render automatically handles ports. No config needed.

---

## 📱 Mobile Access

Once deployed to Render, you can access Covenant OS from:
- Any web browser
- Mobile devices
- Old Android phones via browser
- Anywhere with internet

---

## 🔐 Security Notes

- Don't commit API keys to GitHub
- Use Render environment variables for secrets
- Keep dependencies updated
- Use HTTPS (Render provides free SSL)

---

## 💡 Tips

1. **Free Tier:** Render free tier spins down after inactivity
2. **Keep Alive:** Use a ping service or upgrade to paid
3. **Logs:** Check Render logs for debugging
4. **Scaling:** Upgrade instance for production use

---

## 🙏 Support

For issues:
1. Check GitHub Issues
2. Review Render logs
3. Test locally first
4. Open a new issue with details

---

**🌌 Covenant OS** - *The Operating System that Runs on Truth*

> *"Till test do us part. Not by my hand, but by His."*  
> *God → You → Me*

Chicka chicka, orange. 🍊
