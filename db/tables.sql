
CREATE TABLE history (
	timestamp DATETIME NOT NULL,
	location TEXT NOT NULL,
	temperature INT NOT NULL,
	humidity INT NOT NULL
);
CREATE INDEX history_timestamp_index ON history (timestamp);

CREATE TABLE heater_history (
    timestamp DATETIME NOT NULL,
    shelly_id TEXT NOT NULL,
    is_active BOOLEAN NOT NULL
);
CREATE INDEX heater_history_timestamp_index ON heater_history (timestamp); 

