#!/usr/bin/env python3.8
import paho.mqtt.client as mqtt
import Adafruit_DHT
import json
from datetime import datetime
import re
import argparse
from db import insert_reading

parser = argparse.ArgumentParser(description='Send temperature data')
parser.add_argument('place', type=str)
parser.add_argument('pin', type=int)
parser.add_argument('-f', '--force', default=False, action='store_true')

args = parser.parse_args()

history_file = f'/home/pi/temperature/history_{args.place}.txt'
url = 'paletten.oliverflecke.me'
port = 1883

client = mqtt.Client()
client.connect(url, port, 60)

last_temp = None
last_humidity = None

humidity, temperature = Adafruit_DHT.read_retry(11, args.pin)

with open(history_file, 'r') as history:
   for line in history:
       pass
   m = re.match(r'.*: (?P<temp>[\d]+\.[\d]+), (?P<humidity>[\d]+\.[\d]+)$', line)
   if m is not None:
       last_temp = float(m.group('temp'))
       last_humidity = float(m.group('humidity'))

# print(f'{args.place} - Temperature: {temperature:0.1f} \tHumidity: {humidity:0.1f}')
# with open(history_file, 'a') as history:
    #history.write(f'{datetime.now()}, {temperature}, {humidity}\n')

insert_reading(args.place, temperature, humidity)

if args.force or last_temp != temperature:
    client.publish(f'temperature/{args.place}', f'{temperature:0.1f}', retain=True)
if args.force or last_humidity != humidity:
    client.publish(f'humidity/{args.place}', f'{humidity:0.1f}', retain=True)

