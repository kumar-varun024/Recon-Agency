import os
import asyncio
import json
from urllib.parse import urlparse

def clean_target(user_input: str) -> str:
    """Extracts just the clean domain or IP from any messy URL."""
    user_input = user_input.strip()
    if user_input.startswith("http://") or user_input.startswith("https://"):
        return urlparse(user_input).hostname
    return user_input.split('/')[0]

def parse_nmap_output(raw_text: str):
    """Translates messy terminal text into a clean Python dictionary."""
    ports = []
    lines = raw_text.split('\n')
    for line in lines:
        if '/tcp' in line or '/udp' in line:
            parts = line.split()
            if len(parts) >= 3:
                ports.append({
                    "port": parts[0].split('/')[0],
                    "protocol": parts[0].split('/')[1],
                    "state": parts[1],
                    "service": parts[2]
                })
    return ports

async def run_nmap_scan(target: str):
    """Hunts for open ports using Nmap."""
    safe_target = clean_target(target)
    if not safe_target:
        return {"error": "Invalid target provided."}
    
    command = ["nmap", "-F", safe_target]
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        return {"error": "Nmap failed", "details": stderr.decode()}
        
    raw_text = stdout.decode()
    return {
        "target": safe_target,
        "status": "success",
        "discovered_ports": parse_nmap_output(raw_text)
    }

async def run_ffuf_scan(target: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt"):
    """Hunts for hidden directories using FFUF and an optional custom wordlist."""
    safe_target = clean_target(target)
    if not safe_target:
        return {"error": "Invalid target provided."}
        
    # SAFETY CHECK: Does the wordlist actually exist on their computer?
    if not os.path.exists(wordlist):
        return {"error": f"Wordlist not found at: {wordlist}"}
        
    target_url = f"http://{safe_target}/FUZZ"
    
    command = ["ffuf", "-w", wordlist, "-u", target_url, "-t", "50", "-json"]
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0 and not stdout:
        return {"error": "FFUF failed", "details": stderr.decode()}
        
    try:
        raw_data = json.loads(stdout.decode())
        hits = [{"directory": r["input"]["FUZZ"], "url": r["url"], "status": r["status"]} 
                for r in raw_data.get("results", [])]
        return {"target": safe_target, "status": "success", "hidden_directories": hits}
    except json.JSONDecodeError:
        return {"error": "Could not read FFUF data."}

async def run_subfinder_scan(target: str):
    """Hunts for subdomains using Subfinder (with optional API keys and resolvers)."""
    safe_target = clean_target(target)
    if not safe_target:
        return {"error": "Invalid target provided."}
        
    command = ["subfinder", "-d", safe_target, "-silent", "-json"]
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Check for the optional API keys file
    config_path = os.path.join(BASE_DIR, "provider-config.yaml")
    if os.path.exists(config_path):
        command.extend(["-pc", config_path])
        
    # 2. Check for the optional Resolvers file
    resolvers_path = os.path.join(BASE_DIR, "resolvers-trusted.txt")
    if os.path.exists(resolvers_path):
        command.extend(["-rL", resolvers_path])
        
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0 and not stdout:
        return {"error": "Subfinder failed", "details": stderr.decode()}
        
    try:
        raw_lines = stdout.decode().strip().split('\n')
        subdomains = []
        for line in raw_lines:
            if line: 
                data = json.loads(line)
                subdomains.append({"host": data.get("host"), "source": data.get("source")})
                
        return {
            "target": safe_target, 
            "status": "success", 
            "api_keys_used": os.path.exists(config_path),
            "resolvers_used": os.path.exists(resolvers_path),
            "total_found": len(subdomains), 
            "subdomains": subdomains
        }
    except json.JSONDecodeError:
        return {"error": "Could not read Subfinder data."}

async def run_recon_pipeline(target: str):
    """Pipeline: Subfinder -> httpx-toolkit"""
    safe_target = clean_target(target)
    if not safe_target:
        return {"error": "Invalid target provided."}
        
    # 1. Run Subfinder first
    subfinder_results = await run_subfinder_scan(safe_target)
    
    if "error" in subfinder_results:
        return subfinder_results
        
    # Extract just the raw hostnames into a list
    subdomains = [item["host"] for item in subfinder_results.get("subdomains", [])]
    
    if not subdomains:
        return {"target": safe_target, "message": "No subdomains found to probe."}
        
    # 2. Prepare the data for httpx
    input_data = "\n".join(subdomains).encode()
    
    command = ["httpx-toolkit", "-silent", "-title", "-tech-detect", "-status-code", "-json"]
    
    process = await asyncio.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate(input=input_data)
    
    if process.returncode != 0 and not stdout:
        return {"error": "httpx-toolkit failed", "details": stderr.decode()}
        
    try:
        raw_lines = stdout.decode().strip().split('\n')
        
        alive_hosts = []
        for line in raw_lines:
            if line:
                data = json.loads(line)
                alive_hosts.append({
                    "url": data.get("url"),
                    "status_code": data.get("status_code"),
                    "title": data.get("title", "No Title"),
                    "tech": data.get("tech", [])
                })
                
        return {
            "target": safe_target,
            "pipeline": "Subfinder -> httpx",
            "total_subdomains_found": len(subdomains),
            "live_websites_found": len(alive_hosts),
            "live_websites": alive_hosts
        }
        
    except json.JSONDecodeError:
        return {"error": "Could not read httpx data."}