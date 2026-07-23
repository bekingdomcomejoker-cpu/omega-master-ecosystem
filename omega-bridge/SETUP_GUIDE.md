# OMEGA BRIDGE - Complete Setup Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- ✅ Redmi 13C with Termux installed
- ✅ Node.js installed on Termux (`pkg install nodejs`)
- ✅ Internet connection on both devices
- ✅ Web browser on your computer

### Step 1: Access the Dashboard

Open this URL in your browser:

```
https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer
```

You should see the OMEGA Bridge dashboard with a green terminal aesthetic.

### Step 2: Create a Session

1. Click the **"+ New Session"** button in the sidebar
2. A new session will be created with:
   - **Session ID**: e.g., `abc123`
   - **Connection Token**: e.g., `xyz789...`

**Copy the Connection Token** - you'll need it for the next step.

### Step 3: Get the Listener Script

Download or copy the `silent_listener.mjs` file to your Termux:

**Option A: Direct Download**
```bash
# In Termux
cd ~
curl -o silent_listener.mjs https://raw.githubusercontent.com/your-repo/omega-bridge/main/silent_listener.mjs
```

**Option B: Manual Copy**
```bash
# On your computer
scp /home/ubuntu/omega_bridge/silent_listener.mjs user@redmi:~/
```

**Option C: Manual Paste**
- Open the file on your computer
- Copy all content
- In Termux: `nano ~/silent_listener.mjs`
- Paste the content
- Press Ctrl+X, then Y, then Enter

### Step 4: Install Dependencies

In Termux:

```bash
npm install socket.io-client
```

### Step 5: Start the Listener

In Termux, run:

```bash
node ~/silent_listener.mjs https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer <YOUR_CONNECTION_TOKEN>
```

Replace `<YOUR_CONNECTION_TOKEN>` with the token from Step 2.

Example:
```bash
node ~/silent_listener.mjs https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer abc123xyz789def456
```

You should see:
```
[*] OMEGA BRIDGE - SILENT LISTENER (Socket.IO) v2.0
[*] Target URL: https://3000-i57mmtxn4knpj4c91pn2f-fc86f8e6.us1.manus.computer
[*] Resonance: 1.67x
[✓] Connected to bridge server
[✓] Bridge active. Session ID: abc123
[*] Listening for commands...
```

### Step 6: Test the Connection

In the dashboard:

1. **Select your session** from the sidebar
2. **Type a command**: `echo "Hello from Termux"`
3. **Click "Send Command"** or press Enter
4. **Watch the output** appear in the terminal

If you see the output, you're connected! 🎉

## 📋 Common Commands to Test

```bash
# Print current directory
pwd

# List files
ls -la

# Check system info
uname -a

# Show current user
whoami

# Create a file
echo "test" > test.txt

# Check available storage
df -h

# Show running processes
ps aux | head -10
```

## 🔧 Advanced Usage

### Multiple Sessions

You can create multiple sessions to control different Termux instances:

1. Create a new session in the dashboard
2. Get the connection token
3. Start a new listener in a different Termux window/device
4. Each session will appear in the sidebar

### Long-Running Commands

The bridge supports long-running commands:

```bash
# Download a file
wget https://example.com/largefile.zip

# Run a script
bash ~/myscript.sh

# Monitor system
watch -n 1 free -h
```

### Piping and Redirection

All shell features work:

```bash
# Pipe commands
ls -la | grep ".txt"

# Redirect output
echo "Hello" > output.txt

# Combine commands
cd ~ && ls -la && pwd
```

## 🐛 Troubleshooting

### Dashboard Won't Load

**Problem**: The dashboard URL shows an error or blank page

**Solution**:
1. Check your internet connection
2. Try refreshing the page (Ctrl+R or Cmd+R)
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try a different browser
5. Check if the server is running: `curl http://localhost:3000/health`

### Listener Won't Connect

**Problem**: The listener shows "Connection refused" or "Cannot connect"

**Solution**:
1. Verify the URL is correct (copy from dashboard)
2. Check the connection token is exactly right (copy-paste, don't type)
3. Verify Termux has internet access: `ping 8.8.8.8`
4. Check if Node.js is installed: `node --version`
5. Verify socket.io-client is installed: `npm list socket.io-client`

### Session Shows "Disconnected"

**Problem**: The listener was running but now shows disconnected

**Solution**:
1. Check if the listener process is still running in Termux
2. Look for error messages in the terminal
3. Restart the listener: Stop it (Ctrl+C) and run it again
4. Check network connectivity

### Commands Not Executing

**Problem**: You send a command but nothing happens

**Solution**:
1. Verify the session status is "connected" (green dot)
2. Check if the listener is still running in Termux
3. Try a simple command first: `echo "test"`
4. Check the browser console (F12) for errors
5. Look at the listener terminal for error messages

### No Output Appearing

**Problem**: Command seems to execute but no output shows

**Solution**:
1. Some commands produce no output (e.g., `cd` directory)
2. Try a command that produces output: `ls -la`
3. Check if the command is hanging (wait 30 seconds)
4. Try a timeout: `timeout 5 sleep 100` (should timeout)
5. Check if stderr is being captured: Try `ls /nonexistent` (should show error)

## 📱 Termux-Specific Tips

### Keep Termux Running

To keep the listener running even when you close the Termux app:

1. Install `termux-services`: `pkg install termux-services`
2. Create a service file
3. Or use `tmux` or `screen` to keep a session open

### Access Termux from SSH

If you have SSH access to your Redmi 13C:

```bash
# On your computer
ssh user@redmi-ip

# In the SSH session, run the listener
node ~/silent_listener.mjs https://... <token>
```

### File Transfer

Transfer files between your computer and Termux:

```bash
# Push file to Termux
scp myfile.txt user@redmi:~/

# Pull file from Termux
scp user@redmi:~/myfile.txt .
```

## 🔐 Security Notes

⚠️ **Current Implementation**:
- No user authentication required
- Connection tokens are simple random strings
- All sessions are visible to anyone with the URL
- Commands execute with Termux user privileges

🔒 **Best Practices**:
- Keep the dashboard URL private
- Don't share connection tokens
- Use strong passwords if you add authentication later
- Monitor what commands are being executed
- Run on a private network if possible

## 📊 Performance

- **Response Time**: ~500ms (polling interval)
- **Command Timeout**: 30 seconds
- **Max Output Size**: Unlimited (streamed)
- **Concurrent Sessions**: Unlimited
- **Concurrent Commands**: One per session (queued)

## 🎯 Use Cases

### Remote Device Management
- Control your Redmi 13C from your computer
- Execute commands without physically touching the device
- Monitor system status in real-time

### Autonomous Execution
- Integrate with Omega Federation for automated tasks
- Schedule commands to run periodically
- Chain multiple commands together

### Development & Testing
- Test scripts on Termux environment
- Debug issues remotely
- Run build processes

### Data Processing
- Download files from cloud
- Process data locally
- Upload results back

## 📚 Additional Resources

- **README.md** - Quick start guide
- **DEPLOYMENT.md** - Deployment details
- **API Documentation** - REST and Socket.IO APIs
- **GitHub** - Source code and issues

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review the error messages in the terminal
3. Check browser console (F12 → Console tab)
4. Verify all prerequisites are installed
5. Try restarting both the dashboard and listener

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Dashboard loads in browser
- [ ] Can create a new session
- [ ] Connection token is displayed
- [ ] Listener script is on Termux
- [ ] Node.js is installed on Termux
- [ ] socket.io-client is installed
- [ ] Listener connects successfully
- [ ] Session shows "connected" status
- [ ] Can send a test command
- [ ] Output appears in dashboard
- [ ] Multiple commands work correctly

---

**Status**: 🟢 READY FOR USE

**Last Updated**: 2026-07-05
**Version**: 1.0
