import requests
import os
import socket

def get_available_servers():
    """Retorna uma lista de servidores disponíveis da Radio Browser API."""
    try:
        # Faz o DNS lookup para obter a lista de servidores
        result = socket.gethostbyname_ex("all.api.radio-browser.info")
        servers = [f"https://{ip}" for ip in result[2]]
        return servers
    except Exception as e:
        print(f"Erro ao buscar servidores: {e}")
        return []
def fetch_all_stations(limit_per_query=1000):
    """Busca todas as estações usando um servidor disponível."""
    servers = get_available_servers()
    if not servers:
        print("Nenhum servidor disponível.")
        return []

    # Testa cada servidor até encontrar um que responda
    for server in servers:
        url = f"{server}/json/stations"
        params = {"limit": limit_per_query}
        try:
            print(f"Tentando servidor: {url}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            if data:  # Se encontrou estações
                print(f"Sucesso! {len(data)} estações encontradas.")
                return data
        except Exception as e:
            print(f"Erro no servidor {server}: {e}")
            continue

    print("Nenhum servidor respondeu corretamente. Usando backup...")
    # Se nenhum servidor respondeu, copia o backup
    backup_file = "stations/backup_all_stations.m3u"
    target_file = "stations/all_stations.m3u"
    if os.path.exists(backup_file):
        import shutil
        shutil.copy2(backup_file, target_file)
        print(f"Backup copiado para {target_file}")
    else:
        print("Arquivo de backup não encontrado.")

    return []  # Retorna lista vazia para indicar que usou backup

def save_as_m3u(stations, output_file="stations/all_stations.m3u"):
    """Salva a lista de estações no formato .m3u."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for station in stations:
            name = station.get("name", "Unknown")
            country = station.get("country", "Unknown")
            tags = station.get("tags", "")
            url = station.get("url_resolved") or station.get("url")
            if not url:
                continue
            description = f"{name} - {country} - {tags}"
            f.write(f"#EXTINF:-1,{description}\n")
            f.write(f"{url}\n")

if __name__ == "__main__":
    stations = fetch_all_stations()
    print(f"Total de estações baixadas: {len(stations)}")
    if stations:
        save_as_m3u(stations)
        print("Arquivo salvo em stations/all_stations.m3u")
    else:
        print("Nenhuma estação foi baixada.")
