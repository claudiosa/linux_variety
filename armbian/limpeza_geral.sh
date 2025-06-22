#!/bin/bash

# Limpar logs antigos do sistema
echo "Limpando logs antigos..."
sudo journalctl --vacuum-time=7d  # Remove logs do systemd com mais de 7 dias
sudo rm -rf /var/log/*            # Remove todos os logs antigos (cuidado com logs importantes)
sudo rm -rf /var/log/journal/*     # Remove os logs do journal (se não for necessário)

# Limpar cache do APT
echo "Limpando cache do APT..."
sudo apt-get clean                # Remove pacotes .deb baixados
sudo apt-get autoclean            # Remove pacotes antigos que não podem mais ser baixados

# Limpar arquivos temporários
echo "Limpando arquivos temporários..."
sudo rm -rf /tmp/*                # Limpa arquivos temporários

# Limpar cache de usuário (se necessário)
echo "Limpando cache do usuário..."
rm -rf ~/.cache/*                 # Limpa o cache do usuário

# Limpar pacotes órfãos (pacotes não necessários)
echo "Removendo pacotes órfãos..."
sudo apt-get autoremove --purge   # Remove pacotes órfãos e não necessários

# Limpar arquivos de logs do sistema
echo "Limpeza concluída."

# Verificar espaço livre no disco
echo "Espaço livre no disco após a limpeza:"
df -h
