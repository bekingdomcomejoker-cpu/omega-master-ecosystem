#!/usr/bin/env node
/**
 * OMEGA BRIDGE - STANDALONE SERVER v1.0
 * Real-time command execution bridge between Manus (cloud) and Termux (local).
 * Uses Socket.IO for bidirectional communication.
 */

import express from 'express';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const VERSION = "1.0";
const RESONANCE = "1.67x";
const PORT = process.env.PORT || 5000;

// In-memory session store (replace with database in production)
const sessions = new Map();
const commands = new Map();
const termuxSessions = new Map();

class OmegaBridge {
  constructor() {
    this.app = express();
    this.server = createServer(this.app);
    this.io = new SocketIOServer(this.server, {
      cors: {
        origin: "*",
        methods: ["GET", "POST"],
      },
    });
    this.setupMiddleware();
    this.setupRoutes();
    this.setupSocketIO();
  }

  setupMiddleware() {
    this.app.use(cors());
    this.app.use(express.json());
    this.app.use(express.static('public'));
  }

  setupRoutes() {
    // Agent Control Center
    this.app.get('/agent', (req, res) => {
      res.sendFile('public/agent-control.html', { root: __dirname });
    });

    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'ok', version: VERSION });
    });

    // Create a new session
    this.app.post('/api/session/create', (req, res) => {
      const { name } = req.body;
      const sessionId = Math.random().toString(36).substring(7);
      const connectionToken = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

      sessions.set(sessionId, {
        id: sessionId,
        name: name || `Session-${new Date().toLocaleString()}`,
        connectionToken: connectionToken,
        status: 'disconnected',
        createdAt: new Date(),
        lastActivity: new Date(),
      });

      res.json({
        sessionId: sessionId,
        connectionToken: connectionToken,
        name: sessions.get(sessionId).name,
      });
    });

    // Get session details
    this.app.get('/api/session/:sessionId', (req, res) => {
      const session = sessions.get(req.params.sessionId);
      if (!session) {
        return res.status(404).json({ error: 'Session not found' });
      }
      res.json(session);
    });

    // Get all sessions
    this.app.get('/api/sessions', (req, res) => {
      res.json(Array.from(sessions.values()));
    });

    // Get commands for a session
    this.app.get('/api/session/:sessionId/commands', (req, res) => {
      const sessionCommands = Array.from(commands.values()).filter(
        (cmd) => cmd.sessionId === req.params.sessionId
      );
      res.json(sessionCommands);
    });
  }

  setupSocketIO() {
    this.io.on('connection', (socket) => {
      console.log(`[Socket.IO] Client connected: ${socket.id}`);

      socket.on('disconnect', () => {
        console.log(`[Socket.IO] Client disconnected: ${socket.id}`);
        // Remove from termux sessions if it was a Termux client
        for (const [key, value] of termuxSessions.entries()) {
          if (value.socketId === socket.id) {
            termuxSessions.delete(key);
            const session = sessions.get(key);
            if (session) {
              session.status = 'disconnected';
              this.io.emit('sessionStatusChanged', { sessionId: key, status: 'disconnected' });
            }
            console.log(`[Socket.IO] Termux session ${key} disconnected`);
            break;
          }
        }
      });

      // Handle Termux listener connection
      socket.on('termuxConnect', (data) => {
        const { connectionToken } = data;
        console.log(`[Socket.IO] Termux device attempting connection with token: ${connectionToken}`);

        // Find session by connection token
        let sessionId = null;
        for (const [id, session] of sessions.entries()) {
          if (session.connectionToken === connectionToken) {
            sessionId = id;
            break;
          }
        }

        if (!sessionId) {
          socket.emit('error', { message: 'Invalid connection token' });
          return;
        }

        // Register this socket as a Termux client for this session
        termuxSessions.set(sessionId, {
          socketId: socket.id,
          sessionId: sessionId,
          connectionToken: connectionToken,
        });

        // Update session status
        const session = sessions.get(sessionId);
        session.status = 'connected';
        session.lastActivity = new Date();

        socket.emit('connected', {
          message: 'Successfully connected to Omega Federation Bridge.',
          sessionId: sessionId,
        });

        // Notify dashboard clients
        this.io.emit('sessionStatusChanged', { sessionId: sessionId, status: 'connected' });
        console.log(`[Socket.IO] Termux session ${sessionId} connected`);
      });

      // Handle output from Termux
      socket.on('termuxOutput', (data) => {
        const { sessionId, commandId, output } = data;
        console.log(`[Socket.IO] Output from Termux session ${sessionId}: ${output.substring(0, 100)}...`);

        const command = commands.get(commandId);
        if (command) {
          command.output = output;
          command.status = 'completed';
          command.completedAt = new Date();
        }

        // Broadcast output to dashboard clients
        this.io.emit('commandOutput', { sessionId, commandId, output });
      });

      // Handle commands from dashboard
      socket.on('dashboardCommand', (data) => {
        const { sessionId, command } = data;
        console.log(`[Socket.IO] Command from dashboard for session ${sessionId}: ${command}`);

        const session = sessions.get(sessionId);
        if (!session) {
          socket.emit('error', { message: 'Session not found' });
          return;
        }

        // Create command
        const commandId = Math.random().toString(36).substring(7);
        commands.set(commandId, {
          id: commandId,
          sessionId: sessionId,
          command: command,
          status: 'pending',
          createdAt: new Date(),
        });

        // Find the Termux socket for this session
        const termuxSession = termuxSessions.get(sessionId);
        if (termuxSession) {
          // Send command to Termux client
          this.io.to(termuxSession.socketId).emit('executeCommand', {
            commandId: commandId,
            command: command,
          });

          // Update command status
          commands.get(commandId).status = 'executing';
          commands.get(commandId).executedAt = new Date();

          // Notify dashboard
          this.io.emit('commandStatusChanged', { sessionId, commandId, status: 'executing' });
        } else {
          // Termux is not connected
          socket.emit('error', { message: 'Termux session is not connected' });
          commands.get(commandId).status = 'failed';
        }
      });
    });
  }

  start() {
    this.server.listen(PORT, () => {
      console.log(`[*] OMEGA BRIDGE - STANDALONE SERVER v${VERSION}`);
      console.log(`[*] Resonance: ${RESONANCE}`);
      console.log(`[✓] Server running on http://localhost:${PORT}`);
      console.log(`[*] WebSocket endpoint: ws://localhost:${PORT}`);
    });
  }
}

// Start the server
const bridge = new OmegaBridge();
bridge.start();
