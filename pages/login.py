from dash import html, dcc, Input, Output, State, callback, ctx, register_page
import dash_bootstrap_components as dbc
from utils.database_connector import read_query
from utils.custom_templates import session_data_template
from utils.app_queries import verify_user

register_page(__name__)

layout = dbc.Container([
	dcc.Location(id = "id_login_page_url", refresh = True),

	html.Hr(),
	dbc.Row([
		dbc.Col([
			html.H1("User Login")
			],
			style = {"text-align":"center"})
		]),
	html.Hr(),
	dbc.Row([
		dbc.Col([
			dbc.Input(id= "id_login_email", placeholder = "Enter your work email")
			],
			width = 11
			),
		dbc.Col([
			dbc.Button("Login", id = "id_login_button", color = "primary")
			],
			width = 1
			)
		],
		align = "center"),
	dbc.Row([
		dbc.Col(id = "id_login_output_message")
		])
	],
	fluid = True
	)

@callback(
	Output("id_session_data", "data"),
	Output("id_login_page_url", "pathname"),
	Input("id_login_button", "n_clicks"),
	State("id_login_email", "value"),
	prevent_initial_call = True
	)
def login_user(login_click, email):
	user_data = session_data_template.copy() #To avoid rewriting the whole dict stucture
	returned_name = verify_user(email)
	if ctx.triggered_id == "id_login_button" and returned_name:
		user_data["full_name"] = returned_name
		user_data["is_authenticated"] = True
		user_data["email"] = email
		return user_data, "/"
	user_data["is_authenticated"] = False #This is necessary
	return user_data, "/login"

@callback(
	Output("id_login_output_message", "children"),
	Input("id_login_button", "n_clicks"),
	Input("id_session_data", "data"),
	prevent_initial_call = True
	)
def show_output(login_click, user_data):
	user_logged_in = user_data.get("is_authenticated", False)
	if ctx.triggered_id == "id_login_button" and user_logged_in:
		return "Login Success!"
	elif ctx.triggered_id == "id_login_button" and not user_logged_in:
		return "Login Failure, incorrect information."
	return "Enter your credentials."