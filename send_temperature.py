#!/usr/bin/env python3.8
import paho.mqtt.client as mqtt
import Adafruit_DHT
import json
from datetime import datetime
import argparse
from db import insert_reading, latest_reading, history_without_duplicates

parser = argparse.ArgumentParser(description='Send temperature data')
parser.add_argument('place', type=str)
parser.add_argument('pin', type=int)
parser.add_argument('-f', '--force', default=False, action='store_true')

args = parser.parse_args()

url = 'paletten.oliverflecke.me'
port = 1883

last_temp, last_humidity = latest_reading(args.place)

humidity, temperature = Adafruit_DHT.read_retry(11, args.pin)
insert_reading(args.place, temperature, humidity)

client = mqtt.Client()
client.connect(url, port, 60)

if args.force or last_temp != temperature:
    client.publish(f'temperature/{args.place}', f'{temperature:0.1f}', retain=True)
if args.force or last_humidity != humidity:
    client.publish(f'humidity/{args.place}', f'{humidity:0.1f}', retain=True)

# Update broker with latest history
history = history_without_duplicates(args.place, 24)
client.publish(f'history/{args.place}', json.dumps(history), retain=True)

