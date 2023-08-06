#!/bin/sh

AP_IP=${ARG_AP_IP:-'192.168.10.1'}
AP_IP_BEGIN=`echo "${AP_IP}" | sed -e 's/\.[0-9]\{1,3\}$//g'`

sudo systemctl disable dhcpcd

# Populate `/bin/rpi-wifi.sh`
cat > /bin/rpi-wifi.sh << EOF
echo 'Starting Wifi AP and client...'
sleep 30
sudo ifdown --force wlan0
sudo ifdown --force ap0
sudo ifup ap0
sudo ifup wlan0
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s ${AP_IP_BEGIN}.0/24 ! -d ${AP_IP_BEGIN}.0/24 -j MASQUERADE
sudo systemctl restart dnsmasq
EOF
sudo chmod +x /bin/rpi-wifi.sh

