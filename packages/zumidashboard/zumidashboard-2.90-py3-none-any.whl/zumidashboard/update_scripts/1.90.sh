#!/bin/sh
searchdir="/home/pi/Dashboard/user"
echo $searchdir
for entry in $searchdir/*
do
        echo $entry
        if ! [ -f "$entry/.overlay.json" ] ;then
                echo "generate"
                cat > $entry/.overlay.json << EOF
{"learn": true, "main": true}
EOF
        fi
done