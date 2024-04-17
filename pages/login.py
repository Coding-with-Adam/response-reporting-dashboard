from dash import html, dcc, Input, Output, State, callback, ctx, register_page
import dash_bootstrap_components as dbc
from utils.database_connector import read_query

register_page(__name__)

layout = dbc.Container([
	dcc.Location(id = "id_login_page_url", refresh = True),

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

def verify_user(input_data):
	user_query_string = f"""
	SELECT
		CASE
			WHEN "{input_data}" IN (SELECT work_email FROM vetted_user) THEN 1
			ELSE 0
		END AS is_a_user
	FROM vetted_user;
	"""
	is_a_user = read_query(user_query_string).iloc[0, 0]
	if is_a_user:
		return True
	return False

@callback(
	Output("id_session_data", "data"),
	Output("id_login_page_url", "pathname"),
	State("id_login_email", "value"),
	Input("id_login_button", "n_clicks"),
	prevent_initial_call = True
	)
def login_user(email, login_click):
	is_verified = verify_user(email)
	if ctx.triggered_id == "id_login_button" and is_verified:
		user_data = {"is_authenticated" : True}
		return user_data, "/"
	return {"is_authenticated" : False}, "/login"

@callback(
	Output("id_login_output_message", "children"),
	Input("id_login_button", "n_clicks"),
	State("id_session_data", "data"),
	prevent_initial_call = True
	)
def show_output(login_click, user_data):
	if ctx.triggered_id == "id_login_button" and user_data["is_authenticated"]:
		return "Login Success!"
	else:
		return "Login Failure, incorrect information."