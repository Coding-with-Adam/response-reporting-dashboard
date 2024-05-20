from dash import Dash, html, dcc, callback, Output, Input, State, register_page
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.app_queries import select_all_reports

register_page(__name__)

#___________________________________________Layout Items___________________________________________#

grid = dag.AgGrid(
            id = "id_insights_report_table",
            columnSize = "responsiveSizeToFit",
            defaultColDef = {"filter": True, "resizable": True},
            dashGridOptions = {"pagination": True, "paginationPageSize":7},
        )

tabs_container = dbc.Container([
    dbc.Tabs([
        dbc.Tab([
            grid
            ],
            label = "Report Table"),
        dbc.Tab([
            dbc.Row([
                dbc.Col(dcc.Graph(id ="id_graph_all_reports")),
                ],
                ),
            dbc.Row([
                dbc.Col(dcc.Graph(id = "id_graph_decisions")),
                ],
                ),
            dbc.Row([
                dbc.Col(dcc.Graph(id = "id_graph_reports_types")),
                ])
            ],
            label = "Theme 1"
            ),
        dbc.Tab([
            ],
            label = "Theme 2"
            ),
        dbc.Tab([
            ],
            label = "Theme 3"
            )
        ],
        id = "id_tabs_container")
    ]
    )

refresh_data_button = dbc.Button(
    "Refresh",
    id = "id_refresh_data_button",
    color = "success",
    className = "mt-2",
    )

#_____________________________________________The Layout_____________________________________________#

layout = dbc.Container([
    dbc.Row(dbc.Col("Controls here")),
    html.Hr(),
    dbc.Row(tabs_container),
    refresh_data_button,
    ],
    id = "id_insights_layout",
    fluid = True
)

#______________________________________________Callbacks______________________________________________#

@callback(
    Output("id_insights_report_table", "rowData"),
    Output("id_insights_report_table", "columnDefs"),
    Input("id_refresh_data_button", "n_clicks"),
    #Do not prevent initial call
    )
def refresh_grid_data(refresh_button_click):
    """Data is refreshed both when the page loads(everytime) and when the resfresh button is clicked"""
    df = select_all_reports()
    col_defs = [{"field": i} for i in df.columns]
    data_dict = df.to_dict("records")
    return data_dict, col_defs

@callback(
    Output("id_graph_all_reports", "figure"),
    Output("id_graph_decisions", "figure"),
    Output("id_graph_reports_types", "figure"),
    Input("id_insights_report_table", "rowData"),
    )
def update_graphs(insights_data):
    df = pd.DataFrame(insights_data)
    reports_by_platform = px.histogram(df, x = 'platform')
    report_types = px.histogram(df, x = 'report_type', facet_col = 'platform')
    decisions = px.histogram(df, x = 'platform_decision', facet_col = 'platform')
    return reports_by_platform, report_types, decisions