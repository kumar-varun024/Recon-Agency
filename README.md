# Reconnaissance API (Recon-API)

A high-performance, asynchronous orchestration engine built with FastAPI. This project centralizes industry-standard security tools into a unified REST API, enabling automated, programmatic reconnaissance pipelines for security researchers and penetration testers.

## Core Capabilities

- **Asynchronous Subprocess Management:** Executes resource-intensive CLI tools without blocking the API event loop.
- **Nmap Integration:** Automated network discovery and service enumeration with structured JSON output.
- **FFUF Directory Fuzzer:** High-speed web path discovery with support for custom wordlist injection.
- **Subfinder Subdomain Discovery:** Passive enumeration with automated support for external API providers and trusted DNS resolvers.
- **Automated Recon Pipeline:** A specialized endpoint (`/full-recon`) that chains Subfinder and `httpx-toolkit` to identify live web targets and technology stacks in a single request.
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
git clone https://github.com/YOUR_USERNAME/recon-api.git
cd recon-api
```

### 2. Install Dependencies

```bash
chmod +x setup.sh
./setup.sh
```

This will install all required Python packages listed in `requirements.txt`.

### 3. Configure External API Keys (Optional)

Edit `api/provider-config.yaml` with your API keys for providers like Shodan, Censys, etc. (copy from `provider-config.yaml.example`).

## Quick Start

### Starting the API Server

```bash
launch-agency.sh
```

Wait for the message "Application startup complete" before proceeding.

### Running Reconnaissance Scans

In a new terminal, use the scan launcher:

**Web Reconnaissance (Subfinder → httpx):**
```bash
launch-scan.sh example.com
```

**Network Port Scan (Nmap):**
```bash
launch-scan.sh ports hackerone.com
```

**Full Reconnaissance (All Tools):**
```bash
launch-scan.sh nuke hackerone.com
```

## API Endpoints

- `POST /nmap` - Network reconnaissance with Nmap
- `POST /ffuf` - Web path discovery with FFUF
- `POST /subfinder` - Subdomain enumeration
- `POST /full-recon` - Complete web reconnaissance pipeline
- `GET /health` - API health check

## Project Structure

```
recon-api/
├── api/                    # FastAPI routes and configurations
├── core/                   # Core scanner implementations
├── main.py                 # Entry point
├── setup.sh               # Environment setup script
├── launch-agency.sh       # API server launcher
├── launch-scan.sh         # Scan client launcher
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please ensure all code follows the project's style guidelines.

## License

This project is provided as-is for educational and authorized security testing purposes only.

## Disclaimer

Use this tool responsibly and only on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal.
