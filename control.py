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
active = False

def set_state(state: str):
    print(f'Setting state to {state}')

    for i in ids:
        client.publish(f'shellies/shelly1-{i}/relay/0/command', state)

def get_state():
    return 'on' if temperature < desired_temp else 'off'

def update_clients():
    set_state(get_state())

def handle_set(message):
    global desired_temp
    try:
        desired_temp = float(message.payload)
        print(f'Got desired temperature: {desired_temp}')
        update_clients()
    except Error as e:
        print(e)

def handle_temperature_change(message):
    global temperature
    try:
        temperature = float(message.payload)
        print(f'Current temperature {temperature}')
        update_clients()
    except Error as e:
        print(e)

def handle_active_change(message):
    global active
    active = message.payload == b'true'
    print(f'Automatic temperature control is {"active" if active else "disabled"}')
    if active:
    	update_clients()
    else:
        set_state('off')

def handle(client, userdata, message):
    #print(f'Received at "{message.topic}": {message.payload}')
    if message.topic == 'temperature/set':
        handle_set(message)
    elif message.topic == 'temperature/inside':
        handle_temperature_change(message)
    elif message.topic == 'temperature/auto':
        handle_active_change(message)

subscribe.callback(handle, ['temperature/inside', 'temperature/set', 'temperature/auto'], hostname=url)

