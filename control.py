#!/usr/bin/env python3.8
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import sys

print('Starting control')

ids = ['C4402D', 'C431FB', '10DB9C']
url = 'palletten.northeurope.azurecontainer.io'
client = mqtt.Client()
client.connect(url, 1883, 60)

desired_temp = None
temperature = None

def handle(client, userdata, message):
    global desired_temp
    global temperature
    try:
        if message.topic == 'temperature/set':
            desired_temp = float(message.payload)
            print(f'Got desired temperature: {desired_temp}')
        elif message.topic == 'temperature/inside':
            temperature = float(message.payload)
            print(f'Current temperature {temperature}')

        if not temperature or not desired_temp: return

        if temperature < desired_temp: state = 'on'
        else: state = 'off'

        print(f'Setting state to {state}')
    except Error as e:
        print(e)

    for i in ids:
        client.publish(f'shellies/shelly1-{i}/relay/0/command', state)

subscribe.callback(handle, ['temperature/inside', 'temperature/set'], hostname=url)

