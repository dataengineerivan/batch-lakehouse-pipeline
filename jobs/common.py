"""Shared settings and the Spark session used by every PySpark job."""
import os
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

LAKEHOUSE = os.environ.get("LAKEHOUSE_PATH", "/opt/lakehouse")
BRONZE = f"{LAKEHOUSE}/bronze"
SILVER = f"{LAKEHOUSE}/silver"

# source table -> its primary key
TABLES = {"customers": "customer_id", "orders": "order_id"}

MYSQL = {
    "url": f"jdbc:mysql://{os.environ.get('MYSQL_HOST', 'mysql')}:3306/{os.environ['MYSQL_DATABASE']}",
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"],
    "driver": "com.mysql.cj.jdbc.Driver",
}

POSTGRES = {
    "url": f"jdbc:postgresql://{os.environ.get('POSTGRES_HOST', 'postgres')}:5432/{os.environ['POSTGRES_DB']}",
    "user": os.environ["POSTGRES_USER"],
    "password": os.environ["POSTGRES_PASSWORD"],
    "driver": "org.postgresql.Driver",
}


def get_spark(app_name):
    builder = (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.driver.memory", "2g")
        .config("spark.jars.ivy", "/home/airflow/.ivy2")
    )
    # Delta Lake plus the MySQL and Postgres JDBC drivers, downloaded on first run
    spark = configure_spark_with_delta_pip(
        builder,
        extra_packages=["com.mysql:mysql-connector-j:8.4.0", "org.postgresql:postgresql:42.7.4"],
    ).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
