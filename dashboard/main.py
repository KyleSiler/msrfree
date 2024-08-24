from dash import Dash, html, dcc, callback, Output, Input, dash_table
import graphs.data_ingest as data_ingest
import graphs.total_count_by_dealership as tcbd
import graphs.box_price_by_trim as bpbt
import graphs.pie_distribution_by_trim as pdbt
import graphs.pie_distribution_by_color as pdbc
import graphs.sold_cars_by_dealership as scbd
import graphs.sold_cars_table as sct
import graphs.total_discounts_mojave as tdm
import graphs.sales_by_quarter as sbq

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
                figure=tdm.create_graph(data.df_all_dealerships),
                id="total-discounts-mojave",
            ),
            dash_table.DataTable(
                tdm.create_table(data.df_all_dealerships).to_dict("records"),
                id="total-discounts-mojave-table",
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
    html.Div(
        [
            dcc.Graph(
                figure=sbq.create_graph()
            )
        ]
    )
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
