from plotly.graph_objs import Figure
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as fn
import plotly.express as px


def create_graph(df_all_dealerships: DataFrame, value=[]) -> Figure:
    query = df_all_dealerships
    if value:
        query = df_all_dealerships.filter(fn.col("s_trim").isin(value))
    df_box_by_trim = query.toPandas()
    return px.box(
        df_box_by_trim,
        x="s_trim",
        y="final_price",
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
        title="Box Price by Trim",
    )
