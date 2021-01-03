#!/usr/bin/env python3

import sys
from datetime import datetime
import Adafruit_DHT

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    print(f'{datetime.now()} Temp: {temperature:0.1f} C \tHumidity: {humidity:0.1f} %')
