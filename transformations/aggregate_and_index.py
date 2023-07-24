import logging

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, count, countDistinct, expr,
                                   from_unixtime, unix_timestamp, when)

import config
from apis.elastic import push_data_to_elastic
from mappings.elastic import click_events

logging.basicConfig(level=logging.INFO)


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder.appName("ClickStream")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def read_db_as_df(spark: SparkSession) -> pyspark.sql.DataFrame:
    JDBC_URL = f"jdbc:sqlite:{config.DB_PATH}/{config.DB_NAME}"

    jdbc_properties = {
        "driver": "org.sqlite.JDBC",
        "url": JDBC_URL,
        "dbtable": config.TABLE,
    }
    df = spark.read.format("jdbc").options(**jdbc_properties).load()
    return df


def transform(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    logging.info("Aggregating data :::")

    # Convert the "timestamp" column to a timestamp data type
    df = df.withColumn(
        "timestamp", from_unixtime(unix_timestamp("timestamp", "yyyy-MM-dd'T'HH:mm:ss"))
    )

    # Calculate the timestamp_sec separately
    df = df.withColumn("timestamp_sec", unix_timestamp("timestamp"))

    # Calculate the time spent on each URL for each country by finding the difference
    # between the maximum and minimum timestamps
    time_spent_df = df.groupBy("url", "country").agg(
        countDistinct("user_id").alias("unique_users"),
        count("user_id").alias("clicks"),
        (expr("MAX(timestamp_sec)") - expr("MIN(timestamp_sec)")).alias(
            "time_spent_sec"
        ),
    )

    # Calculate the average time spent for each URL and country, handling the divide-by-zero scenarios
    average_time_df = time_spent_df.withColumn(
        "average_time",
        when(col("unique_users") == 0, "00:00:00").otherwise(
            expr("time_spent_sec / unique_users").cast("integer")
        ),
    ).select(
        "url",
        "country",
        "clicks",
        "unique_users",
        expr("from_unixtime(average_time, 'HH:mm:ss')").alias("average_time"),
    )

    return average_time_df


def push_to_elastic(df: pyspark.sql.DataFrame):
    """function to push spark df to elastic"""
    logging.info("Pushing data :::")
    push_data_to_elastic(
        data=df.toPandas().to_dict(orient="records"),
        index_name="click_events",
        mapping=click_events.mapping,
    )


def main():
    spark = create_spark_session()
    df = read_db_as_df(spark)
    df = transform(df)
    push_to_elastic(df)
    spark.stop()


if __name__ == "__main__":
    main()
