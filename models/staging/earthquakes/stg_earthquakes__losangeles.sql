with source as (
    select * 
    from {{ source('earthquakes', 'LosAngeles') }} 
),

convert_to_pacific as (
    select
        time, -- original column name is 'time' from the usgs api
        magnitude,
        depth_km,
        place,
        convert_timezone('UTC', 'America/Los_Angeles', time) as pacific_timestamp -- chose pacific time since all locations are west coast

    from source
),


cleaned as (
    select
        date(time) as earthquake_date,
        to_char(pacific_timestamp, 'HH12:MI:SS AM') as earthquake_time_pacific, 
        magnitude,
        depth_km,
        regexp_substr(place, 'of (.*)', 1, 1, 'i', 1) as nearest_municipality
    
    from convert_to_pacific
)

select * from cleaned