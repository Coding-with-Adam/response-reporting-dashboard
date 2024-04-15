import dash
import os
from dash import Dash, html, dcc, Input, Output, callback
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

#_____________________________App and Server configuration_____________________________#

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets = [dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions = True
    )

server = app.server

#_______________________________Pages Custom Properties_______________________________#

app_pages = [
    {"name" : "Home", "relative_path" : "/", "protected" : False, "show_to_active_user" : True},
    {"name" : "Data Insights", "relative_path" : "/data-insights", "protected" : False, "show_to_active_user": True},
    {"name" : "Application", "relative_path" : "/application", "protected" : False, "show_to_active_user": False},
    {"name" : "Internal", "relative_path" : "/internal", "protected" : True, "show_to_active_user" : True},
    {"name" : "Login", "relative_path" : "/login", "protected" : False, "show_to_active_user":False},
    {"name" : "Logout", "relative_path" : "/login", "protected" : True, "show_to_active_user":True}
]

#___________________________________Navigation bar___________________________________#

logo_path = os.path.join("assets", "vost_logo.png")
logo = html.Img(src = logo_path, height = "60px")
brand = dbc.NavbarBrand("VOST Europe - Response Reporting Platform")

theme_switch = dmc.Switch(label = "Dark", id = "id_theme_switch", checked = True)

navigation_bar = dbc.Navbar([
    dbc.Container([
        dbc.Row([
            dbc.Col(logo),
            dbc.Col(brand)
            ],
            align = 'center'
            ),
        dbc.Nav(
            id = "id_navigation_pages",
            navbar = True,
            #pills = True,  #To fill the active nav button
            ),
        dbc.Row([
            theme_switch])
        ],
        fluid = True
        )
    ],
    color = "dark",
    dark = True,
    sticky = 'top',
    style = {"height":"60px"}
    )

#___________________________________App body___________________________________#


app.layout = dmc.MantineProvider([
    dcc.Store(id="id_session_data", storage_type = "session", data = {}),
    navigation_bar,
    dash.page_container,
    dbc.Row(id="id_app_test_output")
    ],
    id = "id_app_layout",
    theme = {"colorScheme": "dark"},
    withGlobalStyles = True
    )

#___________________________________Callbacks___________________________________#

@callback(
    Output("id_app_layout", "theme"),
    Input("id_theme_switch", "checked")
    )
def switch_app_theme(dark_theme_active):
    if dark_theme_active == False:
        return {"colorScheme": "white"}
    return {"colorScheme": "dark"}

@callback(
    Output("id_navigation_pages", "children"),
    Input("id_session_data", "data")
    )
def update_navbar_pages(user_data):
    logged_email = user_data.get("user_email", None)

    if logged_email:
        users_pages = [
        dbc.NavItem(
            dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = "exact")
            ) for page in app_pages if page["show_to_active_user"] == True
        ]
        return users_pages
    else:
        public_pages = [
        dbc.NavItem(
            dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = "exact")
            ) for page in app_pages if page["protected"] == False
        ]
        return public_pages

#___________________________________Serve app___________________________________#

if __name__ == '__main__':
    app.run(debug=True)
