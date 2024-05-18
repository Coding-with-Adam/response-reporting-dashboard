from dash import Dash, html, dcc, callback, Output, Input, State, ctx, register_page
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import re
from datetime import datetime
from utils.custom_templates import permission_denial_layout
from utils.app_queries import select_all_users

register_page(__name__)

#_________________________________________Admin Menu Buttons_________________________________________#
approval_menu_button = dbc.Button(
    "User Approval",
    id = "id_approval_menu_button",
    color = "primary",
    outline = True,
    active = True, #Default active menu
    class_name = "me-1",
    )

deletion_menu_button = dbc.Button(
    "User Delete",
    id = "id_deletion_menu_button",
    color = "danger",
    outline = True,
    active = False,
    class_name = "me-1",
    )

add_menu_button = dbc.Button(
    "User Add",
    id = "id_add_menu_button",
    color = "success",
    outline = True,
    active = False,
    class_name = "me-1",
    )

password_reset_menu_button = dbc.Button(
    "Passwords Reset",
    id = "id_resset_password_menu_button",
    color = "warning",
    outline = True,
    active = False,
    class_name = "me-1",
    )

admins_management_menu_button = dbc.Button(
    "Admins Management",
    id = "id_admins_management_menu_button",
    color = "info",
    outline = True,
    active = False,
    class_name = "me-1",
    )

#Group the buttons into a division wich will be a row of the admin menu
admin_buttons_row = html.Div([
        approval_menu_button,
        deletion_menu_button,
        add_menu_button,
        password_reset_menu_button,
        admins_management_menu_button,
        ],
        id = "id_buttons_row",
        className = "gap-2 d-flex justify-content-center"
        )
#A dictionary to update the active buttons. Warning : Designed with callback outputs positions in mind
buttons_status = {
    "id_approval_menu_button" : [True, False, False, False, False],
    "id_deletion_menu_button" : [False, True, False, False, False],
    "id_add_menu_button" : [False, False, True, False, False],
    "id_resset_password_menu_button" : [False, False, False, True, False],
    "id_admins_management_menu_button" : [False, False, False, False, True]
    }

#__________________________________________Menus Content___________________________________________#
#------------------------------------------Approval Menu-------------------------------------------#
admin_decisions = ["Approved", "Rejected", "Pending"]

users_grid_cols = [
    {
        "headerName": "Email",
        "field": "work_email",
        "cellEditor": "agSelectCellEditor",
        "sortable":True
    },
    {
        "headerName": "First Name",
        "field": "first_name",
        "cellEditor": "agSelectCellEditor",
        "sortable":True
    },
    {
        "headerName": "Last Name",
        "field": "last_name",
        "cellEditor": "agSelectCellEditor",
        "sortable":True
    },
    {
        "headerName": "Affiliation",
        "field": "affiliation_name",
        "cellEditor": "agSelectCellEditor",
        "sortable":True
    },
    {
        "headerName": "Application Date",
        "field": "application_date",
        "filter": "agDateColumnFilter",
        "cellEditor": "agDateStringCellEditor",
        "sortable":True
    },
    {
        "headerName": "Application Decision",
        "field": "application_decision",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": admin_decisions}
    }
    ]

pending_applications_table = dag.AgGrid(
    id = "id_pending_applications_table",
    columnDefs = users_grid_cols,
    rowData = [], #Initialize to empty list of records
    columnSize = "sizeToFit",
    defaultColDef = {"editable": False, "filter": True, "resizable": True},
    dashGridOptions = {
    "pagination": True,
    "paginationPageSize": 7,
    "rowSelection": "single"
    }
    )

approve_application_button = dbc.Button(
    "Approve",
    id = "id_approve_application_button",
    color = "success",
    )
reject_application_button = dbc.Button(
    "Reject",
    id = "id_reject_application_button",
    color = "danger",
    )

decisions_buttons = html.Div([
    approve_application_button,
    reject_application_button,
    ],
    id = "id_decisions_buttons_row",
    className = "mt-2 gap-2 d-flex justify-content-center"
    )

#-------------------------Inserting the subcomponents into their containers-------------------------#
approval_menu_content = dbc.Container([
    dbc.Row([pending_applications_table]),
    dbc.Row([decisions_buttons]),
    ],
    id = "id_approval_menu_content"
    )

deletion_menu_content = dbc.Container([
    "Deletion Menu"
    ],
    id = "id_deletion_menu_content"
    )

add_menu_content = dbc.Container([
    "Add Menu"
    ],
    id = "id_add_menu_content"
    )

reset_password_menu_content = dbc.Container([
    "Password Reset Menu"
    ],
    id = "id_reset_menu_content"
    )

admins_management_menu_content = dbc.Container([
    "Admins Management"
    ],
    id = "id_admins_management_menu_content"
    )


#------------------------------Dynamic Layout Content for Selected Button------------------------------#
#A dictionary for dynamic content after each button click. Tabs would be equivalent but less beautiful
buttons_contents = {
    "id_approval_menu_button" : approval_menu_content,
    "id_deletion_menu_button" : deletion_menu_content,
    "id_add_menu_button" : add_menu_content,
    "id_resset_password_menu_button" : reset_password_menu_content,
    "id_admins_management_menu_button" : admins_management_menu_content
    }

#_______________________________________Layout Protection Setup_______________________________________#

protected_layout = dbc.Container([
    html.Hr(),
    dbc.Row(admin_buttons_row),
    html.Hr(),
    dbc.Row(id = "id_chosen_menu")
    ],
    fluid = True
    )

#__________________________________________The actual Layout__________________________________________#

layout = dbc.Container([
    ],
    id = "id_admin_menu_layout",
    fluid = True
    )

#______________________________________________Callbacks______________________________________________#
#------------------------------------------Securing the Page------------------------------------------#
@callback(
    Output("id_admin_menu_layout", "children"),
    Input("id_session_data", "data")
    ) #Do not prevent initial call
def layout_security(session_data):
    is_authenticated = session_data.get("is_authenticated", False)
    is_admin = session_data.get("is_admin", False)

    if is_authenticated and is_admin:
        return protected_layout
    return permission_denial_layout

#--------------------------------------------Active Button-------------------------------------------#
@callback(
    Output("id_approval_menu_button", "active"),
    Output("id_deletion_menu_button", "active"),
    Output("id_add_menu_button", "active"),
    Output("id_resset_password_menu_button", "active"),
    Output("id_admins_management_menu_button", "active"),
    Input("id_approval_menu_button", "n_clicks"),
    Input("id_deletion_menu_button", "n_clicks"),
    Input("id_add_menu_button", "n_clicks"),
    Input("id_resset_password_menu_button", "n_clicks"),
    Input("id_admins_management_menu_button", "n_clicks"),
    )
def set_active_button(approval_menu, deletion_menu, add_menu, reset_menu, admin_management_menu):
    """Remember the button_status dictionary with a warning on the positions of the callback outputs"""
    default_active_button = buttons_status["id_approval_menu_button"]
    return buttons_status.get(ctx.triggered_id, default_active_button)

#---------------------------------------------Chosen Menu--------------------------------------------#
@callback(
    Output("id_chosen_menu", "children"),
    Input("id_approval_menu_button", "n_clicks"),
    Input("id_deletion_menu_button", "n_clicks"),
    Input("id_add_menu_button", "n_clicks"),
    Input("id_resset_password_menu_button", "n_clicks"),
    Input("id_admins_management_menu_button", "n_clicks"),
    prevent_initial_call = False
    )
def open_selected_menu(approval_menu, deletion_menu, add_menu, reset_menu, admin_management_menu):
    """Rember that dictionary for dynamic content after button click? Yes, it is used here"""
    default_content = buttons_contents["id_approval_menu_button"]
    return buttons_contents.get(ctx.triggered_id, default_content)

#Update Pending Users Table
@callback(
    Output("id_pending_applications_table", "rowData"),
    Input("id_approval_menu_button", "n_clicks"),
)
def update_pending_applications_table(approval_menu_opened):
    pending_users_table = select_all_users(application_decision = "Pending")
    grid_row_data = pending_users_table.to_dict("records")
    return grid_row_data