from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as fn
from pandas import DataFrame as PandaFrame


def create_table(df_all_dealerships: DataFrame, value=[]) -> PandaFrame:
    query = df_all_dealerships
    if value:
        query = df_all_dealerships.filter(fn.col("s_trim").isin(value))

    last_seen = (
        query.groupBy("vin", "dealership")
        .agg(fn.max("date").alias("last_seen"))
        .filter(fn.col("last_seen") < fn.current_date())
        .select("vin", fn.col("last_seen").alias("date"))
    )
    return (
        query.join(last_seen, ["vin", "date"], "inner")
        .sort("date", ascending=False)
        .select("date", "vin", "dealership", "s_trim", "final_price")
        .toPandas()
    )
