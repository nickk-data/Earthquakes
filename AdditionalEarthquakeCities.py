# Importing earthquake data going back to the first extraction for Reno. This is not recurring as I'm just trying to build multiple tables for a dbt project.
# I ran this script for Los Angeles, San Francisco, Portland (OR), and Seattle. This is what I ran to get the Los Angeles data.

import requests
import psycopg2 as p
from datetime import datetime, timedelta, timezone

# Define the parameters for the USGS API request
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
parameters = {
    'format': 'geojson',
    'starttime': (datetime.now() - timedelta(days=171)).strftime('%Y-%m-%d'),
    'endtime': (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d'),
    'latitude': 34.05,
    'longitude': -118.24,
    'maxradiuskm': 100
}

# Database credentials
db_name = "Earthquakes"
db_host = "localhost"
db_port = "5432"
db_user = 'postgres'
db_password = 'password'

# Send to Postgres
cursor = None
conn = None

try:
    conn = p.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port, 
    )
    cursor = conn.cursor()

    # Fetch data from USGS API
    response = requests.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()

    # Loop through the earthquake data
    for record in data['features']:
        # Extract relevant data
        properties = record['properties']
        geometry = record['geometry']['coordinates']  # [longitude, latitude]

        # Fields
        earthquake_data = {
            'time': datetime.utcfromtimestamp(properties.get('time') / 1000),  # Convert from ms to seconds
            'latitude': geometry[1],  # Geometry stores [longitude, latitude]
            'longitude': geometry[0],
            'depth_km': geometry[2],
            'magnitude': properties.get('mag'),
            'place': properties.get('place'),
            'insert_date_time': datetime.now(),
        }

        # Ensure that only the necessary columns are being inserted
        keys = ", ".join(earthquake_data.keys())
        values = ", ".join(["%s"] * len(earthquake_data))
        sql = (f'INSERT INTO LosAngeles ({keys}) VALUES ({values})')

        # Execute the query
        cursor.execute(sql, list(earthquake_data.values()))

    # Commit the transaction
    conn.commit()
    print("Data inserted successfully")

except requests.exceptions.RequestException as e:
    print(f'API request error: {e}')

except p.Error as e:
    print(f'Database error: {e}')
    if conn:
        conn.rollback()

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
