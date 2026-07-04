# Project Overview

This repository contains a minimal Android BLE testing app and a GitHub Actions workflow that builds a debug APK on push and pull request.

## Core features
- Connects to a target BLE device by MAC address
- Discovers GATT services
- Enables notifications on target characteristics
- Sends a scripted sequence of writes
- Logs output to the UI and a local file

## Implementation notes
- Kotlin-based Android app
- BLE permissions for modern Android versions
- Single-activity architecture
- Simple build pipeline with Gradle and GitHub Actions
