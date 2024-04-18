from dash import Dash, html, dcc, Input, Output, callback, ctx, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path = '/', redirect_from = ["/home", "/home_page"])

#_____________________________________Accordion Items_____________________________________#

mission_accordion = dbc.AccordionItem([
	html.P("""
		By facilitating a centralized repository of disinformation reports, 
		WATCHTOWER enhances transparency and accountability among online entities, ultimately contributing 
		to more effective detection and mitigation of disinformation on a global scale.
	"""),
	dcc.Link(
		"Learn more",
		href = "https://vosteurope.org/",
		target = "_blank"
		)
	],
	title = "Core Mission"
	)

application_page_accordion = dbc.AccordionItem([
	html.P("""
		To ensure the integrity and effectiveness of our platform, WATCHTOWER implements a thorough
		registration process for new users. Entities that are already signatories of the Code of Practice
		on Disinformation benefit from a streamlined, fast-track registration, acknowledging their
		established commitment to combating disinformation. Non-signatory participants will undergo a
		standard vetting process, ensuring that all contributors are equipped and dedicated to maintaining
		the highest standards of information accuracy.
		"""),
	dcc.Link(
		"Go to the application page",
		href="/application"
		)
	],
	title = "Become a WATCHTOWER user"
	)

insights_page_accordion = dbc.AccordionItem([
	html.P("""
		 In our public analytics dashboard, you can access major insights into the ongoing efforts 
		 by WATCHTOWER's users to combat online disinformation. This interactive tool showcases the 
		 impact and reach of collective actions taken against disinformation, all visualized through 
		 publicly available data.
		"""),
	dcc.Link(
		"Go to data insight page",
		href = "/data-insights")
	],
	title = "WATCHTOWER Insights"
	)

#_____________________________________Home page items_____________________________________#

homepage_title = dbc.Col([
	html.H1(
		"WatchTower by VOST Europe",
		style = {"text-align":"center"}
		)
	])

homepage_accordion = dbc.Accordion([
	mission_accordion,
	application_page_accordion,
	insights_page_accordion,
	],
	start_collapsed = True
	)

#_________________________________________Page Layout_________________________________________#

layout = dbc.Container([
	html.Hr(),
	dbc.Row([
		homepage_title
		]),
	html.Hr(),
	dbc.Row([
		dbc.Col([homepage_accordion]),
		]),
	dbc.Row([
		])
	],
	fluid = True)