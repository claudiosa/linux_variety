# Para configurar um teclado ABNT2 (ou qualquer outro mapa de teclado) no Linux via linha de comando, 
# basta usar o comando setxkbmap, que faz parte do pacote zsh-common. Este comando possui diversas 
# opções, mas no caso da configuração específica do layout ABNT2, usaremos as seguintes opções:
# setxkbmap -model pc105 -layout br -variant abnt2
# PACOTE: pacote zsh-common
!/bin/bash
setxkbmap -model pc105 -layout br -variant abnt2
