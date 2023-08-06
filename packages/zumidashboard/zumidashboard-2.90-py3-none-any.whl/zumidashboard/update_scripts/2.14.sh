#!/bin/sh

# add same script in 2.11 because of script 2.10 is build from window so that is causing issue

cat > /etc/systemd/system/zumi_wifi_setup.service << EOF
[Unit]
Description=zumidashboard wifi connect service
After=network.target
[Service]
WorkingDirectory=/home/pi
ExecStart=/bin/bash /usr/local/lib/python3.5/dist-packages/zumidashboard/shell_scripts/zumi_wifi_setup.sh
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
