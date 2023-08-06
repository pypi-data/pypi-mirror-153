#!/bin/sh
sudo rm /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json
sudo ln -s /etc/hostname /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json