from dash import Dash, html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from datetime import datetime

df = pd.read_csv("reports.csv")
fig1 = px.histogram(df, x='platform')
fig2 = px.histogram(df, x='flag-type', facet_col='platform')
fig3 = px.histogram(df, x='response-type', facet_col='platform')

app = Dash()
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        html.H1("Transparency Reporting Data Insights"),
        dag.AgGrid(
            id="reports-table",
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            columnSize="sizeToFit",
            defaultColDef={"filter": True},
            dashGridOptions={"pagination": True, "paginationPageSize":7},
        ),
        dcc.Graph(id='graph1', figure=fig1),
        dcc.Graph(id='graph2', figure=fig2),
        dcc.Graph(id='graph3', figure=fig3)
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
