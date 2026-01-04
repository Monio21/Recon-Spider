import requests
import argparse
import concurrent.futures

#test
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


def check_alive(subdomain):
    url = f"http://{subdomain}"
    try:
        response = requests.get(url, timeout=3, allow_redirects=True)
        return [subdomain, response.status_code]

    except requests.ConnectionError:
        return [subdomain, "Down"]

    except Exception:
        return [subdomain, "Error"]


def save_results(results):
    filename = "Subdomen_results.csv"
    with open(filename, "w") as f:
        f.write("Subdomena,Status\n")

        for row in results:
            f.write(f"{row[0]},{row[1]}\n")

    print(f"[*] Wyniki zapisane w pliku: {filename}")


def main():
    parser = argparse.ArgumentParser(description="Recon Tool v2 - Matrix Output")
    parser.add_argument("-d", "--domain", help="Domena do sprawdzenia", required=True)
    parser.add_argument("-t", "--threads", help="Liczba wątków", type=int, default=10)
    args = parser.parse_args()

    target_domain = args.domain
    threads = args.threads

    results_matrix = []

    subs = get_subdomains(target_domain)
    print(f"[*] Cel: {target_domain}")
    print(f"[*] Znaleziono {len(subs)} subdomen. Skanowanie...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []

        for sub in subs:
            futures.append(executor.submit(check_alive, sub))

        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            sub = row[0]
            status = row[1]

            if status != "Down" and status != "Error":
                print(f"[+] {sub} \t- Status: {status}")
                results_matrix.append(row)

    save_results(results_matrix)

    print("\n[*] Skanowanie zakończone.")


if __name__ == "__main__":
    main()
