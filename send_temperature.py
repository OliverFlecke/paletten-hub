#!/usr/bin/env python3.8
import paho.mqtt.client as mqtt
import Adafruit_DHT
import json
from datetime import datetime
import argparse
from db import insert_reading, latest_reading, get_history_in_last_x_hours

parser = argparse.ArgumentParser(description='Send temperature data')
parser.add_argument('place', type=str)
parser.add_argument('pin', type=int)
parser.add_argument('-f', '--force', default=False, action='store_true')

args = parser.parse_args()

url = 'paletten.oliverflecke.me'
port = 1883

client = mqtt.Client()
client.connect(url, port, 60)

last_temp, last_humidity = latest_reading(args.place)

humidity, temperature = Adafruit_DHT.read_retry(11, args.pin)
insert_reading(args.place, temperature, humidity)

if args.force or last_temp != temperature:
    client.publish(f'temperature/{args.place}', f'{temperature:0.1f}', retain=True)
if args.force or last_humidity != humidity:
    client.publish(f'humidity/{args.place}', f'{humidity:0.1f}', retain=True)

# Update broker with latest history
history = json.dumps([
	{ 
		'time': row[0],
		'temp': row[2], 
		'hum': row[3],
	} 
	for row in get_history_in_last_x_hours('inside', 6)])
client.publish(f'history/{args.place}', history, retain=True)

