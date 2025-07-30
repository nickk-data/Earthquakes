# Importing earthquake data within 100 km of Reno, NV from the last 7 days

import requests
import psycopg2 as p
from datetime import datetime, timedelta, timezone

# Define the parameters for the USGS API request
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
parameters = {
    'format': 'geojson',
    'starttime': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
    'endtime': datetime.now().strftime('%Y-%m-%d'),
    'latitude': 39.5296,
    'longitude': -119.8138,
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
            'time': datetime.(properties.get('time') / 1000),  # Convert from ms to seconds
            'latitude': geometry[1],  # Geometry stores [longitude, latitude]
            'longitude': geometry[0],
            'depth_km': geometry[2],
            'magnitude': properties.get('mag'),
            'place': properties.get('place'),
            'insert_date_time': datetime.now(),
        }

        # sql
        keys = ", ".join(earthquake_data.keys())
        values = ", ".join(["%s"] * len(earthquake_data))
        sql = (f'INSERT INTO Reno ({keys}) VALUES ({values})')

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
