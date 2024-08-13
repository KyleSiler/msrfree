from plotly.graph_objs import Figure
from pyspark.sql.dataframe import DataFrame
import plotly.express as px
from pandas import DataFrame as PandaFrame
from pyspark.sql import functions as fn


def create_graph(df_all_dealerships: DataFrame) -> Figure:
    query = df_all_dealerships
    df_counts_by_dealership = (
        query.filter("s_trim = 'MOJAVE'")
        .filter("retail_price > 65000")
        .sort("date", ascending=False)
        .toPandas()
    )
    return px.line(
        df_counts_by_dealership,
        x="date",
        y="final_price",
        color="vin",
        markers=True,
        title="Total Discounts Mojave",
    )


def create_table(df_all_dealerships: DataFrame) -> PandaFrame:
    query = df_all_dealerships
    return (
        query.filter("s_trim = 'MOJAVE'")
        .filter("retail_price > 65000")
        .filter(fn.col("date") == fn.current_date())
        .sort("final_price", ascending=False)
        .toPandas()
    )
