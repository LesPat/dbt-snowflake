# dbt_covid_data

dbt project that transforms raw COVID-19 JSON ingested by the Airflow pipeline into structured, testable tables in Snowflake.

## Prerequisites

- dbt Core with the Snowflake adapter (included in the project `Dockerfile`)
- Raw data present in Snowflake at the source defined in `models/example/schema.yml`
- A valid `profiles.yml` for the `dbt_covid_data` profile

## Setup

1. Copy the example profile and edit connection settings:

   ```bash
   cp profiles.yml.example ~/.dbt/profiles.yml
   ```

2. Align the source definition with your Snowflake layout. Default source in `models/example/schema.yml`:

   ```yaml
   sources:
     - name: raw
       database: DBT_PROJECT_DB
       schema: RAW
       tables:
         - name: DBT_COVID_DATA_RAW
   ```

3. Verify the connection:

   ```bash
   dbt debug
   ```

## Commands

```bash
dbt run      # Build models (creates dbt_covid_model table)
dbt test     # Run column tests (unique, not_null on country)
dbt docs generate && dbt docs serve   # Generate and view lineage docs
```

### Docker

From the repository root:

```bash
docker compose exec dbt dbt debug
docker compose exec dbt dbt run
docker compose exec dbt dbt test
```

Place `profiles.yml` in this directory or mount it into the container before running commands.

## Models

### `dbt_covid_model`

Flattens the `VARIANT` JSON in `DBT_COVID_DATA_RAW` into one row per country.

```sql
SELECT
    f.value:country::STRING AS country,
    f.value:stats.population::INT AS population,
    f.value:stats.confirmed::INT AS confirmed_cases,
    ...
FROM {{ source('raw', 'DBT_COVID_DATA_RAW') }},
LATERAL FLATTEN(input => data) f
```

Materialized as a **table** (overrides the project default of `view` for the `example` folder).

### Tests

Defined in `models/example/schema.yml`:

- `country` — `unique`, `not_null`

## Project layout

```
dbt_covid_data/
├── dbt_project.yml       # Project name, profile, model paths
├── profiles.yml.example  # Snowflake connection template
├── models/
│   └── example/
│       ├── dbt_covid_model.sql
│       └── schema.yml
├── macros/               # (empty — add reusable SQL here)
├── seeds/                # (empty — add CSV seeds here)
├── snapshots/            # (empty — add SCD snapshots here)
├── tests/                # (empty — add custom data tests here)
└── analyses/             # (empty — add ad-hoc analyses here)
```

## Configuration reference

| Setting | Value |
|---------|-------|
| Project name | `dbt_covid_data` |
| Profile | `dbt_covid_data` |
| Default materialization (`models/example/`) | `view` (overridden to `table` in model) |

## Related documentation

See the [repository root README](../README.md) for the full pipeline architecture, Airflow setup, and end-to-end quick start.
