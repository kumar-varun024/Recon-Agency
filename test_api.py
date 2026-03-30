#!/usr/bin/env python3
import requests
import sys

# ANSI Color Codes for Terminal Magic
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m' # Special color for the Nuke banner
    RESET = '\033[0m'
    BOLD = '\033[1m'

API_BASE_URL = "http://127.0.0.1:8000"

def run_nmap(target):
    print(f"{Colors.BLUE}{Colors.BOLD}[*] Hiring Detective Nmap for target: '{target}'...{Colors.RESET}")
    print(f"{Colors.YELLOW}[-] (Scanning top 100 ports, please wait...){Colors.RESET}\n")
    
    try:
        response = requests.get(f"{API_BASE_URL}/scan/nmap/{target}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"    {Colors.RED}[!] Nmap Error: {data['error']}{Colors.RESET}")
                return
                
            print(f"    {Colors.GREEN}{Colors.BOLD}[+] Port Scan Complete!{Colors.RESET}")
            ports = data.get("discovered_ports", [])
            if not ports:
                print(f"    {Colors.YELLOW}[-] No open ports found in fast scan.{Colors.RESET}")
                
            for p in ports:
                print(f"        {Colors.CYAN}-> Port {p['port']}/{p['protocol']} | State: {p['state']} | Service: {p['service']}{Colors.RESET}")
            print("") # Empty line for spacing
        else:
            print(f"    {Colors.RED}[!] Server error: {response.status_code}{Colors.RESET}\n")
    except Exception:
        print(f"    {Colors.RED}[!] Connection error: Ensure 'agency' server is running.{Colors.RESET}\n")

def run_pipeline(target):
    print(f"{Colors.BLUE}{Colors.BOLD}[*] Hiring the Recon Agency for target: '{target}'...{Colors.RESET}")
    print(f"{Colors.YELLOW}[-] Triggering Master Pipeline: Subfinder -> httpx-toolkit...{Colors.RESET}")
    print(f"{Colors.YELLOW}[-] (Please wait 10-20 seconds while the detectives work){Colors.RESET}\n")
    
    try:
        response = requests.get(f"{API_BASE_URL}/pipeline/full-recon/{target}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"    {Colors.RED}[!] Pipeline Error: {data['error']}{Colors.RESET}")
                return

            print(f"    {Colors.GREEN}{Colors.BOLD}[+] Pipeline Complete!{Colors.RESET}")
            print(f"    {Colors.GREEN}[+] LIVE Websites Confirmed: {data.get('live_websites_found', 0)}{Colors.RESET}\n")
            
            for site in data.get("live_websites", []):
                tech_list = site.get('tech') or ["Unknown/Blocked"]
                print(f"        {Colors.CYAN}-> {site.get('url')} {Colors.RESET}(Status: {site.get('status_code')}) | Tech: {', '.join(tech_list)}")
            print("") # Empty line for spacing
        else:
             print(f"    {Colors.RED}[!] Server error: {response.status_code}{Colors.RESET}\n")
    except Exception:
        print(f"    {Colors.RED}[!] Connection error: Ensure 'agency' server is running.{Colors.RESET}\n")

def run_nuke(target):
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}[!!!] INITIATING FULL RECONNAISSANCE NUKE ON: '{target}' [!!!]{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[*] PHASE 1: Web Infrastructure Discovery...{Colors.RESET}")
    run_pipeline(target)
    
    print(f"{Colors.YELLOW}[*] PHASE 2: Network Port Enumeration...{Colors.RESET}")
    run_nmap(target)
    
    print(f"{Colors.MAGENTA}{Colors.BOLD}[+] NUKE OPERATION COMPLETE.{Colors.RESET}\n")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "ports":
        run_nmap(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "nuke":
        run_nuke(sys.argv[2])
    elif len(sys.argv) == 2:
        run_pipeline(sys.argv[1])
    else:
        print(f"{Colors.RED}[!] Invalid Command.{Colors.RESET}")
        print(f"    {Colors.CYAN}Web Scan:   agency-scan <domain>{Colors.RESET}")
        print(f"    {Colors.CYAN}Port Scan:  agency-scan ports <domain>{Colors.RESET}")
        print(f"    {Colors.CYAN}Full Nuke:  agency-scan nuke <domain>{Colors.RESET}")
