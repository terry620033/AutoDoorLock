cd /home/pi/ADP/log
CurrentLog=/home/pi/ADP/log/currentLog.log
echo $CurrentLog
unlink $CurrentLog
file=`ls /home/pi/ADP/log/*.log | tail -n 1 | cut -d ' ' -f 1`
if test -f "$CurrentLog"; then
    echo "$CurrentLog existed, and we are going to remove it."
    rm $CurrentLog
fi
ln -s $file $CurrentLog
