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

#_______________________________________Grid Columns definition_______________________________________#
#Consider moving column definitions and its function calls into a new module, and only import the result

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

#_______________________________________Modals Sub components_______________________________________#

confirm_delete_button = dbc.Button(
    id = "id_confirm_delete_button",
    children = "Yes",
    color = "danger",
    class_name = "me-1"
    )
reject_delete_button = dbc.Button(
    id = "id_reject_delete_button",
    children = "No",
    color = "success",
    class_name = "me-auto"
    )

#_________________________________________Report Edit Modals_________________________________________#

delete_report_modal = dbc.Modal([
    dbc.ModalBody([
        dbc.Row([html.P("Delete this report?", style = {"text-align":"center", "color":"black"})]),
        dbc.Row([
            dbc.Col([confirm_delete_button, reject_delete_button])
            ],
            ),
        ])
    ],
    id = "id_delete_report_modal",
    is_open = False,
    size = "sm",
    )

update_report_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Update a Report")),
    dbc.ModalBody("Plaholder for Update Report"),
    dbc.ModalFooter()
    ],
    id = "id_update_report_modal",
    is_open = False,
    size = "lg",
    )

add_report_modal = dbc.Modal([
    dbc.ModalHeader("Add a New Report"),
    dbc.ModalBody("Plaholder for Update Report"),
    dbc.ModalFooter()
    ],
    id = "id_add_report_modal",
    is_open = False,
    size = "lg",
    )

#____________________________________________Layout items____________________________________________#

reports_grid = dag.AgGrid(
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

delete_report_button = dbc.Button(
    id = "id_delete_report_button",
    children = "Delete Report",
    color = "danger",
    class_name = "me-1 mt-1",
    )

update_report_button = dbc.Button(
    id = "id_update_report_button",
    children = "Update Report",
    color = "secondary",
    class_name = "me-1 mt-1",
    )

add_report_button = dbc.Button(
    id = "id_add_report_button",
    children = "Add New Report",
    color = "primary",
    class_name = "me-1 mt-1",
    )

#_______________________________________Layout Protection Setup_______________________________________#

protected_container = dbc.Container([
        html.H1("Internal", style = {"text-align":"center"}),
        dmc.Center(html.H4("Update existing report or insert a new report.")),
        dbc.Row([reports_grid]),
        dbc.Row([
            dbc.Col([delete_report_modal, update_report_modal, add_report_modal])
            ],
            id = "id_hidden_row_for_modals"
            ),
        dbc.Row([
            dbc.Col([delete_report_button, update_report_button, add_report_button]),
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
    Output("id_delete_report_modal", "is_open"),
    Input("id_delete_report_button", "n_clicks"),
    State("id_delete_report_modal", "is_open")
)
def add_report_table(add_click, modal_status):
    if ctx.triggered_id == "id_delete_report_button":
        return not modal_status
    return modal_status

@callback(
    Output("id_update_report_modal", "is_open"),
    Input("id_update_report_button", "n_clicks"),
    State("id_update_report_modal", "is_open")
)
def add_report_table(add_click, modal_status):
    if ctx.triggered_id == "id_update_report_button":
        return not modal_status
    return modal_status

@callback(
    Output("id_add_report_modal", "is_open"),
    Input("id_add_report_button", "n_clicks"),
    State("id_add_report_modal", "is_open")
)
def add_report_table(add_click, modal_status):
    if ctx.triggered_id == "id_add_report_button":
        return not modal_status
    return modal_status
