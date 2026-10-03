#!/usr/bin/env python3
import subprocess
import json
import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def run_semgrep():
    print(Fore.CYAN + "[*] Running SAST (Semgrep) with custom rules...")
    cmd = [
        "semgrep", "scan",
        "--config=rules/semgrep/fastapi-hardcoded-secret.yaml",
        "--json",
        "app/"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and result.stdout == "":
            print(Fore.RED + "[-] Semgrep execution failed. Is it installed?")
            return False

        output = json.loads(result.stdout)
        results = output.get("results", [])
        
        if results:
            print(Fore.RED + f"[!] Semgrep found {len(results)} vulnerabilities:")
            for r in results:
                print(Fore.YELLOW + f"    - {r['check_id']} at {r['path']}:{r['start']['line']}")
                print(f"      {r['extra']['message']}")
        else:
            print(Fore.GREEN + "[+] Semgrep found no vulnerabilities.")
            
    except Exception as e:
        print(Fore.RED + f"[-] Error running Semgrep: {e}")
        return False
    return True

def run_nuclei(target_url):
    print(Fore.CYAN + f"\n[*] Running DAST (Nuclei) against {target_url}...")
    cmd = [
        "nuclei",
        "-t", "rules/nuclei/api-bola-test.yaml",
        "-u", target_url,
        "-json-export", "nuclei_output.json"
    ]
    try:
        # We don't necessarily want to capture output if nuclei prints its own fancy progress
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if not os.path.exists("nuclei_output.json"):
            print(Fore.GREEN + "[+] Nuclei found no vulnerabilities.")
            return True
            
        with open("nuclei_output.json", "r") as f:
            lines = f.readlines()
            if lines:
                print(Fore.RED + f"[!] Nuclei found {len(lines)} vulnerabilities:")
                for line in lines:
                    finding = json.loads(line)
                    print(Fore.YELLOW + f"    - {finding.get('info', {}).get('name')} [{finding.get('info', {}).get('severity')}]")
                    print(f"      Host: {finding.get('host')}")
            else:
                 print(Fore.GREEN + "[+] Nuclei found no vulnerabilities.")
                 
        # cleanup
        os.remove("nuclei_output.json")
    except Exception as e:
        print(Fore.RED + f"[-] Error running Nuclei: {e}")
        return False
    return True

if __name__ == "__main__":
    print(Fore.BLUE + Style.BRIGHT + "=== Moneyview Security Automation Scanner ===")
    
    # 1. Run SAST
    run_semgrep()
    
    # 2. Run DAST (Assuming the app is running on localhost:8000)
    target = os.getenv("TARGET_URL", "http://127.0.0.1:8000")
    print(Fore.CYAN + f"\n[*] NOTE: For DAST to work, ensure the API is running at {target}")
    run_nuclei(target)
    
    print(Fore.BLUE + Style.BRIGHT + "\n=== Scan Complete ===")
