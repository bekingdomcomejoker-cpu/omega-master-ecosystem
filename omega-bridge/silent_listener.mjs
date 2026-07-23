#!/usr/bin/env node
/**
 * OMEGA BRIDGE - SILENT LISTENER (Socket.IO) v2.0
 * Lightweight Termux listener using Socket.IO for real-time command execution.
 * No Selenium, no browser driver required.
 */

import { io } from 'socket.io-client';
import { spawn } from 'child_process';

const VERSION = "2.0";
const RESONANCE = "1.67x";

class SilentListenerSocketIO {
  constructor(bridgeUrl, connectionToken) {
    this.bridgeUrl = bridgeUrl;
    this.connectionToken = connectionToken;
    this.socket = null;
    this.sessionId = null;
  }

  log(message, level = "*") {
    const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
    console.log(`[${level}] ${timestamp} | ${message}`);
  }

  connect() {
    this.log(`OMEGA BRIDGE - SILENT LISTENER (Socket.IO) v${VERSION}`, "*");
    this.log(`Target URL: ${this.bridgeUrl}`, "*");
    this.log(`Resonance: ${RESONANCE}`, "*");

    try {
      this.socket = io(this.bridgeUrl, {
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: Infinity,
      });

      this.socket.on("connect", () => {
        this.log("Connected to bridge server", "✓");
        this.authenticate();
      });

      this.socket.on("disconnect", () => {
        this.log("Disconnected from bridge server", "✗");
      });

      this.socket.on("error", (error) => {
        this.log(`Socket error: ${error}`, "✗");
      });

      this.socket.on("connected", (data) => {
        this.sessionId = data.sessionId;
        this.log(`Bridge active. Session ID: ${this.sessionId}`, "✓");
        this.log("Listening for commands...", "*");
      });

      this.socket.on("executeCommand", (data) => {
        this.handleCommand(data);
      });
    } catch (error) {
      this.log(`Failed to connect: ${error.message}`, "✗");
      process.exit(1);
    }
  }

  authenticate() {
    this.log("Authenticating with connection token...", "*");
    this.socket.emit("termuxConnect", {
      connectionToken: this.connectionToken,
    });
  }

  handleCommand(data) {
    const { commandId, command } = data;
    this.log(`Executing command ${commandId}: ${command}`, "→");

    this.executeCommand(command)
      .then((output) => {
        this.log(`Command ${commandId} completed`, "✓");
        this.socket.emit("termuxOutput", {
          sessionId: this.sessionId,
          commandId: commandId,
          output: output,
        });
      })
      .catch((error) => {
        this.log(`Command ${commandId} failed: ${error.message}`, "✗");
        this.socket.emit("termuxOutput", {
          sessionId: this.sessionId,
          commandId: commandId,
          output: `[ERROR] ${error.message}`,
        });
      });
  }

  executeCommand(command) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        proc.kill();
        reject(new Error("Command timed out after 30 seconds"));
      }, 30000);

      let stdout = "";
      let stderr = "";

      const proc = spawn("sh", ["-c", command], {
        cwd: process.env.HOME || "/data/data/com.termux/files/home",
      });

      proc.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      proc.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      proc.on("close", (code) => {
        clearTimeout(timeout);
        const output = stdout + (stderr ? `\n[STDERR]\n${stderr}` : "");
        if (code !== 0) {
          resolve(`[EXIT CODE ${code}]\n${output}`);
        } else {
          resolve(output || "[No output]");
        }
      });

      proc.on("error", (error) => {
        clearTimeout(timeout);
        reject(error);
      });
    });
  }

  run() {
    this.connect();

    // Keep the process alive
    process.on("SIGINT", () => {
      this.log("Listener stopped by user", "*");
      if (this.socket) {
        this.socket.disconnect();
      }
      process.exit(0);
    });
  }
}

// Main entry point
function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log(`Usage: node ${process.argv[1]} <bridge_url> <connection_token>`);
    console.log(`Example: node ${process.argv[1]} http://localhost:5000 abc123def456`);
    process.exit(1);
  }

  const bridgeUrl = args[0];
  const connectionToken = args[1];

  const listener = new SilentListenerSocketIO(bridgeUrl, connectionToken);
  listener.run();
}

main();
