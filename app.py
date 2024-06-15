import dash
import os
from dash import Dash, html, dcc, Input, Output, State, callback, exceptions
import dash_bootstrap_components as dbc

#_____________________________App and Server configuration_____________________________#

app = Dash(
    __name__,
    title = "WatchTower",
    use_pages = True,
    external_stylesheets = [dbc.themes.DARKLY, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions = True
    )
app._favicon = os.path.join("assets", "favicon.ico")

server = app.server

#_______________________________Pages Custom Properties_______________________________#

app_pages = [
    {"name" : "Home", "relative_path" : "/", "show_to_public":True, "show_to_users":True, "show_to_admin":True},
    {"name" : "Admin Menu", "relative_path" : "/admin-menu", "show_to_public":False, "show_to_users":False, "show_to_admin":True},
    {"name" : "Data Insights", "relative_path" : "/data-insights", "show_to_public":True, "show_to_users":True, "show_to_admin":True},
    {"name" : "Application", "relative_path" : "/application", "show_to_public":True, "show_to_users":False, "show_to_admin":False},
    {"name" : "Internal", "relative_path" : "/internal", "show_to_public":False, "show_to_users":True, "show_to_admin":True},
    {"name" : "Login", "relative_path" : "/login", "show_to_public":True, "show_to_users":False, "show_to_admin":False},
    {"name" : "Logout", "relative_path" : "/login", "show_to_public":False, "show_to_users":True, "show_to_admin":True}
]

#___________________________________Navigation bar___________________________________#

logo_path = os.path.join("assets", "VOSTEU_WatchTowerLogo.png")
logo = html.Img(src = logo_path, height = "60px")
brand = dbc.NavbarBrand("WatchTower: Disinformation Reporting Platform")

navigation_bar = dbc.Navbar([
    dbc.Container([
        dbc.Row([
            dbc.Col(logo),
            dbc.Col(brand),
            ],
            align = 'center'
            ),
        dbc.Row([dbc.Col(id = "id_navbar_active_user")], className = "ms-auto mt-3 flex-nowrap"),
        dbc.Nav(
            id = "id_navigation_pages",
            navbar = True,
            className = "ms-auto",
            #ms-auto pushes the content to the right most side of the navigation bar
            ),
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


app.layout = dbc.Container([
    dcc.Store(id="id_session_data", storage_type = "local", data = {}),
    navigation_bar,
    dash.page_container,
    ],
    id = "id_app_layout",
    fluid = True
    )

#___________________________________Callbacks___________________________________#

@callback(
    Output("id_navigation_pages", "children"),
    Input("id_session_data", "data"),
    Input("id_app_layout", "children"), #To create navbar pages at startup
    )
def update_navbar_pages(session_data, page_initial_load):
    is_authenticated = session_data.get("is_authenticated", False)
    is_admin = session_data.get("is_admin", False)

    if is_authenticated and is_admin:
        navbar_pages = [
        dbc.NavItem(
            dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = "exact")
            ) for page in app_pages if page["show_to_admin"] == True
        ]
    elif is_authenticated and not is_admin:
        navbar_pages = [
        dbc.NavItem(
            dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = "exact")
            ) for page in app_pages if page["show_to_users"] == True
        ]
    else:
        navbar_pages = [
        dbc.NavItem(
            dbc.NavLink(f"{page['name']}", href = page["relative_path"], active = "exact")
            ) for page in app_pages if page["show_to_public"] == True
        ]
    return navbar_pages

@callback(
    Output("id_navbar_active_user", "children"),
    Input("id_session_data", "data"),
    prevent_initial_call = True
    )
def get_navbar_user(session_data):
    user_full_name = session_data.get("full_name", "")
    user_status = session_data.get("application_decision", "")

    if user_full_name and user_status == "Approved":
        nav_item = html.Span([
            html.Label(className = "fa fa-user"),
            html.P(user_full_name, className = "d-inline-block ms-1")
            ]
            )
        return nav_item

#___________________________________Serve app___________________________________#

if __name__ == '__main__':
    app.run(debug=True)
