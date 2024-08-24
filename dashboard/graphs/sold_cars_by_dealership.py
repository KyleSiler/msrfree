from plotly.graph_objs import Figure
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as fn
import plotly.express as px


def create_graph(df_all_dealerships: DataFrame, value=[]) -> Figure:
    query = df_all_dealerships
    if value:
        query = df_all_dealerships.filter(fn.col("s_trim").isin(value))

    df_counts_by_dealership = (
        query.groupBy("vin", "dealership")
        .agg(fn.max("date").alias("last_seen"))
        .filter(fn.col("last_seen") < fn.current_date())
        .groupBy("dealership", "last_seen")
        .count()
        .toPandas()
    )
    return px.bar(
        df_counts_by_dealership,
        x="last_seen",
        y="count",
        color="dealership",
        category_orders={
            "dealership": [
                "elkgrove",
                "folsom",
                "placerville",
                "roseville",
                "sacramento",
            ]
        },
        title="Total Units Sold per Dealership",
    )
