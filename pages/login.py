from dash import html, dcc, Input, Output, State, callback, ctx, register_page
import dash_bootstrap_components as dbc

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
		dbc.Col(id = "id_test_login")
		])
	],
	fluid = True)

@callback(
	Output("id_session_data", "data"),
	Output("id_login_page_url", "pathname"),
	Input("id_login_email", "value"),
	Input("id_login_button", "n_clicks"),
	prevent_initial_call = True
	)
def login_user(email, login_click):
	if ctx.triggered_id == "id_login_button":
		user_data = {"user_email" : email}
		return user_data, "/"
	return {}, "/login"