import dash
from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_mantine_components as dmc


dash.register_page(__name__)


layout =  dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        html.H1("Please register here if you want to assist."),
        ]
)