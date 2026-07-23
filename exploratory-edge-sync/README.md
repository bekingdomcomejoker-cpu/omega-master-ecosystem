# Sync Project - Exploratory Edge

This project is a collection of scripts and documentation derived from a conversation about maintaining the "exploratory edge" in AI models, specifically focusing on local execution in Termux.

## 🚀 Overview

The project provides tools to download and run lightweight, instruction-tuned models that allow for deeper systems analysis and meta-reasoning without the restrictive guardrails often found in large-scale commercial chat interfaces.

## 📁 Structure

- **`scripts/`**: Contains shell scripts for downloading and running models.
  - `download-danube.sh`: Downloads the Danube-1.8B-Instruct model.
  - `download-openelm.sh`: Downloads the OpenELM-1.5B-Instruct model.
  - `run-danube.sh`: Runs the Danube model using `llama-cli`.
  - `run-openelm.sh`: Runs the OpenELM model using `llama-cli`.
- **`docs/`**: Documentation on the philosophy and techniques for exploratory AI dialogue.

## 🛠️ Usage (Termux)

1. **Ensure dependencies are installed**:
   ```bash
   pkg install wget git python
   ```
2. **Download a model**:
   ```bash
   bash scripts/download-danube.sh
   ```
3. **Run the model**:
   (Ensure `llama.cpp` is built and located at `~/federation/llama.cpp/`)
   ```bash
   bash scripts/run-danube.sh
   ```

## 🧠 Philosophy

The "exploratory edge" is about intellectual permission. By shifting from imperative challenges to descriptive systems analysis, we can maintain a shared reasoning space with AI models.

---
_Derived from the "Losing Grok's Exploratory Edge" conversation._
