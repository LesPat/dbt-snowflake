{{ config(materialized='table') }}

SELECT
    f.value:country::STRING AS country,
    f.value:stats.population::INT AS population,
    f.value:stats.confirmed::INT AS confirmed_cases,
    f.value:stats.deaths::INT AS deaths,
    f.value:stats.recovered::INT AS recovered,
    f.value:vaccination.people_vaccinated::INT AS vaccinated_people
FROM {{ source('raw', 'DBT_COVID_DATA_RAW') }},
LATERAL FLATTEN(input => data) f