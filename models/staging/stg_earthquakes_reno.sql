select
    *,
    regexp_substr(place, 'of (.*)', 1, 1, 'i', 1) as nearest_municipality 

from {{ source('earthquakes', 'Reno') }}