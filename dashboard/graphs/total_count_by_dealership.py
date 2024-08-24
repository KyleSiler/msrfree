from plotly.graph_objs import Figure
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as fn
import plotly.express as px


def create_graph(df_all_dealerships: DataFrame, value=[]) -> Figure:
    query = df_all_dealerships
    if value:
        query = df_all_dealerships.filter(fn.col("s_trim").isin(value))
    df_counts_by_dealership = (
        query.groupBy("dealership", "date")
        .count()
        .sort("date", ascending=False)
        .toPandas()
    )
    return px.line(
        df_counts_by_dealership,
        x="date",
        y="count",
        color="dealership",
        markers=True,
        category_orders={
            "dealership": [
                "elkgrove",
                "folsom",
                "placerville",
                "roseville",
                "sacramento",
            ]
        },
        title="Total Units per Dealership",
    )
