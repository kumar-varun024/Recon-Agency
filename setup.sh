#!/bin/bash

echo "[*] Welcome to the Recon API Setup!"
echo "-----------------------------------"

# 1. Create the virtual environment
echo "[-] 1. Creating an isolated virtual environment (venv)..."
python3 -m venv venv

# 2. Activate it and install the requirements file you just made
echo "[-] 2. Activating venv and installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# 3. Give the test script permission to run
echo "[-] 3. Making the client script executable..."
chmod +x test_api.py

echo "-----------------------------------"
echo "[+] Setup Complete! Your agency is ready."
echo ""
echo "To start the server, run:"
echo "    source venv/bin/activate"
echo "    uvicorn main:app --reload"
echo ""
echo "In a second terminal, run the test client:"
echo "    ./test_api.py"
