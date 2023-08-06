#!/bin/sh

mv /home/pi/Dashboard/Zumi_Content /home/pi/Dashboard/Zumi_Content_en
mkdir /home/pi/Dashboard/content_history
mv /home/pi/Dashboard/log_v* /home/pi/Dashboard/content_history/
HOST_CURRENT="$(cat /etc/hostname)"

# Populate `/etc/hostapd/hostapd.conf`
cat > /etc/hostapd/hostapd.conf << EOF
ctrl_interface=/var/run/hostapd
ctrl_interface_group=0
interface=ap0
driver=nl80211
country_code=US

ssid=${HOST_CURRENT}
hw_mode=g
channel=11
wmm_enabled=0
macaddr_acl=0
auth_algs=1
wpa=3
wpa_passphrase=${HOST_CURRENT}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP

# Enable 802.11n
ieee80211n=1
# Enable 40MHz channels with 20ns guard interval
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
EOF
