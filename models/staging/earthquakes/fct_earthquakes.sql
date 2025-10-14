{{
    config(
        materialized='table'
    )
}}

select * from {{ ref('stg_earthquakes__losangeles') }}

union

select * from {{ ref('stg_earthquakes__portland') }}

union

select * from {{ ref('stg_earthquakes__reno') }}

union

select * from {{ ref('stg_earthquakes__sanfrancisco') }}

union

select * from {{ ref('stg_earthquakes__seattle') }}