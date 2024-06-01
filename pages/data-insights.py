from dash import Dash, html, dcc, callback, Output, Input, State, register_page, exceptions
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.app_queries import select_all_reports

register_page(__name__)

#____________________________________________Utilities____________________________________________#

def standard_figure_config(figure):
    figure.update_layout(
        template = "plotly_white",
        #paper_bgcolor = "rgba(0, 0, 0, 0)",
        #plot_bgcolor = "rgba(0, 0, 0, 0)",
        margin = {"t":0, "b":0, "l":0, "r":0}
        )
    return figure


#___________________________________________Layout Items___________________________________________#

controls = dbc.Row([
    ])

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
                dbc.Col(dcc.Graph(id ="id_graph_all_reports", style = {"height":"35vh"})),
                ],
                ),
            dbc.Row([
                dbc.Col(dcc.Graph(id = "id_graph_decisions", style = {"height":"30vh"}), width = 6),
                dbc.Col(dcc.Graph(id = "id_graph_reports_types", style = {"height":"30vh"}), width = 6),
                ],
                #className = "bg-white"
                ),
            ],
            label = "Reports Accros Platforms"
            ),
        dbc.Tab([
            ],
            label = "Reports Over Time"
            ),
        dbc.Tab([
            ],
            label = "Theme 3"
            )
        ],
        id = "id_tabs_container")
    ],
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
    fluid = True,
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
    try:
        df = select_all_reports()
        col_defs = [{"field": i} for i in df.columns]
        data_dict = df.to_dict("records")
    except Exception as e:
        return [], []
    return data_dict, col_defs

@callback(
    Output("id_graph_all_reports", "figure"),
    Output("id_graph_decisions", "figure"),
    Output("id_graph_reports_types", "figure"),
    Input("id_insights_report_table", "rowData"),
    )
def update_graphs(insights_data):
    try:
        df = pd.DataFrame(insights_data)
        fig_1 = px.histogram(df, x = 'platform')
        fig_2 = px.histogram(df, x = 'report_type')
        fig_3 = px.histogram(df, x = 'platform_decision')
    except Exception as e:
        raise exceptions.PreventUpdate
    return standard_figure_config(fig_1), standard_figure_config(fig_2), standard_figure_config(fig_3)