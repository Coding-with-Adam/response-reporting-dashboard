from dash import Dash, html, dcc, callback, Output, Input, State, register_page, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import re
from datetime import datetime
from utils.app_queries import register_user

register_page(__name__)

countries = pd.read_csv("assets/countries_list.csv") #To replace with a read query from database
country_names = countries["country_name"]

#_________________________________________Form Input Components_________________________________________#

name_input = dbc.Row([
	dbc.Label("First Name: ", width = 1),
	dbc.Col([
		dbc.Input(id= "id_first_name_in", placeholder = "Enter your first name", invalid = True),
		],
		width = 5,
		),
	dbc.Label("Last Name:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_last_name_in", placeholder = "Enter your last name", invalid = True),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

affiliation_input = dbc.Row([
	dbc.Label("Affiliation:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_affiliatiion_in", placeholder = "The name of the entity you are representing"),
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
			id = "id_signatory_status")
		],
		width = 2,
		),
	],
	class_name = "mb-3"
	)

contacts_input = dbc.Row([
	dbc.Label("Website:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_website_in", placeholder = "Enter the website of the entity"),
		],
		width = 5,
		),
	dbc.Label("Work Email:", width = 1),
	dbc.Col([
		dbc.Input(id= "id_email_in", type = "email", placeholder = "Enter your work email", invalid = True),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

country_input = dbc.Row([
	dbc.Label("Country:", width = 1),
	dbc.Col([
		dbc.Select([
			{"label" : country, "value" : country} for country in country_names
			],
			id = "id_country_in",
			value = "",
			invalid = True,
			placeholder = "Select the country of the entity",
			required = True),
		],
		width = 5,
		),
	],
	class_name = "mb-3"
	)

#_________________________________________Form body_________________________________________#

form = dbc.Card([
	dbc.CardBody([
		name_input,
		affiliation_input,
		contacts_input,
		country_input,
		])
	])

#_________________________________________Form Layout_________________________________________#

layout = dbc.Container([
	dcc.Store(id = "id_registration_data", storage_type = "local", data = {"registered_user":False}),
	dcc.Location(id="id_url", refresh = True),

	html.Hr(),
	dbc.Row([
		html.H1("New User Registration", style = {"text-align" : "center"}),
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
		dbc.Col(id = "id_registration_message")
		])
	],
	fluid = True
	)

#___________________________________________Callbacks___________________________________________#

@callback(
	Output("id_first_name_in", "invalid"),
	Input("id_first_name_in", "value"),
	prevent_initial_call = True
	)
def verify_first_name(first_name):
	name_criteria = r"[a-zA-Z]{2,}"
	first_name_match = re.match(name_criteria, first_name)
	if first_name_match:
		return False
	return True

@callback(
	Output("id_last_name_in", "invalid"),
	Input("id_last_name_in", "value"),
	prevent_initial_call = True
	)
def verify_last_name(last_name):
	name_criteria = r"[a-zA-Z]{2,}"
	last_name_match = re.match(name_criteria, last_name)
	if last_name_match:
		return False
	return True

@callback(
	Output("id_email_in", "invalid"),
	Input("id_email_in", "value"),
	prevent_initial_call = True
	)
def verify_email(user_email):
	email_criteria = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
	result = re.match(email_criteria, user_email)
	if result:
		return False
	return True

@callback(
	Output("id_country_in", "invalid"),
	Input("id_country_in", "value"),
	prevent_initial_call = True
	)
def verify_country(entity_country):
	if entity_country == "":
		return True
	return False

@callback(
	Output("id_registration_message", "children"),
	Output("id_registration_data", "data"),
	Input("id_submit_button", "n_clicks"),
	State("id_first_name_in", "invalid"),
	State("id_last_name_in", "invalid"),
	State("id_email_in", "invalid"),
	State("id_country_in", "invalid"),
	State("id_first_name_in", "value"),
	State("id_last_name_in", "value"),
	State("id_affiliatiion_in", "value"),
	State("id_signatory_status", "value"),
	State("id_website_in", "value"),
	State("id_email_in", "value"),
	State("id_country_in", "value"),
	prevent_initial_call = True
	)
def submit_button_click(submit_click, f_name_invalid, l_name_invalid, email_invalid, country_invalid,
	f_name_in, l_name_in, affiliation_in, status_in, website_in, email_in, country_in):

	invalid_inputs = [f_name_invalid, l_name_invalid, email_invalid, country_invalid]

	if (ctx.triggered_id == "id_submit_button") and not (True in invalid_inputs):
		query_output_message = register_user(email_in, f_name_in, l_name_in, affiliation_in,
			website_in, status_in, country_in)
		if query_output_message == "Success":
			return "Submission successful", {"registered_user":True}
		elif query_output_message == "Existing User":
			return "The input email is already taken", {"registered_user":False}
		else:
			return query_output_message, {"registered_user":False}
	return "Incorrect information", {"registered_user":False}

@callback(
	Output("id_url", "pathname"),
	Input("id_registration_data", "data"),
	prevent_initial_call = True
	)
def load_user_home_page(registration_data):
	if registration_data["registered_user"] == True:
		return "/login"
	else:
		return "/application"


