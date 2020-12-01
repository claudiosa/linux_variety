#!/bin/bash
clear
rm *.zip
#currentDate = `date  +%d%m%Y'
#currentDate = `date  +"%d%m%Y"`
CURRENTDATE=`date +"%d%m%y"`   ### %y  only 20
#echo $CURRENTDATE
ZIP=".zip"
PREFIX_01="https://iptvm3ulist.com/zip/"
PREFIX_02="fr_iptvm3ulist_com_"
THE_ZIP=$PREFIX_01$PREFIX_02$CURRENTDATE$ZIP
echo "FILE:"$THE_ZIP
wget  $THE_ZIP
unzip -o $PREFIX_02$CURRENTDATE$ZIP
rm $PREFIX_02$CURRENTDATE$ZIP
#unzip fr_iptvm3ulist_com_301120.zip
#rm fr_iptvm3ulist_com_301120.zip
echo "==== OK ===="
