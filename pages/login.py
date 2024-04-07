import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__)



username_input = html.Div(
    [
        dbc.Label("Username"),
        dbc.Input(type="text", id="uname-box", placeholder="Enter username", name="username"),
    ],
    className="mb-3 form-group",
)

password_input = html.Div(
    [
        dbc.Label("Password"),
        dbc.Input(
            type="password",
            id="pwd-box",
            placeholder="Enter password", name="password"
        ),
    ],
    className="mb-3 form-group",
)

button_input = html.Div(
dbc.Button('Login', id='login_button', type='submit', n_clicks=0),
    className= "mb-3 form-group rounded-0"
)


layout = html.Div([
    html.Div(id="the_alert", children=[]),
    html.Div(children="", id="output-state"),
    html.H2("Login", className="my-4 text-center"),
    html.Form([username_input, password_input, button_input], method='POST'),
html.Br(),
    dcc.Link("Don't have an account?", href="/register"),
    html.Br(),
html.Br(),
    dcc.Link("Forgot your Password?", href="/register")
     ],
    className="mx-auto col-10 col-md-8 col-lg-6"
)

