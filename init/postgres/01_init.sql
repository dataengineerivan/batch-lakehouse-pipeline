-- Separate database for Airflow's own metadata
CREATE DATABASE airflow;

-- Warehouse schemas: raw = silver tables loaded by Spark, dbt builds staging and marts
\connect warehouse
CREATE SCHEMA IF NOT EXISTS raw;
