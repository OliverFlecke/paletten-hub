#!/usr/bin/env python3.8

import sqlite3

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

