#!/bin/sh
#python adp_tls.py
#sh listUpdateLog.sh
cd /home/pi/ADP/log
CurrentLog=/home/pi/ADP/log/currentLog.log
rm $CurrentLog
# echo $CurrentLog
# unlink $CurrentLog
file=`ls /home/pi/ADP/log/*.log | tail -n 1 | cut -d ' ' -f 1`
#if test -f "$CurrentLog"; then
#    echo "$CurrentLog existed, and we are going to remove it."
#fi
ln -s $file $CurrentLog
cd /home/pi/ADP
python adp_tls.py

