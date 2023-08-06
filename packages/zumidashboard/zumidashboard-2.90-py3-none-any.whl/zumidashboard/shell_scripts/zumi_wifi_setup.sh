#!/bin/bash

killall wpa_supplicant
rm -rf /var/run/wpa_supplicant/wlan0
sleep 1
wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
dhclient wlan0

while true
do
  sleep 100
done
