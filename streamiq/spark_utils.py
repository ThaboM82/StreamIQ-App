# streamiq/spark_utils.py
from pyspark.sql import SparkSession

def get_spark(app_name: str = "StreamIQDemo"):
    """
    Initialize or return an existing Spark session.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .getOrCreate()
    return spark
