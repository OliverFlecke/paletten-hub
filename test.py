import time 
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D18)

while True:
    try:
        print('hello')
        #print(f'{dhtDevice.temperature}')
    except:
        pass

    time.sleep(2.0)
