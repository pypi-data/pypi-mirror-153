#!/bin/sh

# add same script in 2.11 because of script 2.10 is build from window so that is causing issue

cat > /etc/systemd/system/zumidashboard.service << EOF
[Unit]
Description=zumidashboard for raspberry pi zero
After=network.target
[Service]
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 -u /home/pi/Dashboard/dashboard.py
[Install]
WantedBy=multi-user.target
EOF

cat > /etc/rc.local << EOF
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.
bash /usr/local/bin/check_macaddress.sh
nice -n -15 python3 -c 'import zumidashboard.boot_calibration as b; b.run()' &
exit 0
EOF

cat > /etc/systemd/system/zumi_updater.service << EOF
[Unit]
Description=zumidashboard updater for raspberry pi zero
After=network.target
[Service]
EnvironmentFile=/etc/.updateconf
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /usr/local/lib/python3.5/dist-packages/zumidashboard/updater.py \$args1 \$args2
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable zumidashboard.service