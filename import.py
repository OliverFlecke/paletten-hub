#!/usr/bin/env python3.8

import sqlite3
import re

con = sqlite3.connect('db/paletten.sqlite')

places = ['inside', 'outside']
for place in places:
	print(f'Importing place {place}')	
	with open(f'history_{place}.txt', 'r') as txt:
		for row in txt.readlines():
			values = row.split(' ')
			time = re.sub(r'\.\d+$', '', values[1][:-1])
			timestamp = f'{values[0]} {time}'
			temperature = int(values[2].replace('.0,', ''))
			humidity = int(values[3].replace('.0', '').strip())

			con.execute('INSERT INTO history VALUES (?, ?, ?, ?)', 
				(timestamp, place, temperature, humidity))
		
		con.commit()

