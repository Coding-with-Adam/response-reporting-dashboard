from dash import Dash, html, dcc, Input, Output, callback, ctx, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path = '/')

header_text = """
[VOST EUROPE](https://vosteurope.org/), more than an organisation, is a showcase of what citizens
from different countries can do with the objective to have a society that is more prepared,
more informed, and more resilient to natural disasters and other events, across the European Space.
"""

body_text = """
VOST’s core mission is to:

1. Use online platforms to inform citizens in the areas of Disaster Risk Management(DRM), Disaster Risk
Preparedness (DRP)
2. To support official entities in case of a natural disasters our man-made disruptive events, with an
impact on society, with information gathering and dissemination of official information
3. Provide support in hoax and abusive behavior, disinformation and misinformation detection, 
by monitoring multiple channels and by establishing direct communication channels with online platforms
"""
footer_text = """
**CONTACT US.**
---
You may contact us by sending us an [email](vosteu@vost.pt) and we will get back to you as soon 
as possible.
You can also reach us on [twitter](https://twitter.com/VOSTeurope) or
[facebook](https://www.facebook.com/Vostpt).
"""

home_page_card = dbc.Card([
	dbc.CardHeader([
		dcc.Markdown([header_text])
		]),
	dbc.CardBody([
		dcc.Markdown([body_text])
		]),
	dbc.CardFooter([
		dcc.Markdown([footer_text])
		])
	])

layout = dbc.Container([
	html.Hr(),
	dbc.Row([
		dbc.Col([html.H1("Wellcome to VOST Response Reporting App", style = {"text-align":"center"})])
		]),
	html.Hr(),
	dbc.Row([
		dbc.Col([home_page_card])
		]),
	dbc.Row([
		])
	],
	fluid = True)