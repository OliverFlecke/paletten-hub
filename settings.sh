#!/usr/bin/env sh

for IP in 68 202 202
do
  echo "Settings for $IP"
  curl --location --request POST "192.168.1.$IP/settings?mqtt_server=palletten.northeurope.azurecontainer.io:1883&mqtt_enable=true&mqtt_retain=true&update_period=0"
done
