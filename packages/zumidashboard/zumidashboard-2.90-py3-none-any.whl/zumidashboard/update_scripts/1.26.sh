#!/bin/sh

HOST_CURRENT="$(cat /etc/hostname)"

cat > /etc/hosts << EOF
127.0.0.1           localhost
192.168.10.1        zumidashboard.ai
192.168.10.1        www.zumidashboard.ai
::1                 localhost ip6-localhost ip6-loopback
ff02::1             ip6-allnodes
ff02::2             ip6-allrouters

127.0.1.1           $HOST_CURRENT
EOF

