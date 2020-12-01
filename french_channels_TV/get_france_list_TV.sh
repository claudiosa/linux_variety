#!/bin/bash
clear
echo "Removing old m3u files ..."
rm *.m3u

#currentDate=`date  +"%d%m%Y"`
CURRENTDATE=`date +"%d%m%y"`   ### %y  only 20
echo "Today is: "`date  +"%d/%m/%Y"`
###$CURRENTDATE
ZIP=".zip"
PREFIX_01="https://iptvm3ulist.com/zip/"   ### URL
PREFIX_02="fr_iptvm3ulist_com_"
FILE_ZIP=$PREFIX_02$CURRENTDATE$ZIP
FULL_PATH_FILE=$PREFIX_01$FILE_ZIP
echo "Getting ....: "$PREFIX_01$FILE_ZIP
wget  $FULL_PATH_FILE
unzip -o $FILE_ZIP
rm $FILE_ZIP
#unzip fr_iptvm3ulist_com_301120.zip
#rm fr_iptvm3ulist_com_301120.zip
echo "==== OK ===="
