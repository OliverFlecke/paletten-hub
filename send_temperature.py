#!/usr/bin/env python3.8
import paho.mqtt.client as mqtt
import Adafruit_DHT
import json
from datetime import datetime
import re
import argparse

parser = argparse.ArgumentParser(description='Send temperature data')
parser.add_argument('place', type=str)
parser.add_argument('pin', type=int)

args = parser.parse_args()

history_file = f'/home/pi/temperature/history_{args.place}.txt'
url = 'palletten.northeurope.azurecontainer.io'

client = mqtt.Client()
client.connect(url, 1883, 60)

humidity, temperature = Adafruit_DHT.read_retry(11, args.pin)

with open(history_file, 'r') as history:
   for line in history:
       pass
   m = re.match(r'.*: (?P<temp>[\d]+\.[\d]+), (?P<humidity>[\d]+\.[\d]+)$', line)
   last_temp = float(m.group('temp'))
   last_humidity = float(m.group('humidity'))

print(f'{args.place} - Temperature: {temperature:0.1f} \tHumidity: {humidity:0.1f}')
with open(history_file, 'a') as history:
    history.write(f'{datetime.now()}: {temperature}, {humidity}\n')

if last_temp != temperature:
    client.publish(f'temperature/{args.place}', f'{temperature:0.1f}', retain=True)
if last_humidity != humidity:
    client.publish(f'humidity/{args.place}', f'{humidity:0.1f}', retain=True)

