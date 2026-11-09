"""Daily batch pipeline: source activity -> bronze -> silver -> dbt gold marts."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"retries": 1, "retry_delay": timedelta(minutes=2)}

with DAG(
    dag_id="batch_lakehouse_pipeline",
    description="MySQL to Delta Lake bronze/silver, then dbt gold marts in Postgres",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["spark", "delta", "dbt"],
) as dag:

    simulate_source = BashOperator(
        task_id="simulate_source_activity",
        bash_command="python /opt/scripts/generate_orders.py",
    )

    bronze_extract = BashOperator(
        task_id="spark_bronze_extract",
        bash_command="cd /opt/jobs && python bronze_extract.py {{ ts_nodash }}",
    )

    silver_transform = BashOperator(
        task_id="spark_silver_transform",
        bash_command="cd /opt/jobs && python silver_transform.py",
    )

    # dbt build runs every model and every test in dependency order
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/dbt && /home/airflow/dbt-venv/bin/dbt build",
    )

    simulate_source >> bronze_extract >> silver_transform >> dbt_build
