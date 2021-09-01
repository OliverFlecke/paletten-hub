#!/usr/bin/env python3

import paho.mqtt.client as mqtt

url = 'palletten.oliverflecke.me'
port = 1883

def on_connect(client, userdata, flags, rc):
    print('connected')

client = mqtt.Client(transport="websockets")
client.on_connect = on_connect

print(f'Connectiong to broker {url}')
client.connect(url, port)

client.loop_forever()

