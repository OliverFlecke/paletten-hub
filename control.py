#!/usr/bin/env python3.8
import paho.mqtt.client as mqtt
import sys
import re
import json
import sched
import time
from multiprocessing import Process
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

def log(string: str):
    print(f'{time.time()}: {string}')

def set_state(state: str):
    log(f'Setting state to {state}')

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
        log(f'Got desired temperature: {desired_temp}')
        update_clients()
    except Error as e:
        log(e)

def handle_temperature_change(message):
    global temperature
    try:
        temperature = float(message.payload)
        log(f'Current temperature {temperature}')
        update_clients()
    except Error as e:
        log(e)

def handle_active_change(message):
    global active
    active = message.payload == b'true'
    log(f'Automatic temperature control is {"active" if active else "disabled"}')
    if active:
        update_clients()
    else:
        set_state('off')

def handle_heater_state_change(message):
    #print(f'Received state change at {message.topic}: {message.payload}')
    m = re.match(r'shellies/shelly1-(?P<id>[A-F0-9]*)/relay/0', message.topic)
    if not m:
        log('Message topic does not match expected')
        return

    heater = m.group('id')
    is_on = message.payload == b'on'
    log_heater_state(heater, is_on)
    
    history = get_heater_history_in_last_x_hours(heater, 24)
    client.publish(f'history/heater/{heater}', json.dumps(history), retain=True)

def enable_temperature_control():
    log('Enabling temperature control')
    c = mqtt.Client()
    c.connect(url, port, 60)
    c.publish('temperature/auto', 'true', retain=True)
    c.disconnect()

def run_scheduler(scheduler):
    log('Running scheduler')
    scheduler.run()

p_timer = None
def handle_auto_time(message):
    global p_timer
    t = int(message.payload)
    s = sched.scheduler(time.time, time.sleep)
    s.enterabs(t, 1, enable_temperature_control)

    if p_timer is not None:
        p_timer.kill()

    p_timer = Process(target=run_scheduler, args=(s,))
    p_timer.start()

def on_message(client, userdata, message):
    if message.topic == 'temperature/set':
        handle_set(message)
    elif message.topic == 'temperature/inside':
        handle_temperature_change(message)
    elif message.topic == 'temperature/auto':
        handle_active_change(message)
    elif message.topic == 'temperature/auto/at':
        handle_auto_time(message)
    elif message.topic.startswith('shellies'):
        handle_heater_state_change(message)
    else:
        log(f'Unhandled message received at "{message.topic}": {message.payload}')

client.on_message = on_message

topics = [
    'shellies/+/relay/0', 
    'temperature/inside', 
    'temperature/set', 
    'temperature/auto',
    'temperature/auto/at'
    ]
client.subscribe(list(map(lambda topic: (topic, 1), topics)))

client.loop_forever()

