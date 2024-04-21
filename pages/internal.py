from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update, register_page
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
from utils.app_queries import select_user_reports
from utils.app_queries import select_all_platforms
from utils.app_queries import select_reports_types

register_page(__name__)

platforms = select_all_platforms()
reports_types = select_reports_types()
decisions = ["Demoted", "Removed", "No Action"]

#_________________________________________Columns definition_________________________________________#

cols = [
    {
        "headerName": "Report Date",
        "field": "timestamp",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor'
    },
    {
        "headerName": "Platform",
        "field": "platform",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": platforms["platform_name"].values}
    },
    {
        "headerName": "Content URL",
        "field": "url",
    },
    {
        "headerName": "Report Type",
        "field": "report_type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": reports_types["report_type"].values}
    },
    {
        "headerName" : "Screenshot URL",
        "field" : "screenshot_url"
    },
    {
        "headerName": "Answer Date",
        "field": "answer_date",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {
            'min': '2023-01-01',
        }
    },
    {
        "headerName": "Platform Decision",
        "field": "platform_decision",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": decisions}
    },
    {
        "headerName": "Policy",
        "field": "policy",
    },
    {
    "headerName" : "Appeal",
    "field" : "appeal",
    "cellEditor" : "agSelectCellEditor",
    "cellEditorParams" : {"values" : ["Yes", "No"]}
    }
]

#____________________________________________Layout items____________________________________________#

grid = dag.AgGrid(
    id = "id_internal_reports_table",
    columnDefs = cols,
    rowData = [],
    columnSize = "sizeToFit",
    defaultColDef = {"editable": True, "filter": True},
    dashGridOptions = {
    "pagination": True,
    "paginationPageSize": 7,
    "undoRedoCellEditing": True,
    "rowSelection": "multiple"
    }
    )

delete_record = dbc.Button(
    id = "id_delete_report_button",
    children = "Delete Row",
    color = "danger",
    class_name = "me-1 mt-1",
    )

update_recod = dbc.Button(
    id = "id_update_report_button",
    children = "Update Row",
    color = "secondary",
    class_name = "me-1 mt-1",
    )

add_record = dbc.Button(
    id = "id_add_report_button",
    children = "New Report",
    color = "primary",
    class_name = "me-1 mt-1",
    )

#_______________________________________Layout Protection Setup_______________________________________#

protected_container = dbc.Container([
        html.H1("Internal", style = {"text-align":"center"}),
        dmc.Center(html.H4("Update existing report or insert a new report.")),
        dbc.Row([grid]),
        dbc.Row([
            dbc.Col([delete_record, update_recod, add_record]),
            ]
            )
    ],
    fluid = True
)


unprotected_container = dbc.Container([
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H1("Permission denied. Contact an admnistrator.")
            ],
            style = {"text-align":"center"})
        ]),
    html.Hr(),
    ],
    fluid = True
    )

#_________________________________________The actual Layout_________________________________________#

layout = dbc.Container([
    ],
    id = "id_internal_page_layout",
    fluid = True
    )

#______________________________________________Callbacks______________________________________________#

@callback(
    Output("id_internal_page_layout", "children"),
    Input("id_session_data", "data")
    ) #Do not prevent initial call
def layout_security(session_data):
    authenticated = session_data.get("is_authenticated", False)
    if authenticated:
        return protected_container
    return unprotected_container

@callback(
    Output("id_internal_reports_table", "rowData"),
    Input("id_session_data", "data")
    )
def get_reports_for_this_user(user_data):
    email = user_data.get("email", "")
    df = select_user_reports(email)
    grid_row_data = df.to_dict("records")
    return grid_row_data

@callback(
    Output("reports-table", "deleteSelectedRows"),
    Output("reports-table", "rowData"),
    Input("id_delete_report_button", "n_clicks"),
    Input("id_add_report_button", "n_clicks"),
    State("reports-table", "rowData"),
    prevent_initial_call = True,
)
def update_table(n_dlt, n_add, data):
    if ctx.triggered_id == "id_add_report_button":
        new_row = {
            "timestamp" : [""],
            "reporting_user" : [""],
            "platform" : [""],
            "url" : [""],
            "report_type" : [""],
            "screenshot_url" : [""],
            "answer_date" : [""],
            "platform_decision" : [""],
            "policy" : [""],
            "appeal" : [""]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat(
            [pd.DataFrame(data), df_new_row]
        )  # add new row to orginal dataframe
        return False, updated_table.to_dict("records")

    elif ctx.triggered_id == "id_delete_report_button":
        return True, no_update
