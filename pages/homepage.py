from dash import Dash, html, dcc, Input, Output, callback, ctx, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path = '/')

layout = dbc.Container([
	dbc.Row([]),
	dbc.Row([]),
	dbc.Row([])
	])