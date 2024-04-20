from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update, register_page
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd

register_page(__name__)

df = pd.read_csv("assets/reports.csv")
df["answer_date"] = pd.to_datetime(df["answer_date"]).dt.strftime('%Y-%m-%d')
df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime('%Y-%m-%d')

#_________________________________________Columns definition_________________________________________#

cols = [
    {
        "headerName": "Report Date",
        "field": "timestamp",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor'
    },
    {
        "headerName": "Reporting User",
        "field": "reporting_user"
    },
    {
        "headerName": "Platform",
        "field": "platform",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["platform"].unique()}
    },
    {
        "headerName": "Content URL",
        "field": "url",
    },
    {
        "headerName": "Report Type",
        "field": "report_type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["report_type"].unique()}
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
            'min': '2024-01-01',
        }
    },
    {
        "headerName": "Platform Decision",
        "field": "platform_decision",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["platform_decision"].unique()}
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

#_______________________________________Layout Protection Setup_______________________________________#

protected_container = dbc.Container([
        html.H1("Internal", style = {"text-align":"center"}),
        dmc.Center(html.H4("Update existing report or insert a new report.")),
        dag.AgGrid(
            id="reports-table",
            rowData=df.to_dict("records"),
            columnDefs = cols,
            columnSize = "sizeToFit",
            defaultColDef = {"editable": True, "filter": True},
            dashGridOptions = {"pagination": True,
                             "paginationPageSize": 7,
                             "undoRedoCellEditing": True,
                             "rowSelection": "multiple"}
        ),
        dbc.Button(
            id="delete-row-btn",
            children="Delete row",
            color = "danger",
            class_name = "me-1 mt-1",
        ),
        dbc.Button(
            id="add-row-btn",
            children="Add row",
            color = "primary",
            class_name = "me-1 mt-1",
        ),
    ],
    fluid = True #To fit the size of the screen
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
    Output("reports-table", "deleteSelectedRows"),
    Output("reports-table", "rowData"),
    Input("delete-row-btn", "n_clicks"),
    Input("add-row-btn", "n_clicks"),
    State("reports-table", "rowData"),
    prevent_initial_call = True,
)
def update_table(n_dlt, n_add, data):
    if ctx.triggered_id == "add-row-btn":
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

    elif ctx.triggered_id == "delete-row-btn":
        return True, no_update
