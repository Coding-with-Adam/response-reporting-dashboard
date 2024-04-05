from dash import Dash, html, dcc, callback, Output, Input, State, register_page
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from datetime import datetime

register_page(__name__)

df = pd.read_csv("assets/reports.csv")
fig1 = px.histogram(df, x='platform')
fig2 = px.histogram(df, x='flag-type', facet_col='platform')
fig3 = px.histogram(df, x='response-type', facet_col='platform')

grid = dag.AgGrid(
            id = "reports-table",
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            columnSize="sizeToFit",
            defaultColDef={"filter": True},
            dashGridOptions={"pagination": True, "paginationPageSize":7},
        )

tabs_container = dbc.Container([
    dbc.Tabs([
        dbc.Tab([
            grid
            ],
            label = 'Report Table'),
        dbc.Tab([
            dcc.Graph(id='graph1', figure=fig1),
            ],
            label = 'Report Count by Platform'
            ),
        dbc.Tab([
            dcc.Graph(id='graph2', figure=fig2),
            ],
            label = 'Flag Types'
            ),
        dbc.Tab([
            dcc.Graph(id='graph3', figure=fig3)
            ],
            label = 'Response Type'
            )
        ],
        id = 'all_tabs')
    ])

layout = dbc.Container([
        dbc.Row([html.H1("Data Insights", style = {"text-align":"center"})]),
        dbc.Row(tabs_container)
    ],
    fluid = True
)
