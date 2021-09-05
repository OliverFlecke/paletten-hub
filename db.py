#!/usr/bin/env python3.8

import sqlite3
import json

con = sqlite3.connect('/home/pi/temperature/db/paletten.sqlite')

def insert_reading(location: str, temperature: int, humidity: int):
	con.execute('INSERT INTO history VALUES (CURRENT_TIMESTAMP, ?, ?, ?)', (location, temperature, humidity))
	con.commit()

def latest_reading(location: str) -> (int, int):
	rows = con.cursor().execute(
		"""SELECT temperature, humidity FROM history 
		WHERE location = ? 
		ORDER BY timestamp DESC
		LIMIT 1""",
		(location, ))
	for row in rows:
		return row
		
	return (None, None)

def get_history_in_last_x_hours(location: str, hours: int):
	hours_sql = f'-{hours} hour'
	return con.cursor().execute("""
		SELECT * FROM history
		WHERE location = ?
		AND timestamp > datetime('now', ?)
		ORDER BY timestamp DESC
		""",
		(location, hours_sql))

def history_without_duplicates(location: str, hours: int):
	history = []

	prev = None
	for row in get_history_in_last_x_hours(location, hours):
		current = {
			'time': row[0],
			'temp': row[2], 
			'hum': row[3],
		}

		if prev == None or prev['temp'] != current['temp'] or prev['hum'] != current['hum']:
			history.append(current)
			prev = current	

	return history

def get_last_heater_state(heater: str):
    rows = con.cursor().execute("""
        SELECT is_active FROM heater_history
        WHERE shelly_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (heater, ))
    for row in rows:
        return row[0] == 1

    return None

def log_heater_state(heater: str, active: bool):
    last_state = get_last_heater_state(heater)
    if last_state == active: return

    con.execute("""INSERT INTO heater_history VALUES (CURRENT_TIMESTAMP, ?, ?)""",
        (heater, active))
    con.commit()

def get_heater_history_in_last_x_hours(heater: str, hours: int):
    hours_sql = f'-{hours} hour'
    rows = con.cursor().execute("""
        SELECT * FROM heater_history
        WHERE shelly_id = ?
        AND timestamp > datetime('now', ?)
        ORDER BY timestamp DESC
        """,
        (heater, hours_sql))

    return [{
            'time': row[0],
            'on': row[2] == 1
        } for row in rows]

