import logging

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, countDistinct

import config
from apis.elastic import push_data_to_elastic
from mappings.elastic import click_events

logging.basicConfig(level=logging.INFO)


def create_spark_session() -> SparkSession:
    return SparkSession.builder.appName("ClickStream").getOrCreate()


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

    df = df.groupby(["url", "country"]).agg(
        count("user_id").alias("all_clicks"),
        countDistinct("user_id").alias("unique_users"),
    )
    return df


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
