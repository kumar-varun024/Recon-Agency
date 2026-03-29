#!/usr/bin/env python3
import requests
import json
import sys

API_BASE_URL = "http://127.0.0.1:8000"

def test_my_agency(target):
    print(f"[*] Hiring the Recon Agency for target: '{target}'...\n")
    print("[-] Triggering Master Pipeline: Subfinder -> httpx-toolkit...")
    print("[-] (Please wait 10-20 seconds while the detectives work)\n")
    
    try:
        pipeline_response = requests.get(f"{API_BASE_URL}/pipeline/full-recon/{target}")
        
        if pipeline_response.status_code == 200:
            data = pipeline_response.json()
            if "error" in data:
                print(f"    [!] Pipeline Error: {data['error']}")
                return

            print(f"    [+] Pipeline Complete!")
            print(f"    [+] LIVE Websites Confirmed: {data.get('live_websites_found', 0)}\n")
            
            for site in data.get("live_websites", []):
                print(f"        -> {site.get('url')} (Status: {site.get('status_code')}) | Tech: {', '.join(site.get('tech', []))}")
        else:
             print(f"    [!] Server error: {pipeline_response.status_code}")
             
    except Exception as e:
        print(f"    [!] Connection error: Ensure 'agency' server is running.")

if __name__ == "__main__":
    # Check if a domain was provided: agency-scan <domain>
    if len(sys.argv) > 1:
        user_target = sys.argv[1]
        test_my_agency(user_target)
    else:
        print("[!] Usage: agency-scan <domain>")
        print("    Example: agency-scan hackerone.com")