import requests
import os

def fetch_all_stations(limit_per_query=50000):
    """
    Busca todas as estações do Radio Browser API em lotes (limitados por request).
    """
    url = "https://de1.api.radio-browser.info/json/stations"
    params = {"limit": limit_per_query, "hidebroken": True}
    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao buscar estações: {e}")
        return []

def save_as_m3u(stations, output_file="stations/all_stations.m3u"):
    """
    Salva a lista de estações no formato .m3u com descrição incluindo nome, país e tags.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for station in stations:
            name = station.get("name", "Unknown")
            country = station.get("country", "Unknown")
            tags = station.get("tags", "")
            url = station.get("url_resolved") or station.get("url")

            if not url:
                continue

            # Linha de descrição (EXTINF)
            description = f"{name} - {country} - {tags}"
            f.write(f"#EXTINF:-1,{description}\n")
            f.write(f"{url}\n")

if __name__ == "__main__":
    stations = fetch_all_stations()
    print(f"Total de estações baixadas: {len(stations)}")
    save_as_m3u(stations)
    print("Arquivo salvo em stations/all_stations.m3u")
