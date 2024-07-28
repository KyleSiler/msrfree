from plotly.graph_objs import Figure
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as fn
import plotly.express as px


def create_graph(df_all_dealerships: DataFrame, value=[]) -> Figure:
    query = df_all_dealerships
    if value:
        query = df_all_dealerships.filter(fn.col("s_trim").isin(value))
    df_box_by_trim = (
        query.filter(fn.col("date") == fn.current_date())
        .groupBy("s_trim")
        .count()
        .toPandas()
    )
    return px.pie(
        df_box_by_trim,
        values="count",
        names="s_trim",
        title="Trims",
    )
