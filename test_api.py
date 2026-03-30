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
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

API_BASE_URL = "http://127.0.0.1:8000"

def run_nmap(target, mode="fast"):
    print(f"{Colors.BLUE}{Colors.BOLD}[*] Hiring Detective Nmap for target: '{target}'...{Colors.RESET}")
    if mode == "full":
        print(f"{Colors.YELLOW}[-] (Scanning ALL 65,535 ports, this might take a few minutes...){Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}[-] (Scanning top 100 ports, please wait...){Colors.RESET}\n")
    
    try:
        response = requests.get(f"{API_BASE_URL}/scan/nmap/{target}?mode={mode}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"    {Colors.RED}[!] Nmap Error: {data['error']}{Colors.RESET}")
                return
                
            print(f"    {Colors.GREEN}{Colors.BOLD}[+] Port Scan Complete!{Colors.RESET}")
            ports = data.get("discovered_ports", [])
            if not ports:
                print(f"    {Colors.YELLOW}[-] No open ports found.{Colors.RESET}")
                
            for p in ports:
                print(f"        {Colors.CYAN}-> Port {p['port']}/{p['protocol']} | State: {p['state']} | Service: {p['service']}{Colors.RESET}")
            print("") 
        else:
            print(f"    {Colors.RED}[!] Server error: {response.status_code}{Colors.RESET}\n")
    except Exception:
        print(f"    {Colors.RED}[!] Connection error: Ensure 'agency' server is running.{Colors.RESET}\n")

def run_pipeline(target):
    print(f"{Colors.BLUE}{Colors.BOLD}[*] Hiring the Recon Agency for target: '{target}'...{Colors.RESET}")
    print(f"{Colors.YELLOW}[-] Triggering Master Pipeline: Subfinder -> httpx-toolkit...{Colors.RESET}")
    print(f"{Colors.YELLOW}[-] (Please wait 10-20 seconds while the detectives work){Colors.RESET}\n")
    
    live_urls = [] 
    
    try:
        response = requests.get(f"{API_BASE_URL}/pipeline/full-recon/{target}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"    {Colors.RED}[!] Pipeline Error: {data['error']}{Colors.RESET}")
                return live_urls

            print(f"    {Colors.GREEN}{Colors.BOLD}[+] Pipeline Complete!{Colors.RESET}")
            print(f"    {Colors.GREEN}[+] LIVE Websites Confirmed: {data.get('live_websites_found', 0)}{Colors.RESET}\n")
            
            for site in data.get("live_websites", []):
                tech_list = site.get('tech') or ["Unknown/Blocked"]
                url = site.get('url')
                if url:
                    live_urls.append(url)
                print(f"        {Colors.CYAN}-> {url} {Colors.RESET}(Status: {site.get('status_code')}) | Tech: {', '.join(tech_list)}")
            print("") 
            return live_urls 
        else:
             print(f"    {Colors.RED}[!] Server error: {response.status_code}{Colors.RESET}\n")
             return live_urls
    except Exception:
        print(f"    {Colors.RED}[!] Connection error: Ensure 'agency' server is running.{Colors.RESET}\n")
        return live_urls

def run_ffuf(target):
    print(f"{Colors.BLUE}{Colors.BOLD}[*] Hiring Detective FFUF for target: '{target}'...{Colors.RESET}")
    print(f"{Colors.YELLOW}[-] (Brute-forcing directories, this might take a minute...){Colors.RESET}\n")
    
    try:
        response = requests.get(f"{API_BASE_URL}/scan/ffuf/{target}")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                print(f"    {Colors.RED}[!] FFUF Error: {data['error']}{Colors.RESET}")
                return

            print(f"    {Colors.GREEN}{Colors.BOLD}[+] Directory Fuzzing Complete for {target}!{Colors.RESET}")
            directories = data.get("directories", [])
            if not directories:
                print(f"    {Colors.YELLOW}[-] No hidden directories found.{Colors.RESET}")
                
            for d in directories:
                status_color = Colors.GREEN if d.get('status') == 200 else Colors.YELLOW
                print(f"        {Colors.CYAN}-> {d.get('url')} {Colors.RESET}(Status: {status_color}{d.get('status')}{Colors.RESET})")
            print("") 
        else:
             print(f"    {Colors.RED}[!] Server error: {response.status_code}{Colors.RESET}\n")
    except Exception:
        print(f"    {Colors.RED}[!] Connection error: Ensure 'agency' server is running.{Colors.RESET}\n")

def run_nuke(target, mode="fast", do_fuzz=False):
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}[!!!] INITIATING FULL RECONNAISSANCE NUKE ON: '{target}' [!!!]{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[*] PHASE 1: Web Infrastructure Discovery...{Colors.RESET}")
    live_sites = run_pipeline(target)
    
    print(f"{Colors.YELLOW}[*] PHASE 2: Network Port Enumeration...{Colors.RESET}")
    run_nmap(target, mode)
    
    print(f"{Colors.YELLOW}[*] PHASE 3: Active Directory Fuzzing (FFUF)...{Colors.RESET}")
    if not do_fuzz:
        print(f"    {Colors.CYAN}[i] Skipping Phase 3. (Use the -z or --fuzz flag to enable){Colors.RESET}\n")
    elif not live_sites:
         print(f"    {Colors.YELLOW}[-] No live websites found to fuzz. Skipping Phase 3.{Colors.RESET}\n")
    else:
        print(f"    {Colors.BLUE}[*] Launching FFUF against {len(live_sites)} live targets. This may take a while...{Colors.RESET}\n")
        for url in live_sites:
            run_ffuf(url)
    
    print(f"{Colors.MAGENTA}{Colors.BOLD}[+] NUKE OPERATION COMPLETE.{Colors.RESET}\n")

def show_help():
    # Detective ASCII Art
    print(f"{Colors.BLUE}")
    print(r"       ___")
    print(r"   _.-'   '-._")
    print(r"  |___________|")
    print(r"   \  o   o  /")
    print(r"    \  .-.  /")
    print(r"     \_____/")
    print(f"{Colors.RESET}", end="")

    print(f"{Colors.MAGENTA}{Colors.BOLD}=== RECON AGENCY ORCHESTRATOR (Recon-API) ==={Colors.RESET}")
    print(f"{Colors.CYAN}Advanced Asynchronous Bug Bounty Automation Framework{Colors.RESET}\n")
    
    print(f"{Colors.BLUE}{Colors.BOLD}USAGE:{Colors.RESET}")
    print(f"    agency-scan [command] <target> [flags]\n")
    
    print(f"{Colors.BLUE}{Colors.BOLD}COMMANDS:{Colors.RESET}")
    print(f"    {Colors.GREEN}[blank]{Colors.RESET}        Run Phase 1 Web Recon (Subfinder -> httpx) on a domain")
    print(f"    {Colors.GREEN}ports{Colors.RESET}          Run Phase 2 Network Port Scan (Nmap) on a domain")
    print(f"    {Colors.GREEN}fuzz{Colors.RESET}           Run Phase 3 Active Directory Brute-Forcing (FFUF)")
    print(f"    {Colors.GREEN}nuke{Colors.RESET}           Run the entire pipeline automatically\n")
    
    print(f"{Colors.BLUE}{Colors.BOLD}FLAGS:{Colors.RESET}")
    print(f"    {Colors.YELLOW}-f, --full{Colors.RESET}     Force Nmap to scan all 65,535 ports (Default: Top 100)")
    print(f"    {Colors.YELLOW}-z, --fuzz{Colors.RESET}     Enable Phase 3 (FFUF) during 'nuke' command (Default: Disabled)")
    print(f"    {Colors.YELLOW}-h, --help{Colors.RESET}     Show this help menu\n")
    
    print(f"{Colors.BLUE}{Colors.BOLD}EXAMPLES:{Colors.RESET}")
    print(f"    agency-scan example.com                  {Colors.YELLOW}# Fast web recon{Colors.RESET}")
    print(f"    agency-scan fuzz example.com             {Colors.YELLOW}# Hunt for hidden paths{Colors.RESET}")
    print(f"    agency-scan ports example.com -f         {Colors.YELLOW}# Full 65k port scan{Colors.RESET}")
    print(f"    agency-scan nuke example.com -f -z       {Colors.YELLOW}# Maximum aggression (All tools + Full Ports + Fuzzing){Colors.RESET}\n")
if __name__ == "__main__":
    args = sys.argv[1:]
    
    # Immediately catch the help flag before doing anything else
    if len(args) == 0 or "-h" in args or "--help" in args:
        show_help()
        sys.exit(0)
    
    # Professional CLI Flag Parsing
    mode = "fast"
    if "-f" in args:
        mode = "full"
        args.remove("-f")
    elif "--full" in args:
        mode = "full"
        args.remove("--full")
        
    do_fuzz = False
    if "-z" in args:
        do_fuzz = True
        args.remove("-z")
    elif "--fuzz" in args:
        do_fuzz = True
        args.remove("--fuzz")

    # Command Routing
    if len(args) == 2 and args[0] == "ports":
        run_nmap(args[1], mode)
    elif len(args) == 2 and args[0] == "fuzz":
        run_ffuf(args[1])
    elif len(args) == 2 and args[0] == "nuke":
        run_nuke(args[1], mode, do_fuzz)
    elif len(args) == 1 and args[0] not in ["ports", "fuzz", "nuke"]:
        run_pipeline(args[0])
    else:
        print(f"{Colors.RED}[!] Invalid syntax. Run 'agency-scan --help' for usage.{Colors.RESET}")