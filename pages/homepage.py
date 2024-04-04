from dash import Dash, html, dcc, Input, Output, callback, ctx, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path = '/')

layout = dbc.Container([
	dbc.Row([
		html.H1("Page under construction", style = {"text-align":"center"})
		]),
	dbc.Row([
		]),
	dbc.Row([
		])
	],
	fluid = True)