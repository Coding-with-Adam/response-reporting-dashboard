from dash import html, dcc, callback, Output, Input, State, ctx, register_page, exceptions
import dash_bootstrap_components as dbc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
from datetime import datetime
from utils.custom_templates import permission_denial_layout
from utils.custom_templates import app_events_flags
from utils.app_queries import select_all_users
from utils.app_queries import update_application_decision
from utils.app_queries import select_pending_password_resets
from utils.app_queries import decide_password_reset

register_page(__name__)

#________________________________________All Grids Columns Defs________________________________________#

email_field = {
    "headerName": "Email",
    "field": "work_email",
    "sortable":True
    }

first_name_field = {
    "headerName": "First Name",
    "field": "first_name",
    "sortable":True
    }

last_name_field = {
    "headerName": "Last Name",
    "field": "last_name",
    "sortable":True
    }

admin_flag_field = {
    "headerName": "Is an Admin",
    "field": "is_admin",
    "sortable":True
    }

affiliation_field = {
    "headerName": "Affiliation",
    "field": "affiliation_name",
    "sortable":True
    }

application_date_field = {
    "headerName": "Application Date",
    "field": "application_date",
    "filter": "agDateColumnFilter",
    "sortable":True
    }

application_decision_field = {
    "headerName": "Application Decision",
    "field": "application_decision"
    }

decision_date_field = {
    "headerName": "Member Since",
    "field": "decision_date",
    "filter": "agDateColumnFilter",
    "sortable":True
    }

decision_author_field = {
    "headerName": "Approved by",
    "field": "decision_author"
    }

password_reset_request_id_field = {
    "field": "id_request",
    "hide":True
    }

password_reset_request_email__field = {
    "field": "work_email",
    "hide":True
    }

password_reset_request_date_field = {
    "headerName": "Request Date",
    "field": "request_date",
    "filter": "agDateColumnFilter",
    "sortable":True
    }

reset_reason_field = {
    "headerName": "Reset Reason",
    "field": "reset_reason"
    }

days_since_last_request_field  = {
    "headerName": "Days Since Last Request",
    "field": "days_since_last_request",
    "sortable":True
    }

total_reset_count_field = {
    "headerName": "Resets Count",
    "field": "resets_count",
    "sortable":True
    }

#_________________________________________Admin Menu Buttons_________________________________________#
approval_menu_button = dbc.Button(
    "User Approval",
    id = "id_approval_menu_button",
    color = "success",
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

fetch_back_menu_button = dbc.Button(
    "Fetch Back",
    id = "id_fetch_back_menu_button",
    color = "primary",
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

#Group the buttons into a division which will be a row of the admin menu
admin_buttons_row = html.Div([
        approval_menu_button,
        deletion_menu_button,
        fetch_back_menu_button,
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
    "id_fetch_back_menu_button" : [False, False, True, False, False],
    "id_resset_password_menu_button" : [False, False, False, True, False],
    "id_admins_management_menu_button" : [False, False, False, False, True]
    }

#__________________________________________Menus Content___________________________________________#
#------------------------------------------Approval Menu-------------------------------------------#

pending_applications_cols = [
    email_field,
    first_name_field,
    last_name_field,
    affiliation_field,
    application_date_field,
    application_decision_field
    ]

pending_applications_table = dag.AgGrid(
    id = "id_pending_applications_table",
    columnDefs = pending_applications_cols,
    rowData = [], #Initialize to empty list of records
    columnSize = "sizeToFit",
    defaultColDef = {"editable": False, "filter": True, "resizable": True},
    dashGridOptions = {
    "pagination": True,
    "paginationPageSize": 7,
    "rowSelection": "multiple"
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

#------------------------------------------Deletion Menu-------------------------------------------#

approved_users_cols = [
    email_field,
    first_name_field,
    last_name_field,
    affiliation_field,
    decision_date_field,
    decision_author_field
    ]

approved_users_table = dag.AgGrid(
    id = "id_approved_users_table",
    columnDefs = approved_users_cols,
    rowData = [], #Initialize to empty list of records
    columnSize = "sizeToFit",
    defaultColDef = {"editable": False, "filter": True, "resizable": True},
    dashGridOptions = {
    "pagination": True,
    "paginationPageSize": 7,
    "rowSelection": "multiple"
    }
    )

user_delete_button = dbc.Button(
    "Delete",
    id = "id_user_delete_button",
    color = "danger",
    className = "mt-2",
    )

confirm_user_delete_button = dbc.Button(
    id = "id_confirm_user_delete_button",
    children = "Yes",
    color = "danger",
    class_name = "me-1"
    )
reject_user_delete_button = dbc.Button(
    id = "id_reject_user_delete_button",
    children = "No",
    color = "success",
    class_name = "me-auto"
    )

user_delete_modal = dbc.Modal([
    dbc.ModalBody([
        dbc.Row([html.P("Are you sure?", style = {"text-align":"center", "color":"black"})]),
        dbc.Row([
            dbc.Col([confirm_user_delete_button, reject_user_delete_button], className = "text-center")
            ],),
        dbc.Row(id = "id_user_deleted_message", class_name = "ms-2")
        ])
    ],
    id = "id_user_delete_modal",
    is_open = False,
    size = "sm",
    backdrop = True,
    centered = True
    )

#----------------------------------------Password Reset Menu-----------------------------------------#

password_resets_cols = [
    password_reset_request_id_field,
    password_reset_request_email__field,
    first_name_field,
    last_name_field,
    affiliation_field,
    password_reset_request_date_field,
    reset_reason_field,
    days_since_last_request_field,
    total_reset_count_field
]

pending_resets_table = dag.AgGrid(
    id = "id_pending_password_resets_table",
    columnDefs = password_resets_cols,
    rowData = [], #Initialize to empty list of records
    columnSize = "sizeToFit",
    defaultColDef = {"editable": False, "filter": True, "resizable": True},
    dashGridOptions = {
    "pagination": True,
    "paginationPageSize": 7,
    "rowSelection": "single"
    }
    )

approve_password_reset_button = dbc.Button(
    "Approve",
    id = "id_approve_password_reset_button",
    color = "success",
    )
reject_password_reset_button = dbc.Button(
    "Reject",
    id = "id_reject_password_reset_button",
    color = "danger",
    )

password_reset_decisions_buttons = html.Div([
    approve_password_reset_button,
    reject_password_reset_button,
    ],
    id = "id_password_reset_decisions_buttons_row",
    className = "mt-2 gap-2 d-flex justify-content-center"
    )

#--------------------------------------Admins Management Menu---------------------------------------#
admin_label_icon = html.Div([html.I(className = "fa fa-user-secret pe-1"), "Admin"])
non_admin_label_icon = html.Div([html.I(className = "fa fa-users pe-1"), "Basic"])

admin_user_priviledge_selection = dbc.Card([
    dbc.Label("Priviledge Category"),
    dbc.RadioItems(
        options = [
            {"label": admin_label_icon, "value": 1},
            {"label": non_admin_label_icon, "value": 0},
        ],
        value = 1,
        inline = True
    )
    ],
    className = "mb-4"
    )

admin_affiliation_selection = dbc.Card([
    dbc.Label("Select an Entity (Optional)"),
    dbc.Select(
        id = "id_admin_users_entity_selection"
        )
    ],
    className = "mb-4"
    )

admin_user_selection = dbc.Card([
    dbc.Label("Select a User"),
    dbc.Select(
        id = "id_admin_users_selection"
        )
    ],
    )

admin_menu_controls = dbc.Col([
    dbc.Row(admin_user_priviledge_selection),
    dbc.Row(admin_affiliation_selection),
    dbc.Row(admin_user_selection),
])


user_room_header = html.Header("User Room", style = {"text-align":"center"}),

user_room_left_pane = dbc.Col([
    dbc.Row([
        dbc.Col(dbc.Input(id = "id_user_room_first_name", placeholder = "First name", disabled = True)),
        dbc.Col(dbc.Input(id = "id_user_room_last_name", placeholder = "Last name", disabled = True))
        ],
        className = "mb-4"
        ),
    dbc.Row([
        dbc.Col(dbc.Input(id = "id_user_room_email", placeholder = "Email", disabled = True)),
        dbc.Col(dbc.Input(id = "id_user_room_affiliation", placeholder = "Affiliation", disabled = True))
        ],
        className = "mb-4"
        ),
    dbc.Row([
        dbc.Col(dbc.Input(id = "id_user_room_date_joined", placeholder = "Date Joinded", disabled = True)),
        ]
        )
    ],
    width = 8,
    )
user_room_right_pane= dbc.Col(html.I(className = "fa fa-id-badge fa-10x"), style = {"text-align":"center"})

user_room_body = dbc.Row([
    user_room_left_pane,
    user_room_right_pane
    ])

user_room_promote_button = dbc.Button("Promote", color = "success")
user_room_demote_button = dbc.Button("Demote", color = "danger")

user_room_footer = html.Div(
    [user_room_promote_button, user_room_demote_button],
    className = "gap-2 d-flex justify-content-left")

admin_menu_user_room = dbc.Col(
    dbc.Card([
        dbc.CardHeader(user_room_header),
        dbc.CardBody(user_room_body),
        dbc.CardFooter(user_room_footer)
    ],
    )
)

#-------------------------Inserting the subcomponents into their containers-------------------------#
approval_menu_content = dbc.Container([
    dbc.Row([pending_applications_table]),
    dbc.Row([
        dbc.Col(id = "id_admin_decision_message", className = "mt-3"),
        dbc.Col([decisions_buttons], width = 6),
        dbc.Col(id = "id_placeholder_admin_decision"), #Temporary solution to keep buttons centered
        ]),
    ],
    id = "id_approval_menu_content"
    )

deletion_menu_content = dbc.Container([
    dbc.Row([approved_users_table]),
    user_delete_modal,
    user_delete_button
    ],
    id = "id_deletion_menu_content"
    )

fetch_back_menu_content = dbc.Container([
    "Add Menu"
    ],
    id = "id_fetch_back_menu_content"
    )

reset_password_menu_content = dbc.Container([
    dbc.Row([pending_resets_table]),
    password_reset_decisions_buttons,
    dcc.Store(id = "id_password_reset_flag", storage_type = 'session', data = {})
    ],
    id = "id_reset_menu_content"
    )

admins_management_menu_content = dbc.Container([
    dbc.Row([
        admin_menu_controls,
        admin_menu_user_room
        ]
        )
    ],
    id = "id_admins_management_menu_content"
    )


#------------------------------Dynamic Layout Content for Selected Button------------------------------#
#A dictionary for dynamic content after each button click. Tabs would be equivalent but less beautiful
buttons_contents = {
    "id_approval_menu_button" : approval_menu_content,
    "id_deletion_menu_button" : deletion_menu_content,
    "id_fetch_back_menu_button" : fetch_back_menu_content,
    "id_resset_password_menu_button" : reset_password_menu_content,
    "id_admins_management_menu_button" : admins_management_menu_content
    }

#_______________________________________Layout Protection Setup_______________________________________#

protected_layout = dbc.Container([
    html.Hr(),
    dbc.Row(admin_buttons_row),
    html.Hr(),
    dbc.Row(id = "id_chosen_menu"),
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

#----------------------------------------Setting Active Button---------------------------------------#
@callback(
    Output("id_approval_menu_button", "active"),
    Output("id_deletion_menu_button", "active"),
    Output("id_fetch_back_menu_button", "active"),
    Output("id_resset_password_menu_button", "active"),
    Output("id_admins_management_menu_button", "active"),
    Input("id_approval_menu_button", "n_clicks"),
    Input("id_deletion_menu_button", "n_clicks"),
    Input("id_fetch_back_menu_button", "n_clicks"),
    Input("id_resset_password_menu_button", "n_clicks"),
    Input("id_admins_management_menu_button", "n_clicks"),
    )
def set_active_button(approval_menu, deletion_menu, add_menu, reset_menu, admin_management_menu):
    """Remember the button_status dictionary with a warning on the positions of the callback outputs"""
    default_active_button = buttons_status["id_approval_menu_button"]
    return buttons_status.get(ctx.triggered_id, default_active_button)

#----------------------------------------Opening the Chosen Menu---------------------------------------#
@callback(
    Output("id_chosen_menu", "children"),
    Input("id_approval_menu_button", "n_clicks"),
    Input("id_deletion_menu_button", "n_clicks"),
    Input("id_fetch_back_menu_button", "n_clicks"),
    Input("id_resset_password_menu_button", "n_clicks"),
    Input("id_admins_management_menu_button", "n_clicks"),
    prevent_initial_call = False
    )
def open_selected_menu(approval_menu, deletion_menu, add_menu, reset_menu, admin_management_menu):
    """Rember that dictionary for dynamic content after button click? Yes, it is used here"""
    default_content = buttons_contents["id_approval_menu_button"]
    return buttons_contents.get(ctx.triggered_id, default_content)

#--------------------------------------Pending Applications Decision------------------------------------#
@callback(
    Output("id_pending_applications_table", "rowData"),
    Input("id_approval_menu_button", "n_clicks"),
    Input("id_admin_decision_message", "children")
)
def update_pending_applications_table(approval_menu_opened, admin_decision):
    pending_users_table = select_all_users(application_decision = "Pending")
    grid_row_data = pending_users_table.to_dict("records")
    return grid_row_data

@callback(
    Output("id_admin_decision_message", "children"),
    State("id_pending_applications_table", "selectedRows"),
    Input("id_approve_application_button", "n_clicks"),
    Input("id_reject_application_button", "n_clicks"),
    State("id_session_data", "data"),
    prevent_initial_call = True
    )
def approve_or_reject_application(selected_rows, approval_click, rejection_click, user_data):
    try:
        users_tuple = tuple([row["work_email"] for row in selected_rows])
        admin_email = user_data.get("email", "")
        date_now = datetime.now()
    except Exception as e:
        pass

    if ctx.triggered_id == "id_approve_application_button" and selected_rows:
        update_application_decision(admin_email, "Approved", date_now, users_tuple)
        return f"Application(s) approved!"
    elif ctx.triggered_id == "id_reject_application_button" and selected_rows:
        update_application_decision(admin_email, "Rejected", date_now, users_tuple)
        return f"Application(s) rejected!"
    raise exceptions.PreventUpdate

#-------------------------------------------Users Delete------------------------------------------#
@callback(
    Output("id_approved_users_table", "rowData"),
    Input("id_deletion_menu_button", "n_clicks"),
    Input("id_user_deleted_message", "children"),
)
def update_approved_users_table(delete_menu_opened, delete_user_message):
    approved_users_table = select_all_users(application_decision = "Approved")
    users_except_admins = approved_users_table[approved_users_table["is_admin"]==0]
    row_data = users_except_admins.to_dict("records")
    return row_data

@callback(
    Output("id_user_delete_modal", "is_open"),
    Input("id_user_delete_button", "n_clicks"),
    Input("id_reject_user_delete_button", "n_clicks"),
    Input("id_user_deleted_message", "children"),
    State("id_approved_users_table", "selectedRows"),
    )
def open_close_user_delete_modal(user_delete_button, reject_click, deleted_user, selected_row):
    if ctx.triggered_id == "id_user_delete_button" and selected_row:
        return True
    return False

@callback(
    Output("id_user_deleted_message", "children"),
    State("id_approved_users_table", "selectedRows"),
    Input("id_confirm_user_delete_button", "n_clicks"),
    State("id_session_data", "data"),
    prevent_initial_call = True
    )
def confirm_user_delete(selected_rows, confirm_click, user_data):
    users_tuple = tuple([row["work_email"] for row in selected_rows])
    admin_email = user_data.get("email", "")
    date_now = datetime.now()
    update_application_decision(admin_email, "Deleted", date_now, users_tuple)
    return ""

#-----------------------------------------Password Reset----------------------------------------#

@callback(
    Output("id_pending_password_resets_table", "rowData"),
    Input("id_resset_password_menu_button", "n_clicks"),
    Input("id_password_reset_flag", "data")
)
def update_resets_request_table(approval_menu_opened, reset_event_flag):
    pending_request_table = select_pending_password_resets()
    grid_row_data = pending_request_table.to_dict("records")
    reset_event_flag["refresh_data"] = False
    return grid_row_data

@callback(
    Output("id_password_reset_flag", "data"),
    Input("id_approve_password_reset_button", "n_clicks"),
    Input("id_reject_password_reset_button", "n_clicks"),
    State("id_pending_password_resets_table", "selectedRows"),
    prevent_initial_call = True
)
def decide_password_reset_request(approve_click, reject_click, selected_rows):
    reset_event_flag = app_events_flags.copy()

    date_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")

    if selected_rows:
        id_request = selected_rows[0]["id_request"]
        user_email = selected_rows[0]["work_email"]
        if ctx.triggered_id == "id_approve_password_reset_button":
            decision = "Approved"
            decide_password_reset(decision, date_now, id_request, user_email)
            reset_event_flag["refresh_data"] = True
            return reset_event_flag
        elif ctx.triggered_id == "id_reject_password_reset_button":
            decision = "Rejected"
            decide_password_reset(decision, date_now, id_request, user_email)
            reset_event_flag["refresh_data"] = True
            return reset_event_flag
    raise exceptions.PreventUpdate