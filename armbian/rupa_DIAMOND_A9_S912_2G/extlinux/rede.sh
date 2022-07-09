#!/bin/bash
MOD="realtek mdio-mux-meson-g12a dwmac_meson8b"

for i in $MOD; do
    [ -d /sys/module/$i ] || modprobe $i
    echo $i
done