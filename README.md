# Reconnaissance API (Recon-API)

A high-performance, asynchronous orchestration engine built with FastAPI. This project centralizes industry-standard security tools into a unified REST API, enabling automated, programmatic reconnaissance pipelines for security researchers and penetration testers.

## Core Capabilities

- **Asynchronous Subprocess Management:** Executes resource-intensive CLI tools without blocking the API event loop.
- **Nmap Integration:** Automated network discovery and service enumeration with structured JSON output.
- **FFUF Directory Fuzzer:** High-speed web path discovery with support for custom wordlist injection.
- **Subfinder Subdomain Discovery:** Passive enumeration with automated support for external API providers and trusted DNS resolvers.
- **Automated Recon Pipeline:** A specialized endpoint (`/pipeline/full-recon/{target}`) that chains Subfinder and `httpx-toolkit` to identify live web targets and technology stacks in a single request.
- **Deployment Automation:** Integrated `setup.sh` for standardized environment configuration.

## System Requirements

This framework requires the following tools to be present in the system's PATH:
- Python 3.10+
- Nmap
- FFUF
- Subfinder
- httpx-toolkit (ProjectDiscovery version)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kumar-varun024/recon-api.git
cd recon-api
```

### 2. Install Dependencies

```bash
chmod +x setup.sh
./setup.sh
```

This will install all required Python packages listed in `requirements.txt`.

### 3. Configure Global Commands (Required)

To run this tool from anywhere on your system like a native Linux binary, you must link the launchers to your global binaries folder. Run these commands from inside the recon-api folder:

```bash
sudo ln -sf $(pwd)/launch-agency.sh /usr/local/bin/agency
sudo ln -sf $(pwd)/launch-scan.sh /usr/local/bin/agency-scan
```

## Quick Start (Two-Terminal Workflow)

This tool utilizes a highly efficient client-server architecture. To run a scan, you need two terminal windows open simultaneously.

### Step 1: Start the API Server

Open your terminal and type the global command to wake up the server:

```bash
agency
```

Note: Wait for the "Application startup complete" message. Leave this terminal running in the background.

### Step 2: Run Reconnaissance Scans

Open a new terminal tab and use the global scanner command:

**Web Reconnaissance (Subfinder → httpx):**

```bash
agency-scan example.com
```

**Network Port Scan (Nmap):**

```bash
agency-scan ports example.com
```

**Full Reconnaissance Pipeline (All Tools):**

```bash
agency-scan nuke hackerone.com
```

## API Endpoints

The API utilizes GET requests for simplified browser and client testing.

- `GET /scan/nmap/{target}` - Network reconnaissance with Nmap
- `GET /scan/ffuf/{target}` - Web path discovery with FFUF
- `GET /scan/subfinder/{target}` - Subdomain enumeration
- `GET /pipeline/full-recon/{target}` - Complete web reconnaissance pipeline (Subfinder → httpx)

## Project Structure

```
recon-api/
├── api/                    # FastAPI routes and configurations
├── core/                   # Core scanner implementations
├── main.py                 # Entry point
├── setup.sh                # Environment setup script
├── launch-agency.sh        # API server launcher
├── launch-scan.sh          # Scan client launcher
├── test_api.py             # Client execution logic
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Advanced Configuration

### API Provider Integration

To enhance subdomain discovery, configure your API keys (e.g., Shodan, GitHub, Chaos):

1. Rename `provider-config.yaml.example` to `provider-config.yaml`.
2. Populate the file with valid API credentials.

The API will automatically detect and apply these credentials during scans.

### Trusted Resolvers

To mitigate rate-limiting and improve DNS accuracy, place a trusted resolver list in the root directory.

```bash
wget https://raw.githubusercontent.com/trickest/resolvers/main/resolvers-trusted.txt
```

## Contributing

Contributions are welcome! Please ensure all code follows the project's style guidelines.

## License

This project is provided as-is for educational and authorized security testing purposes only.

## Disclaimer

Use this tool responsibly and only on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal.
