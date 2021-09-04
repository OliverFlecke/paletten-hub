
CREATE TABLE history (
	timestamp DATETIME NOT NULL,
	location TEXT NOT NULL,
	temperature INT NOT NULL,
	humidity INT NOT NULL
);
CREATE INDEX history_timestamp_index on history (timestamp);

