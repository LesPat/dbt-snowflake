import requests
import json
from datetime import datetime
import snowflake.connector

#Public API data extaction config (data availavle under https://disease.sh/ link)
API_URL = "https://disease.sh/v3/covid-19/countries"

#Snowflake config - my Snowflake credentials and RAW data database
SNOWFLAKE_CONFIG = {
    "user": "***",
    "password": "***",
    "account": "***",
    "warehouse": "***",
    "database": "***",
    "schema": "***",
}
TABLE_NAME = "dbt_covid_data_raw"
OUTPUT_FILE = f"/tmp/covid_data_{datetime.now().strftime('%Y%m%d')}.json"

#Data fetching from diesese.sh API appended to json file country by country
def extract_data():
    print("Fetching data from API...")
    resp = requests.get(API_URL)
    resp.raise_for_status()
    data = resp.json()

    cleaned = []
    for country in data:
        cleaned.append({
            "country": country.get("country"),
            "stats": {
                "confirmed": country.get("cases"),
                "deaths": country.get("deaths"),
                "recovered": country.get("recovered"),
                "tests": country.get("tests"),
                "population": country.get("population")
            },
            "vaccination": {
                #Estimating bought doeses by country multiplied by average population coverage (~80%)
                "total_doses": country.get("population") * 2 * 0.8 if country.get("population") else None,
                "people_vaccinated": country.get("active"),
                "people_fully_vaccinated": country.get("critical")
            }
        })
    #Writing data to json
    with open(OUTPUT_FILE, "w") as f:
        json.dump(cleaned, f, indent=2)
    print(f"Data saved to {OUTPUT_FILE}")
    return OUTPUT_FILE

#Loading data into Snowflake using snowflake.connector and given credentials
def load_to_snowflake(file_path):
    print("Connecting to Snowflake...")
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cur = conn.cursor()

    #Series of queries run on snowflake connector on given database and schema
    cur.execute(f"""
        CREATE OR REPLACE TABLE {TABLE_NAME} (data VARIANT);
    """)
    print("Uploading file to Snowflake stage...")

    cur.execute("CREATE OR REPLACE STAGE covid_stage;")
    cur.execute(f"PUT file://{file_path} @covid_stage AUTO_COMPRESS=FALSE;")

    cur.execute(f"""
        COPY INTO {TABLE_NAME}
        FROM @covid_stage/{file_path.split('/')[-1]}
        FILE_FORMAT = (TYPE = 'JSON');
    """)
    print("Data loaded into Snowflake table")

    cur.close()
    conn.close()

#Main pipeline executed by airflow scheduler
def run_pipeline():
    file_path = extract_data()
    load_to_snowflake(file_path)

if __name__ == "__main__":
    run_pipeline()