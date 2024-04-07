import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__)



username_input = html.Div(
    [
        dbc.Label("Username"),
        dbc.Input(type="text", id="username", placeholder="Enter username", name="username"),
    ],
    className="mb-3 form-group",
)

password_input = html.Div(
    [
        dbc.Label("Password"),
        dbc.Input(
            type="password",
            id="password",
            placeholder="Enter password", name="password"
        ),
    ],
    className="mb-3 form-group",
)

button_input = html.Div(
dbc.Button('Sign up', id='submit_button', type='submit'),
    className= "mb-3 form-group"
)



layout = html.Div([
    html.H2("Create an Account", className="my-4 text-center"),
    html.Form([username_input, password_input, button_input], method='POST')
     ],
    className="mx-auto col-10 col-md-8 col-lg-6"
)
