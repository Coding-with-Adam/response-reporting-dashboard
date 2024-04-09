import dash
import dash_mantine_components as dmc
from dash import html
dash.register_page(__name__,path='/')

layout =  dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        dmc.Header(
            html.H1("Welcome to the VOST page"),
            height=60,
        ),

        ]
)