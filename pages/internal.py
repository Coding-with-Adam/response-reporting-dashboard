from dash import html, dcc, callback, Output, Input, State, ctx, register_page, exceptions
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import re
from datetime import datetime
from utils.app_queries import select_user_reports
from utils.app_queries import select_all_platforms
from utils.app_queries import select_reports_types
from utils.app_queries import delete_report
from utils.app_queries import add_report
from utils.app_queries import update_report
from utils.custom_templates import permission_denial_layout

register_page(__name__)

#_________________________________________Utilities Functions_________________________________________#

decisions = ["Demoted", "Removed", "No Action"]
appeal = ["Yes", "No"]

def match_url(content_url):
    url_criteria = r"^[a-zA-Z0-9:/.]+\.[a-z]{2,3}$"
    if content_url:
        return re.match(url_criteria, content_url)
    return None

def preprocess_if_none(value):
    """NULL values from database are converted into None by Python, which complicates update queries"""
    if value == None:
        return ''
    return value

def get_platforms():
    try:
        platforms = select_all_platforms()["platform_name"].values
    except Exception as e:
        return [e]
    return platforms

def get_report_types():
    try:
        reports_types = select_reports_types()["report_type"].values
    except Exception as e:
        return [e]
    return reports_types

#_______________________________________Grid Columns definition_______________________________________#
#Consider moving column definitions and its function calls into a new utils module, and only import the result

cols = [
    {
        "headerName": "Report Date",
        "field": "open_report_timestamp",
        "filter": "agDateColumnFilter",
        "cellEditor": "agDateStringCellEditor",
        "sortable":True
    },
    {
        "headerName": "Platform",
        "field": "platform",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": get_platforms()},
        "sortable":True
    },
    {
        "headerName": "Content URL",
        "field": "url",
    },
    {
        "headerName": "Report Type",
        "field": "report_type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": get_report_types()}
    },
    {
        "headerName" : "Screenshot URL",
        "field" : "screenshot_url"
    },
    {
        "headerName": "Answer Date",
        "field": "close_report_timestamp",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {
            'min': '2023-01-01',
        },
        "sortable":True
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
#-----------------------------------Delete-Report Modal components-----------------------------------#
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
#-------------------------------------Add-Report Modal components-------------------------------------#
add_report_modal_title = dbc.ModalTitle(
    html.P("Add a New Report")
    )

add_report_inputs = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Label("Platform"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in get_platforms()
                ],
                value = "",
                id = "id_add_platform",
                placeholder = "Select the Platform",
                invalid = True,
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Content URL"),
            dbc.Input(id= "id_add_url", placeholder = "Enter content's URL", invalid = True)
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Report Type"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in get_report_types()
                ],
                value = "",
                id = "id_add_report_type",
                placeholder = "Select Report Type",
                invalid = True
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Screenshot URL"),
            dbc.Input(id= "id_add_screenshot", placeholder = "Enter Screenshot URL")
            ],
            class_name = "mb-3"
            )
        ],
        class_name = "ms-4 me-2"),
    dbc.Col([
        dbc.Row([
            dbc.Label("Platform Response Date and time", className = "display-right"),
            dmc.DatePicker(
                id= "id_add_close_report_date",
                placeholder = "Pick a Date",
                minDate = datetime.now().date(),
                maxDate = datetime.now().date(),
                clearable = True,
                ),
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
                id = "id_add_decision",
                placeholder = "Select Platform Decision"
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Policy"),
            dbc.Input(id= "id_add_policy", placeholder = "Enter Policy")
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
                id = "id_add_appeal",
                placeholder = "Apeal Yes/No",
                disabled = True, #To select only when there is already a platform decision
                )
            ],
            class_name = "mb-3"
            )
        ],
        class_name = "ms-2 me-4")
    ],
    )

add_report_output_message = dbc.Row([
    "Complete the form and click on the submit button "
    ],
    id = "id_add_report_message",
    class_name = "ms-3")

submit_report_button = dbc.Button(
    id = "id_submit_report_button",
    children = "Sumbit",
    color = "success",
    class_name = "ms-auto",
    disabled = "True"
    )

#-------------------------------------Update-Report Modal components-------------------------------------#
update_report_modal_title = dbc.ModalTitle(
    html.P("Update a Report")
    )

#identical to add_report_inputs, violates the DRY pinciple but avoids Dash callbacks conflicts
update_report_inputs = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Label("Platform"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in get_platforms()
                ],
                value = "",
                id = "id_update_platform",
                placeholder = "Select the Platform",
                invalid = True,
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Content URL"),
            dbc.Input(id= "id_update_url", type = "text", disabled = False)
            #Turn disabled to True if desirable to prevent update of url
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Report Type"),
            dbc.Select(
                options = [
                {"label": value, "value":value} for value in get_report_types()
                ],
                value = "",
                id = "id_update_report_type",
                placeholder = "Select Report Type",
                invalid = True
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Screenshot URL"),
            dbc.Input(id= "id_update_screenshot", type = "text", placeholder = "Enter Screenshot URL")
            ],
            class_name = "mb-3"
            )
        ],
        class_name = "ms-4 me-2"),
    dbc.Col([
        dbc.Row([
            dbc.Label("Platform Response Date"),
            dmc.DatePicker(
                id= "id_update_close_report_date",
                placeholder = "Pick a Date",
                maxDate = datetime.now().date(),
                clearable = True,
                ),
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
                id = "id_update_decision",
                placeholder = "Select Platform Decision"
                )
            ],
            class_name = "mb-3"
            ),
        dbc.Row([
            dbc.Label("Policy"),
            dbc.Input(id= "id_update_policy", type = "text", placeholder = "Enter Policy")
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
                id = "id_update_appeal",
                placeholder = "Apeal Yes/No",
                disabled = True, #To select only when there is already a platform decision
                )
            ],
            class_name = "mb-3"
            )
        ],
        class_name = "ms-2 me-4")
    ],
    )

update_report_message = dbc.Row([
    "Update and click on the Confirm Update button"
    ],
    id = "id_update_report_message",
    class_name = "ms-3")

confirm_update_button = dbc.Button(
    id = "id_confirm_update_button",
    children = "Confirm Update",
    color = "success",
    class_name = "ms-auto",
    disabled = "True"
    )

#___________________________________________Report Modals___________________________________________#

delete_report_modal = dbc.Modal([
    dbc.ModalBody([
        dbc.Row([html.P("Are you sure?", style = {"text-align":"center", "color":"black"})]),
        dbc.Row([dbc.Col([confirm_delete_button, reject_delete_button], className = "text-center")],),
        dbc.Row(id = "id_delete_report_message", class_name = "ms-2")
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
    dbc.ModalBody([
        update_report_inputs,
        update_report_message,
        ]),
    dbc.ModalFooter(confirm_update_button)
    ],
    id = "id_update_report_modal",
    is_open = False,
    size = "lg",
    backdrop = "static",
    scrollable = True,
    )

add_report_modal = dbc.Modal([
    dbc.ModalHeader(add_report_modal_title),
    dbc.ModalBody([
        add_report_inputs,
        add_report_output_message
        ]),
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
    rowData = [], #Initialize to empty list of records
    columnSize = "sizeToFit",
    defaultColDef = {"editable": False, "filter": True, "resizable": True},
    dashGridOptions = {
    "pagination": True,
    "paginationPageSize": 7,
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

protected_layout = dbc.Container([
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

#__________________________________________The actual Layout__________________________________________#

layout = dbc.Container([
    ],
    id = "id_internal_page_layout",
    fluid = True
    )

#______________________________________________Callbacks______________________________________________#

#------------------------------------------Securing the Page------------------------------------------#
@callback(
    Output("id_internal_page_layout", "children"),
    Input("id_session_data", "data")
    ) #Do not prevent initial call
def layout_security(session_data):
    authenticated = session_data.get("is_authenticated", False)
    if authenticated:
        return protected_layout
    return permission_denial_layout

#---------------------------------------Returning User's reports---------------------------------------#
@callback(
    Output("id_internal_reports_table", "rowData"),
    Input("id_session_data", "data"),
    Input("id_add_report_message", "children"),
    Input("id_delete_report_message", "children"),
    Input("id_update_report_message", "children")
    )
def get_reports_for_this_user(user_data, new_report_msg, delete_report_msg, update_report_message):
    """The data is refreshed both when the user logs in and when there are updates"""
    user_email = user_data.get("email", "")
    df = select_user_reports(user_email)
    grid_row_data = df.to_dict("records")
    return grid_row_data

#------------------------------------------Deleting Data------------------------------------------#
@callback(
    Output("id_delete_report_button_popover", "is_open"),
    Input("id_delete_report_button", "n_clicks"),
    State("id_internal_reports_table", "selectedRows"),
    State("id_delete_report_button_popover", "is_open"),
    prevent_initial_call = True,
)
def open_delete_popover(delete_click, row_data, popover_status):
    if ctx.triggered_id == "id_delete_report_button" and (not row_data):
        return not popover_status
    return False

@callback(
    Output("id_delete_report_modal", "is_open"),
    Input("id_delete_report_button", "n_clicks"),
    State("id_internal_reports_table", "selectedRows"),
    State("id_delete_report_modal", "is_open"),
    Input("id_confirm_delete_button", "n_clicks"),
    Input("id_reject_delete_button", "n_clicks"),
    prevent_initial_call = True,
)
def open_delete_report_modal(delete_click, row_data, modal_status, confirm_click, reject_click):
    """A click on delete button with data selected opens the delete modal. All other clicks close it"""
    if ctx.triggered_id == "id_delete_report_button" and row_data:
        return True
    return False

@callback(
    Output("id_delete_report_message", "children"),
    State("id_internal_reports_table", "selectedRows"),
    Input("id_confirm_delete_button", "n_clicks"),
    Input("id_reject_delete_button", "n_clicks"),
    prevent_initial_call = True,
)
def delete_a_report(row_data, confirm_click, reject_click):
    """If this callback is triggered, then the delete modal is already open, with a selected row of data."""
    if ctx.triggered_id == "id_confirm_delete_button":
        input_url = row_data[0]["url"]
        delete_report(input_url)
    #A None children is returned as output message, which still helps trigger data update, no value needed.

#------------------------------------------Adding Data------------------------------------------#
@callback(
    Output("id_add_report_modal", "is_open"),
    Input("id_add_report_button", "n_clicks"),
    State("id_add_report_modal", "is_open"),
    prevent_initial_call = True,
)
def open_add_modal(add_click, modal_status):
    if ctx.triggered_id == "id_add_report_button":
        return not modal_status
    return modal_status

@callback(
    Output("id_add_platform", "invalid"),
    Input("id_add_platform", "value"),
    prevent_initial_call = True,
    )
def verify_platform_name(platform_name):
    if len(platform_name) == 0:
        return True
    return False

@callback(
    Output("id_add_url", "invalid"),
    Input("id_add_url", "value"),
    prevent_initial_call = True,
    )
def verify_content_url(url_to_add):
    result = match_url(url_to_add)
    if result:
        return False
    return True

@callback(
    Output("id_add_report_type", "invalid"),
    Input("id_add_report_type", "value"),
    prevent_initial_call = True,
    )
def verify_report_type(report_type):
    if len(report_type) == 0:
        return True
    return False

@callback(
    Output("id_add_appeal", "disabled"),
    Input("id_add_decision", "value"),
    prevent_initial_call = True
    )
def prevent_appeal_of_nonexisting_decision(platform_decision):
    if platform_decision:
        return False
    return True

@callback(
    Output("id_submit_report_button", "disabled"),
    Input("id_add_platform", "invalid"),
    Input("id_add_url", "invalid"),
    Input("id_add_report_type", "invalid"),
    prevent_initial_call = True,
    )
def prevent_bad_report_submission(platform_invalid, url_invalid, type_invalid):
    if True in [platform_invalid, url_invalid, type_invalid]:
        return True
    return False

@callback(
    Output("id_add_report_message", "children"),
    Input("id_submit_report_button", "n_clicks"),
    State("id_session_data", "data"),
    State("id_add_platform", "value"),
    State("id_add_url", "value"),
    State("id_add_report_type", "value"),
    State("id_add_screenshot", "value"),
    State("id_add_close_report_date", "value"),
    State("id_add_decision", "value"),
    State("id_add_policy", "value"),
    State("id_add_appeal", "value"),
    prevent_initial_call = True,
    )
def insert_new_report(submit_click, user_data, platform, url, report_type, screenshot,
    close_report_timestamp, decision, policy, appeal):
    open_report_timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
    user_email = user_data.get("email")
    if ctx.triggered_id == "id_submit_report_button":
        output = add_report(open_report_timestamp, user_email, platform, url, report_type, screenshot,
            close_report_timestamp, decision, policy, appeal)
        return output

#------------------------------------------Updating Data------------------------------------------#
@callback(
    Output("id_update_report_modal", "is_open"),
    Input("id_update_report_button", "n_clicks"),
    State("id_internal_reports_table", "selectedRows"),
    State("id_update_report_modal", "is_open"),
    prevent_initial_call = True,
)
def open_update_modal(add_click, selected_row, modal_status):
    if ctx.triggered_id == "id_update_report_button" and selected_row:
        return True
    return False

@callback(
    Output("id_update_platform", "value"),
    Output("id_update_url", "value"),
    Output("id_update_report_type", "value"),
    Output("id_update_screenshot", "value"),
    Output("id_update_close_report_date", "value"),
    Output("id_update_decision", "value"),
    Output("id_update_policy", "value"),
    Output("id_update_appeal", "value"),
    Input("id_update_report_button", "n_clicks"),
    State("id_internal_reports_table", "selectedRows"),
    prevent_initial_call = True
    )
def fill_in_update_modal(update_modal_n_clik, selected_row):
    """Callback triggered once there is a click on the update button (with or without selected row)"""
    if ctx.triggered_id == "id_update_report_button" and selected_row:

        data = selected_row[0]
        platform = data["platform"]
        url = data["url"]
        report_type = preprocess_if_none(data["report_type"])
        screenshot = preprocess_if_none(data["screenshot_url"])
        close_report_timestamp = preprocess_if_none(data["close_report_timestamp"])
        decision = preprocess_if_none(data["platform_decision"])
        policy = preprocess_if_none(data["policy"])
        appeal = preprocess_if_none(data["appeal"])

        return (platform, url, report_type, screenshot, close_report_timestamp, decision, policy, appeal)
    raise exceptions.PreventUpdate

@callback(
    Output("id_update_platform", "invalid"),
    Input("id_update_platform", "value"),
    prevent_initial_call = True,
    )
def verify_platform_to_update(platform_to_update):
    if platform_to_update:
        return False
    return True

@callback(
    Output("id_update_url", "invalid"),
    Input("id_update_url", "value"),
    prevent_initial_call = True,
    )
def verify_url_to_update(url_to_update):
    result = match_url(url_to_update)
    if result:
        return False
    return True

@callback(
    Output("id_update_report_type", "invalid"),
    Input("id_update_report_type", "value"),
    prevent_initial_call = True,
    )
def verify_type_to_update(report_type):
    if report_type:
        return False
    return True

@callback(
    Output("id_update_appeal", "disabled"),
    Input("id_update_decision", "value"),
    prevent_initial_call = True
    )
def prevent_update_appeal_of_nonexisting_decision(platform_decision_update):
    if platform_decision_update:
        return False
    return True

@callback(
    Output("id_confirm_update_button", "disabled"),
    Input("id_update_platform", "invalid"),
    Input("id_update_url", "invalid"),
    Input("id_update_report_type", "invalid"),
    prevent_initial_call = True,
    )
def prevent_bad_report_update(platform_update_invalid, url_update_invalid, type_update_invalid):
    if True in [platform_update_invalid, url_update_invalid, type_update_invalid]:
        return True
    return False

@callback(
    Output("id_update_report_message", "children"),
    Input("id_update_report_modal", "is_open"),
    Input("id_confirm_update_button", "n_clicks"),
    State("id_update_platform", "value"),
    State("id_update_url", "value"),
    State("id_update_report_type", "value"),
    State("id_update_screenshot", "value"),
    State("id_update_close_report_date", "value"),
    State("id_update_decision", "value"),
    State("id_update_policy", "value"),
    State("id_update_appeal", "value"),
    prevent_initial_call = True
    )
def perform_data_update(update_modal_opened, confirm_update_click, platform, url, report_type,
    screenshot, close_report_timestamp, decision, policy, appeal):

    if ctx.triggered_id == "id_confirm_update_button":
        result = update_report(platform, url, report_type, screenshot, close_report_timestamp, decision, policy, appeal)
        return result
    return "Update and click on the Confirm Update button" #Default output message