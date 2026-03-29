#!/usr/bin/env python3
import requests
import sys

API_BASE_URL = "http://127.0.0.1:8000"

def run_nmap(target):
    print(f"[*] Hiring Detective Nmap for target: '{target}'...\n")
    print("[-] (Scanning top 100 ports, please wait...)\n")
    
    try:
        response = requests.get(f"{API_BASE_URL}/scan/nmap/{target}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"    [!] Nmap Error: {data['error']}")
                return
                
            print("    [+] Port Scan Complete!\n")
            ports = data.get("discovered_ports", [])
            if not ports:
                print("    [-] No open ports found in fast scan.")
                
            for p in ports:
                print(f"        -> Port {p['port']}/{p['protocol']} | State: {p['state']} | Service: {p['service']}")
        else:
            print(f"    [!] Server error: {response.status_code}")
    except Exception:
        print("    [!] Connection error: Ensure 'agency' server is running.")

def run_pipeline(target):
    print(f"[*] Hiring the Recon Agency for target: '{target}'...\n")
    print("[-] Triggering Master Pipeline: Subfinder -> httpx-toolkit...")
    print("[-] (Please wait 10-20 seconds while the detectives work)\n")
    
    try:
        response = requests.get(f"{API_BASE_URL}/pipeline/full-recon/{target}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"    [!] Pipeline Error: {data['error']}")
                return

            print(f"    [+] Pipeline Complete!")
            print(f"    [+] LIVE Websites Confirmed: {data.get('live_websites_found', 0)}\n")
            
            for site in data.get("live_websites", []):
                # We add a fallback just in case the WAF blocks the tech detection
                tech_list = site.get('tech') or ["Unknown/Blocked"]
                print(f"        -> {site.get('url')} (Status: {site.get('status_code')}) | Tech: {', '.join(tech_list)}")
        else:
             print(f"    [!] Server error: {response.status_code}")
    except Exception:
        print("    [!] Connection error: Ensure 'agency' server is running.")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "ports":
        run_nmap(sys.argv[2])
    elif len(sys.argv) == 2:
        run_pipeline(sys.argv[1])
    else:
        print("[!] Invalid Command.")
        print("    Usage for Web Scan:  agency-scan <domain>")
        print("    Usage for Port Scan: agency-scan ports <domain>")
