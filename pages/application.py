from dash import Dash, html, dcc, callback, Output, Input, State, register_page
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime

register_page(__name__)

name_input = dbc.Row([
	dbc.Col([
		dbc.Input(id= "id_first_name", placeholder = "Enter first name"),
		],
		width = 6,
		),
	dbc.Col([
		dbc.Input(id= "id_last_name", placeholder = "Enter last name"),
		],
		width = 6,
		),
	],
	class_name = "mb-3"
	)

birth_input = dbc.Row([
	dbc.Col([
		dbc.Input(id= "id_dob", placeholder = "Enter date of birth"),
		],
		width = 6,
		),

	dbc.Col([
		dbc.Input(id= "id_country", placeholder = "Enter country of nationality"),
		],
		width = 6,
		),
	],
	class_name = "mb-3"
	)

credentials_input = dbc.Row([
	dbc.Col([
		dbc.Input(id= "id_email", type = "email", placeholder = "Enter email"),
		],
		width = 6,
		),
	dbc.Col([
		dbc.Input(id= "id_password", type = "password", placeholder = "Enter password"),
		],
		width = 6,
		),
	],
	class_name = "mb-3"
	)

form = dbc.Card([
	dbc.CardBody([
		name_input,
		birth_input,
		credentials_input,
		])
	])

layout = dbc.Container([
	html.Hr(),
	dbc.Row([
		html.H1("Become a vetted user for VOST", style = {"text-align" : "center"}),
		]),
	html.Hr(),
	form,
	html.Hr(),
	dbc.Row([
		dbc.Col([
			dbc.Button("Submit", color = "primary")
			])
		])
	],
	fluid = True
	)