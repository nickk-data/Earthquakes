Pacific Coast Seismic Analysis

Project Overview

This project is a personal data engineering pipeline and dbt transformation of historical earthquake data across five major Pacific Coast metropolitan areas. The goal was to consolidate raw data from the USGS API into a clean, unified fact table optimized for analytical consumption, addressing specific timezone and location formatting requirements for a hypothetical analyst.

✨ Key Features

    Automated Data Collection: Initial historical data for Reno, NV, was collected weekly via an automated Python script and persisted to a local PostgreSQL database.

    Targeted Data Acquisition: One-time batch pulls were executed for Los Angeles, San Francisco, Portland, OR, and Seattle, WA, covering the same historical time frame as the Reno data.

    Cloud Data Migration: All raw data was successfully migrated from PostgreSQL into Snowflake for centralized processing.

    dbt Data Transformation: A dbt project was used to clean, standardize, and model the data.

    Timezone Localization: UTC timestamps were converted to Pacific Time (12-hour format) to improve usability for analysts focused on this region.

    Feature Engineering: The nearest major municipality was extracted from the raw location field to create a cleaner, more intuitive dimension for analysis.

    Unified Fact Table: All five regional datasets were combined into a single, analysis-ready fact table.

🛠️ Technology Stack

Category	Tool / Service	Purpose
Data Source	USGS Earthquake API	Source of raw seismic data.
Initial Storage	PostgreSQL	Local database for initial automated data ingestion (Reno, NV).
Data Migration	Python (psycopg2, snowflake-connector-python)	Scripts for API interaction and migrating data to the cloud.
Cloud Data Warehouse	Snowflake	Target data platform for all raw and transformed data.
Transformation (ETL/ELT)	dbt (data build tool)	Data cleaning, modeling, and business logic application.
Orchestration	Windows Task Scheduler (or equivalent)	Automated execution of the weekly Reno data pull script.

🏗️ Data Pipeline & Architecture

1. Ingestion (Python & PostgreSQL)

Location	Method	Details
Reno, NV	Automated Incremental	A Python script queried the USGS API for earthquakes within a 100km radius, saving weekly results to a local PostgreSQL database.
LA, SF, Portland, Seattle	Batch One-Time	Separate Python scripts performed a one-time pull for the same historical time range, based on a defined geographic boundary (e.g., a city radius).

2. Migration to Cloud

All data from the local PostgreSQL database and the new batch pulls were staged into dedicated raw schemas within Snowflake.

3. Transformation (dbt)

The dbt project executed the following primary transformations:
dbt Model / Step	Description
Cleaning & Formatting	Applied SQL logic to clean the raw data (e.g., removing nulls, correcting data types).
Time Standardization	Converted the raw time column from UTC 24-Hour format to a user-friendly Pacific Time 12-Hour format.
Location Extraction	Used string manipulation logic to extract the nearest major Municipality from the raw place field.
Fact Table Creation	A final model used a UNION to merge the 5 cleaned regional datasets into a single fact table: fact_earthquake_events.

Final Fact Table Schema (fact_earthquake_events)

Field Name	Description	Source / Transformation
earthquake_date	Date of the seismic event.	Extracted from the API timestamp.
earthquake_time	Time of the event (12-hour Pacific).	Converted from UTC 24-hr to Pacific 12-hr.
magnitude	Richter magnitude of the event.	Raw API data.
depth_km	Depth of the event in kilometers.	Raw API data.
nearest_municipality	Major city associated with the event.	Extracted from the raw place field.
