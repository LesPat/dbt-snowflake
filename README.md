Project description: a simple dbt data ingestion setup with Snowflake as a storage and processing

Project consists of two main folders: dbt model and data extractor running on Airflow ingesting data to Snowflake on a daily basis, dbt runs SQL model transformations saving the results back to Snowflake as a business-ready data.

dbt uses Snowflake connector to perform data transformation within the dbt model
