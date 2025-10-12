from airflow import DAG
from airflow.operators import PythonOperator
from datetime import datetime, timedelta
import sys

#sys.path.append("/path/to/your/scripts")
from data_extraction import run_pipeline

default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes = 5),
}

with DAG(
    "covid_data_to_snowflake",
    default_args = default_args,
    description = "Daily COVID-19 data extraction and loading to Snowflake",
    schedule_interval = "@daily",
    start_date = datetime(2025, 10, 11),
    catchup = False,
    tags = ["covid", "snowflake", "etl"],
) as dag:

    extract_and_load = PythonOperator(
        task_id = "extract_and_load_to_snowflake",
        python_callable = run_pipeline
    )

    extract_and_load