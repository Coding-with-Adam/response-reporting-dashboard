from dash import html, dcc, Input, Output, State, callback, ctx, register_page
import dash_bootstrap_components as dbc
from utils.database_connector import read_query
from utils.custom_templates import session_data_template
from utils.app_queries import verify_user
from utils.password_encryption import compare_passwords

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
			width = {"size" : 5, "offset" : 1}
			),
		dbc.Col([
			dbc.Input(id = "id_login_password", type = "password", placeholder = "Enter your password")
			],
			width = 4
			),
		dbc.Col([
			dbc.Button("Login", id = "id_login_button", color = "primary")
			],
			width = 1
			)
		],
		style = {"align":"center"}
		),
	dbc.Row([
		dbc.Col(id = "id_login_output_message", width = {"size" : 10, "offset" : 1})
		])
	],
	fluid = True
	)

@callback(#This callback will be run at startup no matter what, because the output from here is in the app
	Output("id_session_data", "data"),
	Output("id_login_page_url", "pathname"),
	Input("id_login_button", "n_clicks"),
	State("id_login_email", "value"),
	State("id_login_password", "value"),
	#Preventing intial call would be useless here because the output from this is used in the app at startup
	)
def login_user(login_click, input_email, input_password):
	user_data = session_data_template.copy() #To avoid rewriting the whole dict stucture

	if ctx.triggered_id == "id_login_button":
		user_full_name = verify_user(input_email)["full_name"]
		hashed_password = verify_user(input_email)["hashed_password"]
		user_is_an_admin = verify_user(input_email)["is_admin"]

		password_validation = compare_passwords(input_password, hashed_password)

		if user_full_name and password_validation:
			user_data["full_name"] = user_full_name
			user_data["is_authenticated"] = True
			user_data["email"] = input_email
			user_data["is_admin"] = bool(user_is_an_admin)
			return user_data, "/"

	user_data["is_authenticated"] = False #To prevent potential bypass of the login
	return user_data, "/login"

@callback(
	Output("id_login_output_message", "children"),
	Input("id_login_button", "n_clicks"),
	Input("id_session_data", "data"),
	prevent_initial_call = True
	)
def show_login_message(login_click, user_data):
	user_logged_in = user_data.get("is_authenticated", False)
	if ctx.triggered_id == "id_login_button" and user_logged_in:
		return "Login Success!"
	elif ctx.triggered_id == "id_login_button" and not user_logged_in:
		return "Login Failure, incorrect credentials."
	return "Enter your credentials."