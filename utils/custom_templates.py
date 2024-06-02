from dash import html
import dash_bootstrap_components as dbc


#Template to store user's session data
session_data_template = {
    "email" : "",
    "full_name" : "",
    "is_authenticated" : False,
    "application_decision" : "",
    "is_admin" : False,
    "require_password_reset" : False
    }

#Pages protection setup
permission_denial_layout = dbc.Container([
	html.Hr(),
	dbc.Row([
        dbc.Col([
            html.H1("Permission denied. No rights to access the requested page.")
            ],
            style = {"text-align":"center"})
        ]),
    html.Hr(),
    ],
    fluid = True
    )