import requests
import argparse
import concurrent.futures
import random
import re
import csv
import sys
import os

def get_subdomains(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data:
                subdomains.add(entry["name_value"])
            return list(subdomains)
        else:
            return []
    except Exception:
        return []

def check_alive(target):
    if not target.startswith("http://") and not target.startswith("https://"):
        url = f"http://{target}"
    else:
        url = target

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    
    try:
        headers = {"User-Agent": random.choice(user_agents)}
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        
        title_search = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
        if title_search:
            title = title_search.group(1).strip()
        else:
            title = "No Title"        
        
        return [target, response.status_code, title]

    except requests.ConnectionError:
        return [target, "Down", ""]
    except Exception:
        return [target, "Error", ""]

def save_results(results):
    filename = "Subdomain_results.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Target", "Status", "Title"])
        writer.writerows(results)
    print(f"[*] Results saved to file: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Recon Tool v5 - All in One")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", help="Target domain (crt.sh)")
    group.add_argument("-u", "--url", help="Single URL to check")
    group.add_argument("-f", "--file", help="Path to text file with target list")
    
    parser.add_argument("-t", "--threads", help="Number of threads", type=int, default=10)
    args = parser.parse_args()

    results_matrix = []
    targets_list = []

    if args.domain:
        print("[*] Mode: Full Domain Scan (crt.sh)")
        targets_list = get_subdomains(args.domain)
        print(f"[*] Found {len(targets_list)} subdomains from certificate logs.")
        
    elif args.url:
        print("[*] Mode: Single URL Check")
        targets_list = [args.url]

    elif args.file:
        print("[*] Mode: File Input")
        if os.path.exists(args.file):
            with open(args.file, "r") as f:
                targets_list = [line.strip() for line in f if line.strip()]
            print(f"[*] Loaded {len(targets_list)} targets from file: {args.file}")
        else:
            print(f"[!] File not found: {args.file}")
            sys.exit()

    if not targets_list:
        print("[!] No targets found. Exiting.")
        sys.exit()

    print("[*] Starting scan...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for target in targets_list:
            futures.append(executor.submit(check_alive, target))

        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            target = row[0]
            status = row[1]
            title = row[2]

            if status != "Down" and status != "Error":
                print(f"[+] {target} \t- [{status}] - {title[:30]}")
                results_matrix.append(row)

    save_results(results_matrix)
    print("\n[*] Scan completed.")

if __name__ == "__main__":
    main()