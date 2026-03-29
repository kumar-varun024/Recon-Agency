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

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/recon-api.git](https://github.com/YOUR_USERNAME/recon-api.git)
   cd recon-api
# Recon-Agency
# Recon-Agency
