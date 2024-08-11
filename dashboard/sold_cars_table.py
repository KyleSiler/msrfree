from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as fn
from pandas import DataFrame as PandaFrame


def create_table(df_all_dealerships: DataFrame, value=[]) -> PandaFrame:
    query = df_all_dealerships
    if value:
        query = df_all_dealerships.filter(fn.col("s_trim").isin(value))

    return (
        query.groupBy("vin", "dealership", "s_trim")
        .agg(fn.max("date").alias("last_seen"))
        .filter(fn.col("last_seen") < fn.current_date())
        .sort("last_seen", ascending=False)
        .select("last_seen", "vin", "dealership", "s_trim")
        .toPandas()
    )
