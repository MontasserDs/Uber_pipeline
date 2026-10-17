from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, when, from_json
from pyspark.sql.types import *

def create_spark_session():
    spark = SparkSession.builder \
        .appName("UberPipeline") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def get_schema():
    return StructType([
        StructField("trip_id", StringType(), True),
        StructField("driver_name", StringType(), True),
        StructField("passenger_name", StringType(), True),
        StructField("pickup_zone", StringType(), True),
        StructField("dropoff_zone", StringType(), True),
        StructField("pickup_lat", DoubleType(), True),
        StructField("pickup_lon", DoubleType(), True),
        StructField("dropoff_lat", DoubleType(), True),
        StructField("dropoff_lon", DoubleType(), True),
        StructField("distance_km", DoubleType(), True),
        StructField("duration_min", IntegerType(), True),
        StructField("price_mad", DoubleType(), True),
        StructField("surge_multiplier", DoubleType(), True),
        StructField("status", StringType(), True),
        StructField("timestamp", StringType(), True)
    ])

def transform(df):
    return df \
        .withColumn("price_mad", round(col("price_mad"), 2)) \
        .withColumn("trip_category",
            when(col("distance_km") < 5, "short")
            .when(col("distance_km") < 15, "medium")
            .otherwise("long")
        ) \
        .withColumn("is_surge", col("surge_multiplier") > 1.0)

if __name__ == "__main__":
    spark = create_spark_session()
    print("Session Spark créée!")

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "uber_trips") \
        .load()

    schema = get_schema()

    df_parsed = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    df_transformed = transform(df_parsed)

    query = df_transformed.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()