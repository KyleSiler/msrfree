from dash import Dash, html, dcc, callback, Output, Input, dash_table
import data_ingest
import total_count_by_dealership as tcbd
import box_price_by_trim as bpbt
import pie_distribution_by_trim as pdbt
import pie_distribution_by_color as pdbc
import sold_cars_by_dealership as scbd
import sold_cars_table as sct

app = Dash()

data = data_ingest.DataIngest()

app.layout = [
    html.Div("Jeep Gladiator"),
    html.Hr(),
    dcc.Checklist(
        ["RUBICON", "MOJAVE", "WILLYS", "SPORT", "NIGHTHAWK"],
        ["RUBICON", "MOJAVE", "WILLYS", "SPORT", "NIGHTHAWK"],
        id="total-count-checklist",
    ),
    html.Div(
        [
            dcc.Graph(
                figure=tcbd.create_graph(data.df_all_dealerships),
                id="total-count-graph",
            ),
            dcc.Graph(
                figure=bpbt.create_graph(data.df_all_dealerships),
                id="box-price-by-trim-graph",
            ),
        ],
        style={"display": "flex", "flexDirection": "row"},
    ),
    html.Div(
        [
            dcc.Graph(
                figure=scbd.create_graph(data.df_all_dealerships),
                id="sold-cars-by-dealership",
            ),
            dash_table.DataTable(
                sct.create_table(
                    data.df_all_dealerships,
                ).to_dict("records"),
                id="sold-cars-table",
            ),
        ],
        style={"display": "flex", "flexDirection": "row"},
    ),
    html.Div(
        [
            dcc.Graph(
                figure=pdbt.create_graph(data.df_all_dealerships),
                id="pie-distribution-by-trim",
            ),
            dcc.Graph(
                figure=pdbc.create_graph(data.df_all_dealerships),
                id="pie-distribution-by-color",
            ),
        ],
        style={"display": "flex", "flexDirection": "row"},
    ),
]


@callback(
    Output("total-count-graph", "figure"), Input("total-count-checklist", "value")
)
def update_total_count_graph(value):
    return tcbd.create_graph(data.df_all_dealerships, value)


@callback(
    Output("box-price-by-trim-graph", "figure"), Input("total-count-checklist", "value")
)
def update_box_price_by_trim_graph(value):
    return bpbt.create_graph(data.df_all_dealerships, value)


@callback(
    Output("pie-distribution-by-color", "figure"),
    Input("total-count-checklist", "value"),
)
def update_pie_distribution_by_color_graph(value):
    return pdbc.create_graph(data.df_all_dealerships, value)


@callback(
    Output("sold-cars-by-dealership", "figure"), Input("total-count-checklist", "value")
)
def update_sold_cars_by_dealership(value):
    return scbd.create_graph(data.df_all_dealerships, value)


@callback(Output("sold-cars-table", "data"), Input("total-count-checklist", "value"))
def update_sold_cars_table(value):
    return sct.create_table(data.df_all_dealerships, value).to_dict("records")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
