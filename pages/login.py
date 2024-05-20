import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__)

username_input = html.Div(
    [
        dbc.Label("Username"),
        dbc.Input(type="text", id="login-username-input", placeholder="Enter username", name="username"),
        dbc.FormFeedback(id="login-username-feedback-message", children='username cannot be empty', type="invalid"),
    ],
    className="mb-3 form-group",
)

password_input = html.Div(
    [
        dbc.Label("Password"),
        dbc.Input(type="password", id="login-password-input", placeholder="Enter password", name="password"),
        dbc.FormFeedback("Password cannot be empty", type="invalid"),
    ],
    className="mb-3 form-group",
)

button_input = html.Div(
dbc.Button('Login', id='login-submit-button', type='submit'),
    className= "mb-3 form-group rounded-0"
)


layout = html.Div([
    html.Div(children="", id="output-state"),
    html.H2("Login", className="my-4 text-center"),
    html.Div([username_input, password_input, button_input]),
    html.Br(),
    dcc.Link("Don't have an account?", href="/register"),
html.Div(id='login-test')
     ],
    className="mx-auto col-10 col-md-8 col-lg-6"
)

