#!/usr/bin/env sh

#server='palletten.northeurope.azurecontainer.io'
server='paletten.oliverflecke.me'

port=1883

# IPs for the Shelly instances should be 68, 203 and 217. Note that these are not static. 
# MQTT server can also be changed from the web UI which can be found by visiting each of the shellies IPs.

for IP in 68 202
do
  echo "Settings for $IP"
  curl --location --request POST "192.168.1.$IP/settings?mqtt_server=$server:$port&mqtt_enable=true&mqtt_retain=true&update_period=0"
done
