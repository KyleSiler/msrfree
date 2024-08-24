from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd

def create_graph() -> Figure :
    df = pd.DataFrame({
    'Month': [1,2,3,4,5,6,7,8,9,10,11,12], 
    '2020': [4956, 6416, 3886, 3522, 7827, 8219, 7771, 6908, 7484, 6933, 5695, 7924],
    '2021': [6023, 6023, 6776, 10117, 9728, 10117, 7652, 7369, 7652, 6085, 6085, 6085],
    '2022': [5732, 5732, 6448, 7124, 6860, 6860, 7080, 7352, 7080, 5862, 5628, 6097],
    '2023': [4465, 4287, 4823, 4643, 4465, 4643, 4552, 4916, 4734, 4493, 4493, 4673],
    '2024': [4273, 4273, 4444, 3496, 3496, 3496, 0, 0, 0, 0, 0, 0]})

    dfl = pd.melt(df, ['Month'], var_name='Year', value_name='Units')

    return px.line(
        dfl,
        x = 'Month',
        y = 'Units',
        color = 'Year',
        title="Sales by Quarter"
    )
