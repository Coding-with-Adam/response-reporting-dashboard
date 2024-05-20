import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__)

username_input = html.Div(
    [
        dbc.Label("Username"),
        dbc.Input(type="text", id="username-input", placeholder="Enter username", name="username"),
        dbc.FormFeedback(id="username_feedback_message", type="invalid"),
    ],
    className="mb-3 form-group",
)

password_input = html.Div(
    [
        dbc.Label("Password"),
        dbc.Input(type="password", id="password-input", placeholder="Enter password", name="password"),
        dbc.FormFeedback("Password cannot be empty", type="invalid"),
    ],
    className="mb-3 form-group",
)

button_input = html.Div(
dbc.Button('Sign up', id='registration_submit_button', type='submit'),
    className="mb-3 form-group"
)



layout = html.Div([
    html.Div(id="the_alert", children=[]),
    html.H2("Create an Account", className="my-4 text-center"),
    html.Div([username_input, password_input, button_input]),
    html.Br(),
    dcc.Link("Already have an account?", href="/login"),
     ],
    className="mx-auto col-10 col-md-8 col-lg-6"
)
