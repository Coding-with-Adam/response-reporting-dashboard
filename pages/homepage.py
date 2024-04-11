import dash
import dash_mantine_components as dmc
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__,path='/')

layout =  dbc.Container(
    children=[
        html.H1("Welcome to the VOST page"),
    ]
)
