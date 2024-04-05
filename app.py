import dash
import os
from dash import Dash, html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets = [dbc.themes.BOOTSTRAP])

#___________________________________Navigation bar___________________________________#

logo_path = os.path.join("assets", "vost_logo.png")
logo = html.Img(src = logo_path, height = "60px")
brand = dbc.NavbarBrand("VOST Europe - Response Reporting Platform")

navigation_pages = [
            dbc.NavItem(
                dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = 'exact')
                )
            for page in dash.page_registry.values()
            ]

navigation_bar = dbc.Navbar([
    dbc.Container([
        dbc.Row([
            dbc.Col(logo),
            dbc.Col(brand)
            ],
            align = 'center'),
        dbc.Nav(
            navigation_pages,
            navbar = True),
        ],
        fluid = True)
    ],
    color = "dark",
    dark = True,
    sticky = 'top',
    style = {"height":"60px"})

#___________________________________App body___________________________________#


app.layout = dmc.MantineProvider(
    theme = {"colorScheme": "dark"},
    withGlobalStyles = True,
    children = [
    navigation_bar,
    dash.page_container
    ]
    )

#___________________________________Serve app___________________________________#

if __name__ == '__main__':
    app.run(debug=True)
