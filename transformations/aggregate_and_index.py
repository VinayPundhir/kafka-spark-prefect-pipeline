from pyspark.sql import SparkSession
from pyspark.sql.functions import count,countDistinct
from apis.elastic import push_data_to_elastic
from mappings.elastic import click_events
import config
import logging

logging.basicConfig(level=logging.INFO)


def read_db_as_df():
    spark = SparkSession.builder.appName("SQLiteRead").getOrCreate()
    JDBC_URL = f"jdbc:sqlite:{config.DB_PATH}/{config.DB_NAME}"

    jdbc_properties = {
        "driver": "org.sqlite.JDBC",
        "url": JDBC_URL,
        "dbtable": config.TABLE,
    }
    df = spark.read.format("jdbc").options(**jdbc_properties).load()
    return spark, df


def transform(spark,df):

    logging.info("Aggregating data")

    df = df.groupby(["url", "country"]).agg(
        count("user_id").alias("all_clicks"),
        countDistinct("user_id").alias("unique_users")
    )

    logging.info("Pushing data")

    push_data_to_elastic(
        data=df.toPandas().to_dict(orient='records'),
        index_name="click_events",
        mapping=click_events.mapping)
    spark.stop()


def main():
    transform(*read_db_as_df())


if __name__=="__main__":
    main()

