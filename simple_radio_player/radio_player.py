import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import signal
import json
import requests
import shlex

class RadioPlayer:
    """
    Classe principal do tocador de rádio.
    Gerencia a interface gráfica, a lista de estações e a reprodução de áudio.
    """

    def __init__(self, root):
        """
        Inicializa a janela principal e configura o frame com borda dupla.
        """
        self.root = root
        self.root.title("Simples Tocador de Rádio")

        # Personaliza o estilo do frame principal para ter uma borda dupla
        style = ttk.Style()
        style.configure(
            "MainFrame.TFrame",
            background="#f0f0f0",
            borderwidth=5,
            relief="groove"  # Estilo da borda: "groove", "ridge", "solid", etc.
        )

        # Cria um frame principal com estilo personalizado para envolver toda a janela
        self.main_frame = ttk.Frame(self.root, style="MainFrame.TFrame", padding=10)
        self.main_frame.pack(fill="both", expand=True)  # Preenche toda a janela

        # Inicializa as variáveis
        self.stations_dir = "stations"
        self.stations = self.load_stations()
        self.current_station = 0
        self.player_process = None
        self.volume = 70

        # Chama o método para criar os widgets
        self.create_widgets()

        # Configura o fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_stations(self):
        """Carrega a lista de estações de rádio do arquivo all_stations.m3u."""
        if not os.path.exists(self.stations_dir):
            os.makedirs(self.stations_dir)
        if os.path.exists(f"{self.stations_dir}/all_stations.m3u"):
            with open(f"{self.stations_dir}/all_stations.m3u", "r") as f:
                return f.readlines()
        return []

    def load_filters(self):
        """Carrega os filtros de países e tags das estações."""
        countries = set()
        tags = set()
        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
                if line.startswith("#EXTINF:"):
                    # Extrair a descrição: "#EXTINF:-1,<nome> - <país> - <tags>"
                    description = line.split(",", 1)[1]
                    parts = description.split(" - ")
                    if len(parts) >= 3:
                        country = parts[1].strip()
                        station_tags = parts[2].strip().split(", ")
                        countries.add(country)
                        tags.update(station_tags)
        self.countries = sorted(countries)
        self.tags = sorted(tags)

    def filter_stations(self, event=None):
        """Filtra as estações por país ou tag."""
        country = self.country_combo.get()
        tag = self.tag_combo.get()
        self.station_list.delete(0, "end")
        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
                if line.startswith("#EXTINF:"):
                    description = line.split(",", 1)[1]
                    parts = description.split(" - ")
                    if len(parts) >= 3:
                        station_name = parts[0].strip()
                        station_country = parts[1].strip()
                        station_tags = parts[2].strip().split(", ")
                        if ((not country) or country == station_country) and ((not tag) or tag in station_tags):
                            self.station_list.insert("end", station_name)


    def create_widgets(self):
        """Cria todos os widgets da interface gráfica."""
        # Frame de filtros
        filter_frame = ttk.LabelFrame(self.main_frame, text="Filtros")
        filter_frame.pack(fill="x", padx=10, pady=5)
        self.load_filters()
        ttk.Label(filter_frame, text="País:").grid(row=0, column=0, padx=5)
        self.country_combo = ttk.Combobox(filter_frame, values=self.countries, width=20)
        self.country_combo.grid(row=0, column=1, padx=5)
        self.country_combo.bind("<<ComboboxSelected>>", self.filter_stations)
        ttk.Label(filter_frame, text="Tag:").grid(row=0, column=2, padx=5)
        self.tag_combo = ttk.Combobox(filter_frame, values=self.tags, width=20)
        self.tag_combo.grid(row=0, column=3, padx=5)
        self.tag_combo.bind("<<ComboboxSelected>>", self.filter_stations)
        ttk.Label(filter_frame, text="Busca:").grid(row=0, column=4, padx=5)
        self.search_entry = ttk.Entry(filter_frame, width=20)
        self.search_entry.grid(row=0, column=5, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_stations)
        ttk.Button(filter_frame, text="Atualizar Rádios", command=self.update_stations).grid(row=0, column=6, padx=5)

        # Frame para URL externa
        url_frame = ttk.LabelFrame(self.main_frame, text="Reproduzir URL Externa")
        url_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, padx=5)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=5)
        ttk.Button(url_frame, text="Play Externo", command=self.play_external_url).grid(row=0, column=2, padx=5)

        # Lista de estações e barra de rolagem
        self.station_list = tk.Listbox(self.main_frame, height=10, width=60, bg="yellow")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.station_list.yview)
        self.station_list.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.station_list.pack(fill="both", expand=True, padx=15, pady=15)

        # Preenche a lista de estações
        self.station_urls = []  # Lista para armazenar as URLs das estações
        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
            if line.startswith("#EXTINF:"):
                description = line.split(",", 1)[1]
                station_name = description.split(" - ")[0].strip()
                self.station_list.insert("end", station_name)
                self.station_urls.append(self.stations[i + 1].strip())  # Armazena a URL correspondente

        if self.stations:
            self.station_list.selection_set(0)
        self.station_list.bind("<<ListboxSelect>>", self.on_select)

        # Frame dos botões
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)

        # Botões de controle
        self.prev_btn = ttk.Button(btn_frame, text="Anterior", command=self.prev_station)
        self.prev_btn.pack(side="left", padx=5)
        self.play_btn = ttk.Button(btn_frame, text="Play", command=self.play_station)
        self.play_btn.pack(side="left", padx=5)
        self.pause_btn = ttk.Button(btn_frame, text="Pausa", command=self.pause_station)
        self.pause_btn.pack(side="left", padx=5)
        self.next_btn = ttk.Button(btn_frame, text="Próxima", command=self.next_station)
        self.next_btn.pack(side="left", padx=5)

        # Controle de volume
        ttk.Label(btn_frame, text="Volume:").pack(side="left", padx=5)
        self.volume_scale = ttk.Scale(btn_frame, from_=0, to=100, orient="horizontal", command=self.change_volume)
        self.volume_scale.set(self.volume)
        self.volume_scale.pack(side="left", padx=5)

        # Botão "Sair"
        self.exit_btn = ttk.Button(btn_frame, text="Sair", command=self.on_close)
        self.exit_btn.pack(side="left", padx=5)

    def play_external_url(self):
        """Abre um xterm e executa o mpv com a URL informada."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Erro", "Informe uma URL válida!")
            return
        try:
#           subprocess.Popen(["xterm", "-e", "mpv", url])
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"mpv {url}; exec bash"])
            '''
            gnome-terminal -- bash -c "mpv <url>; exec bash":
            Abre um novo terminal.
            Executa o mpv com a URL.
            Mantém o terminal aberto após o mpv ser fechado (por causa do exec bash).
            '''
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o gnome-terminal/mpv: {e}")

    def on_select(self, event):
        """Chamado quando uma estação é selecionada na lista."""
        selection = self.station_list.curselection()
        if selection:
            self.current_station = selection[0]

    def play_station(self):
        """Inicia a reprodução da estação selecionada."""
        self.kill_all_mpv()  # Mata todos os processos mpv antes de iniciar um novo

        # Obtém o nome da estação a partir da linha #EXTINF
        station_info_line = self.stations[self.current_station * 2].strip()
        station_name = station_info_line.split(",", 1)[1].split(" - ")[0].strip()
        station_url = self.station_urls[self.current_station]

        print(f"Reproduzindo: {station_name} ({station_url})")

        try:
            response = requests.head(station_url, timeout=5)
            if response.status_code == 200:
                escaped_url = shlex.quote(station_url)
                self.player_process = subprocess.Popen(["mpv", "--no-video", "--volume=" + str(self.volume), escaped_url])
            else:
                messagebox.showerror("Erro", f"Não foi possível tocar a estação: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Não foi possível tocar a estação: {e}")


    def pause_station(self):
        """Pausa a reprodução da estação atual."""
        self.kill_all_mpv()
        self.player_process = None

    def kill_all_mpv(self):
        """Encerra todos os processos do mpv."""
        subprocess.run(["pkill", "-f", "mpv"])

    def on_close(self):
        """Chamado ao fechar a janela."""
        self.kill_all_mpv()
        self.root.destroy()
        sys.exit(0)  # Encerra o script explicitamente

    def prev_station(self):
        """Selecionar a estação anterior."""
        if self.current_station > 0:
            self.current_station -= 1
            self.station_list.selection_clear(0, "end")
            self.station_list.selection_set(self.current_station)
            self.play_station()

    def next_station(self):
        """Selecionar a próxima estação."""
        if self.current_station < len(self.station_urls) - 1:
            self.current_station += 1
            self.station_list.selection_clear(0, "end")
            self.station_list.selection_set(self.current_station)
            self.play_station()

    def change_volume(self, volume):
        """Altera o volume da reprodução."""
        self.volume = int(float(volume))
        if self.player_process:
            self.player_process.terminate()
            self.play_station()

    def filter_stations(self, event=None):
        """Filtra as estações por país ou tag."""
        country = self.country_combo.get()
        tag = self.tag_combo.get()
        self.station_list.delete(0, "end")
        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
                if line.startswith("#EXTINF:"):
                    parts = line.split(",")
                    if len(parts) > 3:
                        station_name = parts[1]
                        station_country = parts[2]
                        station_tags = parts[3:]
                        if ((not country) or country == station_country) and ((not tag) or tag in station_tags):
                            self.station_list.insert("end", station_name)

    def search_stations(self, event=None):
        """Busca estações pelo nome."""
        search_term = self.search_entry.get().lower()
        self.station_list.delete(0, "end")
        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
                if line.startswith("#EXTINF:"):
                    parts = line.split(",")
                    if len(parts) > 1:
                        station_name = parts[1].lower()
                        if search_term in station_name:
                            self.station_list.insert("end", parts[1])

    def update_stations(self):
        """Atualiza a lista de estações."""
        subprocess.run(["python3", "update_stations.py"])
        self.stations = self.load_stations()
        self.load_filters()
        self.station_list.delete(0, "end")
        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
                if line.startswith("#EXTINF:"):
                    parts = line.split(",")
                    if len(parts) > 1:
                        self.station_list.insert("end", parts[1])
        messagebox.showinfo("Sucesso", "Rádios atualizadas com sucesso!")
        messagebox.showinfo("Atenção: fonte ...", "API: https://de1.api.radio-browser.info/json/stations")

if __name__ == "__main__":
    root = tk.Tk()
    app = RadioPlayer(root)
    root.mainloop()
