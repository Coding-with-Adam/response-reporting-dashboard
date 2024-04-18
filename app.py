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

logo_path = os.path.join("assets", "VOSTEU_WatchTowerLogo.png")
logo = html.Img(src = logo_path, height = "60px")
brand = dbc.NavbarBrand("WatchTower: Disinformation Reporting Platform")

theme_switch = dmc.Switch(label = "Dark", id = "id_theme_switch", checked = True)
active_user = html.P(id="id_active_user_name")

navigation_bar = dbc.Navbar([
    dbc.Container([
        dbc.Row([
            dbc.Col(logo),
            dbc.Col(brand),
            ],
            align = 'center'
            ),
        dbc.Row([dbc.Col(active_user)], className = "ms-auto mt-3 flex-nowrap"),
        dbc.Nav(
            id = "id_navigation_pages",
            navbar = True,
            className = "ms-auto",
            #ms-auto pushes the content to the right most side of the navigation bar
            ),
        dbc.Row([theme_switch]),
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
def update_navbar_pages(session_data):
    authenticated = session_data.get("is_authenticated", False)

    if authenticated:
        protected_pages = [
        dbc.NavItem(
            dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = "exact")
            ) for page in app_pages if page["show_to_active_user"] == True
        ]
        return protected_pages
    else:
        public_pages = [
        dbc.NavItem(
            dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = "exact")
            ) for page in app_pages if page["protected"] == False
        ]
        return public_pages

@callback(
    Output("id_active_user_name", "children"),
    Input("id_session_data", "data"),
    prevent_initial_call = True
    )
def user_greetings(session_data):
    user_full_name = session_data.get("full_name", "")
    if user_full_name:
        return f"Hi, {user_full_name}"

#___________________________________Serve app___________________________________#

if __name__ == '__main__':
    app.run(debug=True)
