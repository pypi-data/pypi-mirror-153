# Flask-AP

<H2>AP Mode Set Up</H2>

**Update your pi and install hostapd and dnsmasq**

---

sudo apt-get update<br>
sudo apt-get install hostapd<br>
sudo apt-get install dnsmasq<br>
sudo systemctl stop hostapd<br>
sudo systemctl stop dnsmasq

---

**Add the following lines to /etc/dhcpcd.conf**

```
interface wlan0
static ip_address=192.168.0.10/24
nohook wpa_supplicant
```

**Move the original dnsmasq.conf file under a new name**

---

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

---

**Create a new /etc/dnsmasq.conf file and add the following lines**

```
interface=wlan0
dhcp-range=192.168.0.11,192.168.0.30,255.255.255.0,24h
```

**Create a new file /etc/hostapd/hostapd.conf and add the following lines**

```
interface=wlan0
driver=nl80211
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=whateverssidwant
wpa_passphrase=whateverpasswordyouwant
```

**Change the `DAEMON_CONF=""` line in /etc/default/hostapd to `DAEMON_CONF="/etc/hostapd/hostapd.conf"`**

**Disable hostapd and restart your pi**

---

sudo systemctl disable hostapd<br>
sudo reboot

---

**After reboot unmask hostapd and start the services**

---

sudo systemctl unmask hostapd<br>
sudo systemctl start dnsmasq<br>
sudo systemctl start hostapd

---

<h1>Setup dashboard</h1>
Install flask-socketio package by running
```
sudo pip3 install flask-socketio
```

Now you should be able to bring up socketio and serve dashboard static files by running

```
sudo python3 app.py
```

Check zumi.local:3456

<h3>Restart wlan0 and ap0 interfaces</h3>
If ap0 or wlan0 don't show on ifconfig or Zumi AP network doesn't show up you can 
restart both interfaces by running rpi-wifi-manual script on root directory like this:
```
sudo sh rpi-wifi-manual.sh
```
