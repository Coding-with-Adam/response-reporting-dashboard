# This application page will be built later later in April

# import dash
# from dash import html
# dash.register_page(__name__, path="/application")
#
#
# layout = html.Div(
#     [
#         html.H1('Join Us', className="text-center mt-3 fw-bolder", style={'color': '#2471A3'}),
#
#     ]
# )
import dash
from dash import Dash, html, dcc, callback, Output, Input, State, ctx
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
import re


dash.register_page(__name__)


countries = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/assets/countries_list.csv")
country_names = countries["country_name"]

#_________________________________________Form Input Components_________________________________________#

name_input = dbc.Row([
	dbc.Label("First Name: ", width = 1),
	dbc.Col([
		dbc.Input(id= "id_first_name", placeholder = "Enter your first name", invalid = True),
		],
		width = 5,
		),
	dbc.Label("Last Name:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_last_name", placeholder = "Enter your last name", invalid = True),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

affiliation_input = dbc.Row([
	dbc.Label("Affiliation:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_affiliatiion", placeholder = "The name of the entity you are representing"),
		],
		width = 5),
	dbc.Label("Signatory of the Code of Practice on Disinformation:", width = 4),
	dbc.Col([
		dbc.Select(
			options = [
			{"label":"Yes", "value":"yes"},
			{"label":"No", "value":"no"},
			],
			value = "yes",
			id = "id_signatory")
		],
		width = 2,
		),
	],
	class_name = "mb-3"
	)

country_input = dbc.Row([
	dbc.Label("Website:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_website", placeholder = "Enter the website of the entity"),
		],
		width = 5,
		),
	dbc.Label("Country:", width = 1),
	dbc.Col([
		dcc.Dropdown([
			{"label" : country, "value" : country} for country in country_names
			],
			value = "France",
			clearable = False,
			searchable = True),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

credentials_input = dbc.Row([
	dbc.Label("Work Email:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_email", type = "email", placeholder = "Enter your work email", invalid = True),
		],
		width = 5,
		)
	],
	class_name = "mb-3"
	)

#_________________________________________Form body_________________________________________#

form = dbc.Card([
	dbc.CardBody([
		name_input,
		affiliation_input,
		country_input,
		credentials_input,
		])
	])

#_________________________________________Form Layout_________________________________________#

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
			dbc.Button("Submit", id = "id_submit_button", color = "primary")
			])
		]),
	dbc.Row([
		dbc.Col(id = "id_test_output")
		])
	],
	fluid = True
	)

#_________________________________________Callbacks_________________________________________#

@callback(
	Output("id_first_name", "invalid"),
	Input("id_first_name", "value"),
	prevent_initial_call = True)
def verify_names(first_name):
	name_criteria = r"[a-zA-Z]{2,}"
	first_name_match = re.match(name_criteria, first_name)
	if first_name_match:
		return False
	return True

@callback(
	Output("id_last_name", "invalid"),
	Input("id_last_name", "value"),
	prevent_initial_call = True)
def verify_names(last_name):
	name_criteria = r"[a-zA-Z]{2,}"
	last_name_match = re.match(name_criteria, last_name)
	if last_name_match:
		return False
	return True

@callback(
	Output("id_email", "invalid"),
	Input("id_email", "value"),
	prevent_initial_call = True
	)
def verify_email(user_email):
	email_criteria = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
	result = re.match(email_criteria, user_email)
	if result:
		return False
	return True


@callback(
	Output("id_test_output", "children"),
	Input("id_submit_button", "n_clicks"),
	State("id_first_name", "invalid"),
	State("id_last_name", "invalid"),
	State("id_email", "invalid"),
	prevent_initial_call = True)
def submit_button_click(_, f_name_invalid, l_name_invalid, email_invalid):
	all_status = [f_name_invalid, l_name_invalid, email_invalid]
	print(all_status)
	if True in all_status :
		return "Incorrect information. Form rejected"
	return "Submission successful"
