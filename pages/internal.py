from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update, register_page
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
from datetime import datetime
from utils.app_queries import select_user_reports
from utils.app_queries import select_all_platforms
from utils.app_queries import select_reports_types
from utils.app_queries import delete_report

register_page(__name__)

platforms = select_all_platforms()
reports_types = select_reports_types()
decisions = ["Demoted", "Removed", "No Action"]
appeal = ["Yes", "No"]

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

#_________________________________________Modals components_________________________________________#
#----------------------------------------------------------------------------------------------------#
#Delete-Report Modal components
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
#----------------------------------------------------------------------------------------------------#
#Update-Report Modal components
update_report_modal_title = dbc.ModalTitle(
    html.P("Update a Report", style = {"color":"black"})
    )
#----------------------------------------------------------------------------------------------------#
#Add-Report Modal components
add_report_modal_title = dbc.ModalTitle(
    html.P("Add a New Report", style = {"color":"black"})
    )
current_timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")

report_input = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Label("Platform"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in platforms["platform_name"].values
                ],
                value = "",
                id = "id_modal_platform",
                placeholder = "Select the Platform",
                invalid = True,
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Content URL"),
            dbc.Input(id= "id_modal_url", placeholder = "Enter content's URL", invalid = True)
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Report Type"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in reports_types["report_type"].values
                ],
                value = "",
                id = "id_modal_report_type",
                placeholder = "Select Report Type",
                invalid = True
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Screenshot URL"),
            dbc.Input(id= "id_modal_screenshot", placeholder = "Enter Screenshot URL")
            ],
            class_name = "mb-3"
            )
        ],
        class_name = "ms-4 me-2"),
    dbc.Col([
        dbc.Row([
            dbc.Label("Platform Response Date"),
            #To change into date picker
            dbc.Input(id= "id_modal_answer_date", placeholder = "Enter answer date")
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Platform Decison"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in decisions
                ],
                value = "",
                id = "id_modal_decision",
                placeholder = "Select Platform Decision"
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Policy"),
            dbc.Input(id= "id_modal_policy", placeholder = "Enter Policy")
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Appeal"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in appeal
                ],
                value = "",
                id = "id_modal_appeal",
                placeholder = "Apeal Yes/No"
                )
            ],
            class_name = "mb-3"
            )
        ],
        class_name = "ms-2 me-4")
    ],
    )

submit_report_button = dbc.Button(
    id = "id_submit_report_button",
    children = "Sumbit",
    color = "success",
    class_name = "ms-auto"
    )

#___________________________________________Report Modals___________________________________________#

delete_report_modal = dbc.Modal([
    dbc.ModalBody([
        dbc.Row([html.P("Are you sure?", style = {"text-align":"center", "color":"black"})]),
        dbc.Row([
            dbc.Col([confirm_delete_button, reject_delete_button], className = "text-center")
            ],
            ),
        ])
    ],
    id = "id_delete_report_modal",
    is_open = False,
    size = "sm",
    backdrop = True,
    centered = True
    )

update_report_modal = dbc.Modal([
    dbc.ModalHeader(update_report_modal_title),
    dbc.ModalBody("Plaholder for Update Report"),
    dbc.ModalFooter()
    ],
    id = "id_update_report_modal",
    is_open = False,
    size = "lg",
    backdrop = "static",
    scrollable = True,
    )

add_report_modal = dbc.Modal([
    dbc.ModalHeader(add_report_modal_title),
    dbc.ModalBody(report_input),
    dbc.ModalFooter(submit_report_button)
    ],
    id = "id_add_report_modal",
    is_open = False,
    size = "lg",
    backdrop = "static",
    scrollable = True,
    )

#__________________________________________Page Layout items__________________________________________#

reports_grid = dag.AgGrid(
    id = "id_internal_reports_table",
    columnDefs = cols,
    rowData = [],
    columnSize = "sizeToFit",
    defaultColDef = {"editable": False, "filter": True},
    dashGridOptions = {
    "pagination": True,
    "paginationPageSize": 7,
    #"undoRedoCellEditing": True,
    "rowSelection": "single"
    }
    )

delete_report_button = dbc.Button(
    id = "id_delete_report_button",
    children = "Delete Report",
    color = "danger",
    class_name = "me-1 mt-1",
    )
delete_report_button_popover = dbc.Popover([
    "Select a row first to delete."
    ],
    id = "id_delete_report_button_popover",
    target = "id_delete_report_button",
    body = True,
    is_open = False,
    placement = "top",
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
            dbc.Col([
                delete_report_modal,
                update_report_modal,
                add_report_modal
                ])
            ],
            id = "id_hidden_row_for_modals"
            ),
        dbc.Row([
            dbc.Col([
                delete_report_button,
                delete_report_button_popover,
                update_report_button,
                add_report_button
                ]),
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
    Input("id_session_data", "data"),
    )
def get_reports_for_this_user(user_data):
    email = user_data.get("email", "")
    df = select_user_reports(email)
    grid_row_data = df.to_dict("records")
    return grid_row_data

@callback(
    Output("id_delete_report_modal", "is_open"),
    Input("id_delete_report_button", "n_clicks"),
    State("id_internal_reports_table", "selectedRows"),
    State("id_delete_report_modal", "is_open"),
    Input("id_confirm_delete_button", "n_clicks"),
    Input("id_reject_delete_button", "n_clicks"),
)
def open_delete_modal(delete_click, row_data, modal_status, confirm_click, reject_click):
    if ctx.triggered_id == "id_delete_report_button" and row_data:
        return True
    elif ctx.triggered_id == "id_confirm_delete_button" and row_data:
        input_url = row_data[0]["url"]
        delete_report(input_url)
        return False
        #Implement a refresh page mechanism in another callback to reload grid data
    elif ctx.triggered_id == "id_reject_delete_button":
        return False
    return modal_status

@callback(
    Output("id_delete_report_button_popover", "is_open"),
    Input("id_delete_report_button", "n_clicks"),
    State("id_internal_reports_table", "selectedRows"),
    State("id_delete_report_button_popover", "is_open"),
)
def open_delete_popover(delete_click, row_data, popover_status):
    if ctx.triggered_id == "id_delete_report_button" and (not row_data):
        return not popover_status
    return False

@callback(
    Output("id_update_report_modal", "is_open"),
    Input("id_update_report_button", "n_clicks"),
    State("id_internal_reports_table", "selectedRows"),
    State("id_update_report_modal", "is_open")
)
def open_update_modal(add_click, selected_row_data, modal_status):
    if ctx.triggered_id == "id_update_report_button":
        return not modal_status
    return modal_status

@callback(
    Output("id_add_report_modal", "is_open"),
    Input("id_add_report_button", "n_clicks"),
    State("id_add_report_modal", "is_open")
)
def open_add_modal(add_click, modal_status):
    if ctx.triggered_id == "id_add_report_button":
        return not modal_status
    return modal_status
