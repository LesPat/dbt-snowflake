Project description: a simple dbt data ingestion setup with Snowflake as a storage and processing

Project consists of two main folders: dbt model and data extractor running on Airflow daily ingesting data to Snowflake, dbt then runs model with SQL transformations saving the results back to Snowflake as business-data ready table
