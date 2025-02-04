import requests
import json

# Siti da cui scaricare i dati
BASE_URLS = [
    "https://huhu.to",
    "https://vavoo.to",
    "https://kool.to",
    "https://oha.to"
]

OUTPUT_FILE = "channels_italy.m3u8"

def fetch_channels(base_url):
    """Scarica i dati JSON da /channels di un sito."""
    try:
        response = requests.get(f"{base_url}/channels", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Errore durante il download da {base_url}: {e}")
        return []

def filter_italian_channels(channels, base_url):
    """Filtra i canali con country Italy e genera il link m3u8 con il nome del canale."""
    return [(ch["name"], f"{base_url}/play/{ch['id']}/index.m3u8") for ch in channels if ch.get("country") == "Italy"]

def main():
    all_links = []
    
    for url in BASE_URLS:
        channels = fetch_channels(url)
        italian_channels = filter_italian_channels(channels, url)
        all_links.extend(italian_channels)
    
    # Ordinare alfabeticamente per nome del canale
    all_links.sort()
    
    # Salvare in un file M3U8
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for name, link in all_links:
            f.write(f"#EXTINF:-1,{name}\n{link}\n")
    
    print(f"File {OUTPUT_FILE} creato con successo!")

if __name__ == "__main__":
    main()
