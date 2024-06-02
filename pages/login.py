from dash import html, dcc, Input, Output, State, callback, ctx, register_page
import dash_bootstrap_components as dbc
import re
from datetime import datetime
from utils.database_connector import read_query
from utils.custom_templates import session_data_template
from utils.app_queries import verify_user, password_reset_request
from utils.password_encryption import hash_password, compare_passwords

register_page(__name__)

#___________________________________________Utilities___________________________________________#

reset_reasons = ["Password Forgotten", "Weak Password", "Password Compromised", "Others"]

#______________________________________Password Reset Modal______________________________________#
#----------------------------------------Modal Components----------------------------------------#

password_reset_modal_title = dbc.ModalTitle(
	html.P("Reset your password")
	)

password_reset_inputs = dbc.Row([
	dbc.Row([
		dbc.Col([
			dbc.Label("Work Email"),
			dbc.Input(
				id = "id_password_reset_email_input",
				type = "email",
				debounce = True,
				placeholder = "Enter your email",
				invalid = True
				)
			],
			width = 6
			),
		dbc.Col([
			dbc.Label("Select a reason"),
			dbc.Select(
                options = [{"label": value, "value":value} for value in reset_reasons],
                value = "",
                id = "id_password_reset_reason_input",
                placeholder = "Select a reason",
                invalid = True,
				)
			],
			width = 6
			)
	],
	class_name = "mb-3"
	),
	dbc.Row([
		dbc.Col([
			dbc.Label("Enter a new password"),
			dbc.Input(
				id = "id_password_reset_password_input",
				type = "password",
				debounce = True, #Prevent update after each letter input
				placeholder = "Enter a new password",
				invalid = True
				)
			]
			),
		dbc.Col([
			dbc.Label("Repeat the new password"),
			dbc.Input(
				id = "id_password_reset_password_input_repeat",
				type = "password",
				debounce = True,
				placeholder = "Re-enter the new password",
				invalid = True
				)	
			]
			)
		],
		class_name = "mb-3"
		)
	]
	)

password_reset_message = dbc.Row([
    "Complete the form, press the Enter key, and click on the request button "
    ],
    id = "id_password_reset_message",
	class_name = "ms-0"
)

request_password_reset = dbc.Button(
	"Request",
	id = "id_password_reset_request_button",
	disabled = True
	)

#----------------------------------------The Actual Modal----------------------------------------#
password_reset_modal = dbc.Modal([
	dbc.ModalHeader(password_reset_modal_title),
    dbc.ModalBody([
        password_reset_inputs,
        password_reset_message,
        ]),
    dbc.ModalFooter(request_password_reset)
    ],
    id = "id_password_reset_modal",
    is_open = False,
    size = "lg",
    backdrop = "static",
    scrollable = True,
	)

#__________________________________________Page Layout__________________________________________#

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
			width = {"size" : 4, "offset" : 1}
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
			),
		dbc.Col([
			dbc.Button("Password Reset", id = "id_password_reset_button", color = "danger", outline=True)
			],
			width = 2
			)
		],
		style = {"align":"center"}
		),
	dbc.Row([
		dbc.Col(id = "id_login_output_message", width = {"size" : 10, "offset" : 1})
		]),
	dbc.Row([
		password_reset_modal
	])
	],
	fluid = True
	)

#____________________________________________Callbacks____________________________________________#
#----------------------------------------------Login----------------------------------------------#

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
	
	user_full_name = verify_user(input_email)["full_name"]
	hashed_password = verify_user(input_email)["hashed_password"]
	user_is_an_admin = verify_user(input_email)["is_admin"]
	user_status = verify_user(input_email)["application_decision"]

	password_validation = compare_passwords(input_password, hashed_password)

	if user_full_name and password_validation:
		user_data["full_name"] = user_full_name
		user_data["email"] = input_email
		user_data["is_admin"] = bool(user_is_an_admin)
		user_data["application_decision"] = user_status
	if user_status == "Approved":
		user_data["is_authenticated"] = True
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
	user_status = user_data.get("application_decision")

	if ctx.triggered_id == "id_login_button" and user_status == "Pending":
		return f"Hi {user_data["full_name"]}, your application is still pending. Please, wait while we process it."
	elif ctx.triggered_id == "id_login_button" and user_status == "Deleted":
		return f"Hi {user_data["full_name"]}, your account has been suspended."
	elif ctx.triggered_id == "id_login_button" and user_status == "Rejected":
		return f"Hi {user_data["full_name"]}, your application was rejected by an admin."
	elif ctx.triggered_id == "id_login_button" and user_logged_in:
		return "Login Success!"
	elif ctx.triggered_id == "id_login_button" and not user_logged_in:
		return "Login Failure, incorrect credentials."
	return "Enter your credentials."

#-----------------------------------------Password Reset-----------------------------------------#

@callback(
	Output("id_password_reset_modal", "is_open"),
	Input("id_password_reset_button", "n_clicks"),
	prevent_initial_call = True
)
def open_password_reset_modal(button_clicked):
	if ctx.triggered_id == "id_password_reset_button":
		return True
	return False

@callback(
	Output("id_password_reset_email_input", "invalid"),
	Input("id_password_reset_email_input", "value"),
	prevent_initial_call = True
)
def validate_password_reset_email(input_email):
	user_full_name = verify_user(input_email)["full_name"]
	if user_full_name:
		return False
	return True

@callback(
    Output("id_password_reset_reason_input", "invalid"),
    Input("id_password_reset_reason_input", "value"),
    prevent_initial_call = True,
    )
def validate_reset_reason(reset_reason):
    if reset_reason:
        return False
    return True

@callback(
	Output("id_password_reset_password_input", "invalid"),
	Input("id_password_reset_password_input", "value"),
	prevent_initial_call = True,
	)
def validate_new_password(new_password):
	password_criteria = r"[a-zA-Z0-9@_\-]{5,16}"
	result = re.match(password_criteria, new_password)
	if result:
		return False
	return True

@callback(
	Output("id_password_reset_password_input_repeat", "invalid"),
	Input("id_password_reset_password_input_repeat", "value"),
	Input("id_password_reset_password_input", "value"),
	prevent_initial_call = True
	)
def validate_second_password_input(first_input, second_input):
	if first_input == second_input:
		return False
	return True

@callback(
    Output("id_password_reset_request_button", "disabled"),
    Input("id_password_reset_email_input", "invalid"),
    Input("id_password_reset_password_input", "invalid"),
    Input("id_password_reset_password_input_repeat", "invalid"),
    prevent_initial_call = True,
    )
def prevent_bad_report_update(email_invalid, password_invalid, password_repeat_invalid):
    if True in [email_invalid, password_invalid, password_repeat_invalid]:
        return True
    return False

@callback(
	Output("id_password_reset_message", "children"),
	Input("id_password_reset_request_button", "n_clicks"),
	State("id_password_reset_email_input", "value"),
	State("id_password_reset_reason_input", "value"),
	State("id_password_reset_password_input", "value"),
	prevent_initial_call = True
)
def submit_password_reset_request(request_click, email_in, reason_in, password_in):
	date_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
	user_status = verify_user(email_in)["application_decision"]
	old_password = verify_user(email_in)["hashed_password"]

	same_password = compare_passwords(password_in, old_password)

	if same_password:
		return "Your new password needs to be different from the old password."

	new_password = hash_password(password_in)
	result = password_reset_request(user_status, date_now, email_in, reason_in, old_password, new_password)
	
	if result == "Success":
		return "Your request was submitted. Kindly wait while we process it."
	else:
		return result