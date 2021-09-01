#!/usr/bin/env sh

#server='palletten.northeurope.azurecontainer.io'
server='palletten.oliverflecke.me'

port=1883

# IPs for the Shelly instances should be 68, 202 and ?
for IP in 68 202 202
do
  echo "Settings for $IP"
  curl --location --request POST "192.168.1.$IP/settings?mqtt_server=$server:$port&mqtt_enable=true&mqtt_retain=true&update_period=0"
done
