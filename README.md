# 🕷️ ReconSpider

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-brightgreen)

**ReconSpider** to lekkie, zorientowane na wydajność narzędzie OSINT służące do mapowania powierzchni ataku (**Attack Surface Mapping**).

Narzędzie automatyzuje proces wstępnego rekonesansu, łącząc pasywne zbieranie danych (CT Logs) z aktywnym fingerprintingiem usług HTTP. Zaprojektowane z myślą o testach penetracyjnych (Red Teaming) oraz programach Bug Bounty.

---

## ⚡ Kluczowe Funkcjonalności

### 🔍 Discovery & Enumeration
* **Passive Recon (`-d`):** Integracja z API `crt.sh` w celu identyfikacji subdomen na podstawie historii certyfikatów SSL/TLS. Zerowy ślad w logach celu.
* **Active Recon (`-f`):** Obsługa zewnętrznych list słownikowych (np. SecLists) umożliwiająca wykrycie zasobów "shadow IT" i domen deweloperskich nieobecnych w publicznych rejestrach.

### 🛡️ Evasion & Fingerprinting
* **WAF Evasion:** Implementacja rotacji `User-Agent` (Randomized Header Injection) w celu omijania prostych reguł blokujących boty.
* **HTTP Fingerprinting:** Automatyczna ekstrakcja nagłówków i tytułów stron (`<title>`), pozwalająca na szybką identyfikację paneli administracyjnych, błędów konfiguracji czy zapomnianych środowisk testowych.

### 🚀 Performance
* **Concurrency:** Wykorzystanie `concurrent.futures.ThreadPoolExecutor` do wielowątkowego przetwarzania żądań, co pozwala na skanowanie setek hostów w sekundy.
* **Smart Parsing:** Inteligentna obsługa błędów połączeń i timeoutów.

---

## 🛠️ Instalacja

Projekt wspiera nowoczesny manager pakietów `uv` dla szybkiej i izolowanej instalacji środowiska.

### Metoda 1: Używając uv (Zalecane)
```bash
git clone https://github.com/Monio21/Recon-Spider
cd Recon-Spider
uv sync

