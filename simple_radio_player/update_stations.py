import requests
import os
import json

def fetch_stations_from_radio_browser():
    url = "http://all.api.radio-browser.info/json/stations"
    params = {
        "limit": 10000,
        "hidebroken": True,
        "order": "clickcount",
        "reverse": True
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            stations = response.json()
            os.makedirs("stations", exist_ok=True)
            with open("stations/all_stations.m3u", "w") as f:
                for station in stations:
                    name = station['name']
                    country = station.get('country', 'Unknown')
                    tags = station.get('tags', 'Unknown')
                    url = station['url']
                    f.write(f"#EXTINF:-1,{name},{country},{tags}\n{url}\n")
            print(f"Salvas {len(stations)} rádios em 'stations/all_stations.m3u'")
        else:
            print(f"Falha ao buscar rádios. Código de status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao buscar rádios: {e}")

if __name__ == "__main__":
    if os.path.exists("stations/all_stations.m3u"):
        os.remove("stations/all_stations.m3u")
    print("Apagando arquivo antigo e buscando novas rádios...")
    fetch_stations_from_radio_browser()
    print("Rádios atualizadas com sucesso!")
