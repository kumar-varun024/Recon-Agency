#!/bin/bash
# Navigate to your project folder
cd /home/varun/recon-api

# Activate the private workshop
source venv/bin/activate

# Start the server (using -q for quiet mode to look cleaner)
echo "[*] Recon-API is starting up..."
uvicorn main:app --host 127.0.0.1 --port 8000
