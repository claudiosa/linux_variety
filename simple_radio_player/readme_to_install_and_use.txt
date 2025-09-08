
Requisitos para Rodar no Armbian 12 (ARM)

1. Dependências Básicas
No Armbian (Debian-based), você precisará instalar as mesmas dependências que usa no Debian 12 x86, mas garantindo que sejam compatíveis com a arquitetura ARM (geralmente armhf ou arm64). As principais são:

Python 3 (versão 3.9 ou superior, já incluso no Armbian 12)
Tkinter (para a interface gráfica)
ALSA (para áudio)
mpv (para reprodução de streams)
Audacious (opcional, se for usado como player externo)
git (para clonar o repositório)

2. Instalação das Dependências
Execute os seguintes comandos no terminal da TV Box:


sudo apt update
sudo apt install python3 python3-tk python3-pip mpv audacious git alsa-utils

3. Bibliotecas Python
Instale as bibliotecas Python necessárias (se houver um requirements.txt, use-o):


pip3 install --user -r requirements.txt
Se não houver, instale manualmente as bibliotecas usadas no projeto (ex: pillow, requests, etc.).

4. Ajustes para ARM
Arquitetura ARM: Certifique-se de que todos os pacotes instalados são compatíveis com ARM. Alguns pacotes Python podem precisar de versões específicas para ARM (ex: pyalsaaudio).

ALSA: Verifique se o áudio está configurado corretamente no Armbian. Teste com:


speaker-test -c 2
mpv: Teste se o mpv funciona corretamente no ARM:


mpv --version


5. Teste o Projeto
Clone o repositório na TV Box e execute o script principal:


git clone https://github.com/claudiosa/linux_variety.git
cd linux_variety/simple_radio_player
python3 radio_player.py


6. Para executar:
sh simple_radio.sh
ou 
python radio_player.py

