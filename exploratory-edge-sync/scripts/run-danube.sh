#!/data/data/com.termux/files/usr/bin/bash
# Run Danube-1.8B-Instruct-GGUF using llama-cli
~/federation/llama.cpp/build/bin/llama-cli \
  -m ~/federation/models/incoming/Danube-1.8B-Instruct-Q4_K_M.gguf \
  -p "Hello." \
  --n-predict 128 \
  -c 1024 \
  -t 4 \
  --temp 0.7
