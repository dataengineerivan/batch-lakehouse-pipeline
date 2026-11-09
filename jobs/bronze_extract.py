"""
Bronze layer: copy new and changed rows from MySQL into append-only Delta tables.

Each run only pulls rows whose updated_at is at or after the newest updated_at already in bronze.
Bronze keeps every version it receives, so the full history of each record is preserved.
"""
import sys
from datetime import datetime
from delta.tables import DeltaTable
from pyspark.sql import functions as F
from common import get_spark, BRONZE, TABLES, MYSQL


def main(batch_id):
    spark = get_spark("bronze_extract")
    for table in TABLES:
        path = f"{BRONZE}/{table}"

        # find where the last run left off
        watermark = None
        if DeltaTable.isDeltaTable(spark, path):
            watermark = spark.read.format("delta").load(path).agg(F.max("updated_at")).first()[0]

        query = f"SELECT * FROM {table}"
        if watermark:
            # >= so nothing updated in the same second is missed; silver removes the repeats
            query += f" WHERE updated_at >= '{watermark:%Y-%m-%d %H:%M:%S}'"

        df = (
            spark.read.format("jdbc").options(**MYSQL).option("query", query).load()
            .withColumn("_ingested_at", F.current_timestamp())
            .withColumn("_batch_id", F.lit(batch_id))
        )
        rows = df.count()
        df.write.format("delta").mode("append").save(path)
        print(f"bronze.{table}: appended {rows:,} rows (watermark: {watermark or 'full load'})")
    spark.stop()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else datetime.utcnow().strftime("%Y%m%dT%H%M%S"))
