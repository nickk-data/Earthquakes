CREATE TABLE Reno (
	quake_id SERIAL PRIMARY KEY NOT NULL,
	time TIMESTAMP NOT NULL,
	latitude varchar(30) NOT NULL,
	longitude varchar(30) NOT NULL,
	depth_km decimal(10,3) NOT NULL,
	magnitude decimal(10,3) NOT NULL,
	place varchar(255) NOT NULL
);