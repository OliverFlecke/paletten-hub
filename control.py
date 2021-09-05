#!/usr/bin/env python3.8
import paho.mqtt.client as mqtt
import sys
import re
import json
from db import log_heater_state, get_heater_history_in_last_x_hours

print('Starting control')

ids = ['C4402D', 'C431FB', '10DB9C']
url = 'paletten.oliverflecke.me'
port = 1883

client = mqtt.Client()
client.connect(url, port, 60)

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

def handle_heater_state_change(message):
    #print(f'Received state change at {message.topic}: {message.payload}')
    m = re.match(r'shellies/shelly1-(?P<id>[A-F0-9]*)/relay/0', message.topic)
    if not m:
        print('Message topic does not match expected')
        return

    heater = m.group('id')
    is_on = message.payload == b'on'
    log_heater_state(heater, is_on)
    
    history = get_heater_history_in_last_x_hours(heater, 24)
    client.publish(f'history/heater/{heater}', json.dumps(history), retain=True)

def on_message(client, userdata, message):
    if message.topic == 'temperature/set':
        handle_set(message)
    elif message.topic == 'temperature/inside':
        handle_temperature_change(message)
    elif message.topic == 'temperature/auto':
        handle_active_change(message)
    elif message.topic.startswith('shellies'):
        handle_heater_state_change(message)
    else:
        print(f'Unhandled message received at "{message.topic}": {message.payload}')

client.on_message = on_message

topics = ['shellies/+/relay/0', 'temperature/inside', 'temperature/set', 'temperature/auto']
client.subscribe(list(map(lambda topic: (topic, 1), topics)))

client.loop_forever()

