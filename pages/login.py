from dash import html, dcc, Input, Output, State, callback, ctx, register_page
import dash_bootstrap_components as dbc
from utils.database_connector import read_query
from utils.custom_templates import session_data_template

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
		CONCAT(first_name, ' ', last_name) AS full_name
	FROM vetted_user
	WHERE work_email = "{input_data}";
	"""
	df = read_query(user_query_string)
	if not df.empty:
		return df.iloc[0]["full_name"]
	return ""

@callback(
	Output("id_session_data", "data"),
	Output("id_login_page_url", "pathname"),
	Input("id_login_button", "n_clicks"),
	State("id_login_email", "value"),
	prevent_initial_call = True
	)
def login_user(login_click, email):
	user_full_name = verify_user(email)
	if ctx.triggered_id == "id_login_button" and user_full_name:
		user_data = session_data_template.copy() #To avoid rewriting the whole dict stucture
		user_data["is_authenticated"] = True
		user_data["full_name"] = user_full_name
		return user_data, "/"
	return {"is_authenticated" : False, "full_name": ""}, "/login"

@callback(
	Output("id_login_output_message", "children"),
	Input("id_login_button", "n_clicks"),
	State("id_session_data", "data"),
	prevent_initial_call = True
	)
def show_output(login_click, user_data):
	if ctx.triggered_id == "id_login_button" and user_data["is_authenticated"] == True:
		return "Login Success!"
	else:
		return "Login Failure, incorrect information."