import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import json
import requests

class RadioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Tocador de Rádio")
        self.stations_dir = "stations"
        self.stations = self.load_stations()
        self.current_station = 0
        self.player_process = None
        self.volume = 70
        self.create_widgets()

    def load_stations(self):
        if not os.path.exists(self.stations_dir):
            os.makedirs(self.stations_dir)
        if os.path.exists(f"{self.stations_dir}/all_stations.m3u"):
            with open(f"{self.stations_dir}/all_stations.m3u", "r") as f:
                return f.readlines()
        return []

    def load_filters(self):
        countries = set()
        tags = set()
        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
                if line.startswith("#EXTINF:"):
                    parts = line.split(",")
                    if len(parts) > 3:
                        countries.add(parts[2])
                        tags.update(parts[3:])
        self.countries = sorted(countries)
        self.tags = sorted(tags)

    def create_widgets(self):
        self.load_filters()

        filter_frame = ttk.LabelFrame(self.root, text="Filtros")
        filter_frame.pack(fill="x", padx=10, pady=5)

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

        self.station_list = tk.Listbox(self.root, height=10)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.station_list.yview)
        self.station_list.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.station_list.pack(fill="both", expand=True, padx=10, pady=10)

        for i in range(0, len(self.stations), 2):
            if i + 1 < len(self.stations):
                line = self.stations[i].strip()
                if line.startswith("#EXTINF:"):
                    parts = line.split(",")
                    if len(parts) > 1:
                        self.station_list.insert("end", parts[1])

        if self.stations:
            self.station_list.selection_set(0)
        self.station_list.bind("<<ListboxSelect>>", self.on_select)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.prev_btn = ttk.Button(btn_frame, text="Anterior", command=self.prev_station)
        self.prev_btn.pack(side="left", padx=5)

        self.play_btn = ttk.Button(btn_frame, text="Play", command=self.play_station)
        self.play_btn.pack(side="left", padx=5)

        self.pause_btn = ttk.Button(btn_frame, text="Pausa", command=self.pause_station)
        self.pause_btn.pack(side="left", padx=5)

        self.next_btn = ttk.Button(btn_frame, text="Próxima", command=self.next_station)
        self.next_btn.pack(side="left", padx=5)

        ttk.Label(btn_frame, text="Volume:").pack(side="left", padx=5)
        self.volume_scale = ttk.Scale(btn_frame, from_=0, to=100, orient="horizontal", command=self.change_volume)
        self.volume_scale.set(self.volume)
        self.volume_scale.pack(side="left", padx=5)

        self.station_label = ttk.Label(self.root, text="Selecione uma estação")
        self.station_label.pack(pady=5)

    def on_select(self, event):
        self.current_station = self.station_list.curselection()[0]
        self.play_station()

    def play_station(self):
        if self.player_process:
            self.player_process.terminate()
        station_line = self.stations[self.current_station * 2 + 1].strip()
        try:
            response = requests.head(station_line, timeout=5)
            if response.status_code == 200:
                self.player_process = subprocess.Popen(["mpv", "--no-video", "--volume=" + str(self.volume), station_line])
            else:
                messagebox.showerror("Erro", f"Não foi possível tocar a estação: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Não foi possível tocar a estação: {e}")

    def pause_station(self):
        if self.player_process:
            self.player_process.terminate()
            self.player_process = None

    def prev_station(self):
        if self.current_station > 0:
            self.current_station -= 1
            self.station_list.selection_clear(0, "end")
            self.station_list.selection_set(self.current_station)
            self.play_station()

    def next_station(self):
        if self.current_station < len(self.stations) // 2 - 1:
            self.current_station += 1
            self.station_list.selection_clear(0, "end")
            self.station_list.selection_set(self.current_station)
            self.play_station()

    def change_volume(self, volume):
        self.volume = int(float(volume))
        if self.player_process:
            self.player_process.terminate()
            self.play_station()

    def filter_stations(self, event=None):
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
        subprocess.run(["python", "update_stations.py"])
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

if __name__ == "__main__":
    root = tk.Tk()
    app = RadioPlayer(root)
    root.mainloop()
