#!/bin/sh
#some people have problem with seeing after 2.0 update still not sure but will update this again
sudo rm /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json
sudo ln -s /etc/hostname /usr/local/lib/python3.5/dist-packages/zumidashboard/dashboard/hostname.json