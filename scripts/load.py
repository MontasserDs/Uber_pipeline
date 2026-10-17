from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, when, from_json
from pyspark.sql.types import *

def create_spark_session():
    spark = SparkSession.builder \
        .appName("UberLoad") \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                "org.postgresql:postgresql:42.6.0") \
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

def write_to_postgres(df, epoch_id):
    """Écrit chaque batch dans PostgreSQL"""
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/uber_pipeline") \
        .option("dbtable", "trips") \
        .option("user", "postgres") \
        .option("password", "Montasser2001") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    print(f"Batch {epoch_id} chargé dans PostgreSQL!")

if __name__ == "__main__":
    spark = create_spark_session()
    print("Session Spark créée!")

    # Lire depuis Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "uber_trips") \
        .load()

    # Parser et transformer
    schema = get_schema()
    df_parsed = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    df_transformed = df_parsed \
        .withColumn("price_mad", round(col("price_mad"), 2)) \
        .withColumn("trip_category",
            when(col("distance_km") < 5, "short")
            .when(col("distance_km") < 15, "medium")
            .otherwise("long")
        ) \
        .withColumn("is_surge", col("surge_multiplier") > 1.0)

    # Charger dans PostgreSQL
    query = df_transformed.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .start()

    query.awaitTermination()