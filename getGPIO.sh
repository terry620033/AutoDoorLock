#!/bin/sh

cd /home/pi/ADP/
while :
do
  gpio readall > gpio.log
  sleep 0.125
done
