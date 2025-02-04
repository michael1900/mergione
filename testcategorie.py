import requests
import json
import os

# Siti da cui scaricare i dati
BASE_URLS = [
    "https://huhu.to",
    "https://vavoo.to",
    "https://kool.to",
    "https://oha.to"
]

OUTPUT_FILE = "channels_italy.m3u8"

# Mappatura categorie
CATEGORIES = {
    "Cinema": ["film", "movie", "cinema", "serie"],
    "Sport": ["sport", "calcio", "football", "basket", "tennis", "dazn"],
    "Intrattenimento": ["show", "reality", "music", "game", "y uno", "dmax", "italia1"],
    "Informazione": ["news", "tg", "report", "documentary", "natur", "history"]
}

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
    return [(ch["name"], f"{base_url}/play/{ch['id']}/index.m3u8", base_url) for ch in channels if ch.get("country") == "Italy"]

def assign_category(channel_name):
    """Assegna una categoria basata sul nome del canale."""
    for category, keywords in CATEGORIES.items():
        if any(keyword.lower() in channel_name.lower() for keyword in keywords):
            return category
    return "Varie"

def main():
    # Rimuovere il file esistente prima di ogni esecuzione
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

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
        for name, link, site in all_links:
            site_name = site.replace("https://", "").replace(".to", "").upper()
            category = assign_category(name)
            f.write(f"#EXTINF:-1 tvg-id=\"\" tvg-name=\"{name}\" tvg-logo=\"\" group-title=\"{category}\", {name}\n")
            f.write(f"#EXTVLCOPT:http-user-agent={site_name}/1.0\n")
            f.write(f"#EXTVLCOPT:http-referrer={site}\n")
            f.write(f"#EXTHTTP:{{\"User-Agent\":\"{site_name}/1.0\",\"Referer\":\"{site}\"}}\n")
            f.write(f"{link}\n")
    print(f"File {OUTPUT_FILE} creato con successo!")

if __name__ == "__main__":
    main()
