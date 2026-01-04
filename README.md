# 🕷️ ReconSpider

Szybkie, wielowątkowe narzędzie OSINT do pasywnego i aktywnego rekonesansu subdomen.

## 🚀 Funkcje
- **Pasywny Rekonesans:** Pobiera subdomeny z certyfikatów SSL (crt.sh) bez dotykania celu.
- **Wielowątkowość:** Szybka weryfikacja (Active Recon) statusów HTTP przy użyciu `ThreadPoolExecutor`.
- **Raportowanie:** Generuje wyniki w formacie `.csv` (gotowe do importu do Excela).
- **Smart Filtering:** Odsiewa nieaktywne hosty.

## 🛠️ Instalacja (używając uv)

Projekt wykorzystuje nowoczesny manager pakietów `uv`.

```bash
git clone https://github.com/Monio21/Secon-Spider
cd recon-spider
uv sync
