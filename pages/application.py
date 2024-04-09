from dash import Dash, html, dcc, callback, Output, Input, State, register_page
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
from datetime import datetime

register_page(__name__)

name_input = dbc.Row([
	dbc.Label("First Name: ", width = 1),
	dbc.Col([
		dbc.Input(id= "id_first_name", placeholder = "Enter first name"),
		],
		width = 5,
		),
	dbc.Label("Last Name:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_last_name", placeholder = "Enter last name"),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

gender_and_dob_input = dbc.Row([
	dbc.Label("Gender:", width = 1),
	dbc.Col([
		dbc.Select(
			options = [
			{"label":"Male", "value":"male"},
			{"label":"Female", "value":"female"},
			{"label":"Others", "value":"others"}
			],
			value = "male",
			id = "id_gender_input")
		],
		width = 5),
	dbc.Label("Date of Birth:", width = 2),
	dbc.Col([
		dmc.DatePicker(id= "id_dob", value = "1950/01/01"),
		],
		width = 4,
		),
	],
	class_name = "mb-3"
	)

country_input = dbc.Row([
	dbc.Label("Nationality:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_nationality", placeholder = "Enter country of nationality"),
		],
		width = 5,
		),
	dbc.Label("City:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_city", placeholder = "Enter city of residence"),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

credentials_input = dbc.Row([
	dbc.Label("Email:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_email", type = "email", placeholder = "Enter email", invalid = True),
		],
		width = 5,
		),
	dbc.Label("Password:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_password", type = "password", placeholder = "Enter password", invalid = True),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

form = dbc.Card([
	dbc.CardBody([
		name_input,
		gender_and_dob_input,
		country_input,
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