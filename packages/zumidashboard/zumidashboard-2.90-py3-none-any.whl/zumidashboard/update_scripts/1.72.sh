#!/bin/sh

searchdir="/home/pi/Dashboard/user"

echo $searchdir
for entry in $searchdir/*
do
        echo "$entry/content_history"
        if ! [ -d "$entry/content_history" ] ;then
                mkdir $entry/content_history
                mv $entry/log_* $entry/content_history
                sudo chown -R pi $entry/content_history
        fi
done