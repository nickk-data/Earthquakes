-- Original 'create table'
CREATE TABLE Reno (
	quake_id SERIAL PRIMARY KEY NOT NULL,
	time TIMESTAMP NOT NULL,
	latitude varchar(30) NOT NULL,
	longitude varchar(30) NOT NULL,
	depth_km decimal(10,3) NOT NULL,
	magnitude decimal(10,3) NOT NULL,
	place varchar(255) NOT NULL
);

-- 'Alter table' when I realized I didn't include an 'insert date time' field
ALTER TABLE reno
ADD insert_date_time TIMESTAMP;

-- Inserted the date & time of the first run
UPDATE reno
SET insert_date_time = '2025-02-10 11:00:00.000' WHERE time <= '2025-02-10'; 

-- Inserted the date & time of the second run
UPDATE reno
SET insert_date_time = '2025-02-18 07:55:00.000' WHERE time >= '2025-02-10';

-- Table is now up to date
