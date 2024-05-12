from dash import Dash, html, dcc, callback, Output, Input, State, ctx, register_page
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import re
from datetime import datetime
from utils.custom_templates import permission_denial_layout

register_page(__name__)

#_______________________________________Layout Protection Setup_______________________________________#

protected_layout = dbc.Container([
    ],
    fluid = True
)

#__________________________________________The actual Layout__________________________________________#

layout = dbc.Container([
    ],
    id = "id_admin_menu_layout",
    fluid = True
    )

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