# This file is typically the entry page to a multipage app using Dash Page -- https://dash.plotly.com/urls#dash-pages
# More multipage app examples by Ann Marie: https://github.com/AnnMarieW/dash-multi-page-app-demos
# Here is some code to get started:

from flask import Flask, request, redirect, session, url_for, flash, render_template
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import dash
from dash import dcc, html, Input, Output, State, ALL
from utils.login_handler import restricted_page
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()
#
#
#
# ## SERVER CONFIGURATION AND INITIALISATION
#
# server = Flask(__name__)
# server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
# server.config.update(SECRET_KEY=os.environ.get('SECRET_KEY'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# db = SQLAlchemy(server)
#
#
#
#
# global_username = ''
#
# ## Creating the USER Model and the Database
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     def __repr__(self):
#         return f"User('{self.id}', '{self.username}', '{self.password}', '{self.registration_date}')"
#
# with server.app_context():
#     db.create_all()
#
# ## Routing For Login and Registartion and Logout
# alert = False
# count_message = 0
#
# @server.route('/register', methods=['POST', 'GET'])
# def register_route():
#     global alert
#     global count_message
#     if request.form:
#         data = request.form
#         with server.app_context():
#             # if User.query.all() == []:
#             user = User(username=data['username'], password=data['password'])
#             db.session.add(user)
#             db.session.commit()
#             alert=True
#             count_message = 0
#         return redirect('/login')
#
#
# @server.route('/login', methods=['POST'])
# def login():
#     global global_username
#     if request.form:
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user is None or user.password != password:
#             return """invalid username and/or password <a href='/login'>login here</a>"""
#         login_user(user)
#         if 'url' in session:
#             if session['url']:
#                 url = session['url']
#                 session['url'] = None
#                 return redirect(url) ## redirect to target url
#         return redirect('/internal') ## redirect to home
#
#
# @server.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('/'))
#
#
#
# # Login manager object will be used to login / logout users
# login_manager = LoginManager()
# login_manager.init_app(server)
# login_manager.login_view = "login"
#
# @login_manager.user_loader
# def load_user(username):
#     u = User.query.get(username)
#     return u
#
# load_figure_template("yeti")
#
# # The DASH APP
# app = dash.Dash(
#     __name__, server=server, use_pages=True, suppress_callback_exceptions=True,
#     external_stylesheets=[dbc.themes.YETI, dbc.icons.BOOTSTRAP]
# )
# app.config["suppress_callback_exceptions"] = True
#
# server = app.server
#
# home_page = dbc.NavLink(html.Div("Home", className="fw-bolder fs-5 text"), href="/", active="exact")
# internal_page = dbc.NavLink(html.Div("Internal", className="fw-bolder fs-5 text"), href="/internal", active="exact")
# insights_page = dbc.NavLink(html.Div("Insights", className="fw-bolder fs-5 text"), href="/insights", active="exact")
# application_page = dbc.NavLink(html.Div("Application", className="fw-bolder fs-5 text"), href="/application", active="exact")
# register_page = dbc.NavLink(html.Div("Register", className="fw-bolder fs-5 text"), href="/register", active="exact")
# login_page = dbc.NavLink(html.Div("Login", className="fw-bolder fs-5 text"), href="/login", active="exact")
# logout_page = dbc.NavLink(html.Div("Logout"), href="/logout", active="exact")
# menue = dbc.NavLink(dbc.DropdownMenu(children=
#             [dbc.DropdownMenuItem("Settings", id='placeholder', className="fw-bolder"), dbc.DropdownMenuItem("Logout", href='/logout', className="fw-bold")],
#             label="Profile",
#             nav=True,
#             className="fw-bolder fs-5 text"
#                     ),
#              active="exact"
#             )
#
# toggle_button = dbc.Button(
#     id="navbar-toggle"
# )
#
#
#
#
#
# sidebar = dbc.Nav(
#             [
#                 toggle_button,
#                 html.Br(),
#                 html.Br(),
#                 html.Div(home_page),
#                 html.Div(id="internal-page"),
#                 html.Div(id="insights-page"),
#                 html.Div(id="register-page"),
#                 html.Div(id="login-page"),
#                 html.Div(id="sales-profit-scatter"),
#                 html.Div(id="application-page"),
#                 html.Div(id="menu", className="text-danger"),
#                 html.Br(),
#                 html.Br(),
#                 html.Br(),
#                 html.Br(),
#                 html.Hr(),
#             ],
#             navbar=True,
#             vertical=True,
#             pills=True,
#             className="border border-2 shadow",
# style={'height': '100vh', 'background-color': '#EAECEE'},
#     )
#
# collapse = dbc.Collapse(sidebar, id="navbar-collapse", is_open=True)
#
#
# app.layout = dbc.Container([
#     dbc.Row(
#         [
#             dbc.Col(
#                 [
#                     # toggle_button,
#                     sidebar,
#                     dcc.Location(id="url") ## THE PATH ELEMENT
#                 ], width=2, style={'height': '100%'}, className='mt-1'),
#             dbc.Col(
#                 dash.page_container, width=10
#             )
#         ],
#             className='my-2', style={'height': '100%'}
#     )
# ], fluid=True, style={'background-color': '#F4F6F7'})
#
#
# @app.callback(
#      Output("register-page", "children"),
#      Output("login-page", "children"),
#      Output("internal-page", "children"),
#      Output("application-page", "children"),
#      Output("menu", "children"),
#      Output('url', 'pathname'),
#      Output('insights-page', 'children'),
#      Input("url", "pathname"),
#      Input({'index': ALL, 'type':'redirect'}, 'n_intervals'),
#     prevent_initial_call=True
# )
# def update_authentication_status(path, n):
#     global popovers
#     ### logout redirect
#     if n:
#         if not n[0]:
#             return '', '', '', '', '', dash.no_update, ''
#         else:
#             return '', '', '', '', '', '/', ''
#
#     ### test if user is logged in
#     if current_user.is_authenticated:
#         if path == '/login':
#             return '', '',  internal_page, application_page, menue, '/', insights_page
#
#         if path == '/summary':
#             return '', '', internal_page, application_page, menue, dash.no_update, insights_page
#
#         return '', '', internal_page, application_page, menue,  dash.no_update, insights_page
#     else:
#         ### if page is restricted, redirect to login and save path
#         if path in restricted_page:
#             session['url'] = path
#             return register_page, login_page, '', '', '', '/login', ''
#
#     ### if path not login and logout display login link
#     if current_user and path not in ['/register', '/login', '/logout']:
#         return register_page, login_page, '', '', '', dash.no_update, ''
#     elif path == '/register':
#         return register_page, login_page, '', '', '', dash.no_update, ''
#
#     ### if path login and logout hide links
#     if path in ['/login', '/logout', '/register']:
#         return register_page, login_page, '', '', '', dash.no_update, ''
#
# @app.callback(
#     Output("username", "children"),
#     Input('url', 'pathname'))
# def current_username(url):
#     if url == '/internal' and current_user.is_authenticated:
#         current_username = "Welcome, " + current_user.username + '!'
#         return current_username
#
#
# @app.callback(
#     Output("the_alert", "children"),
#     Input("url", "pathname"))
# def toggle_modal(path):
#     alert_message = dbc.Alert("User registered successfully", color="#2e8cbc",
#                               dismissable=True, className="text-center fw-bold")
#     global count_message
#     if path == '/login' and alert == True and count_message == 0:
#         count_message = 1
#         return alert_message
#     return dash.no_update

from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
import dash

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP],
    use_pages=True,
    pages_folder="pages",
    prevent_initial_callbacks=True,
)

########### Navbar design section####################
# dropdown w/ quick links to navigate to the other pages
quickLinksLabels = {
    "Homepage": "Home",
    "Data-insights": "WATCHTOWER Insights",
    "Application": "Become a part of WatchTower",
    "Internal": "Internal",
}

nav = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(quickLinksLabels[page["name"]], href=page["path"])
        for page in dash.page_registry.values()
        if (page["module"] != "pages.not_found_404")
        # if (page["module"] != "pages.not_found_404") & (page["name"] != "Internal")
    ],
    nav=True,
    in_navbar=True,
    label="Quick Links",
    className="me-5 text-primary fw-bold",
)
# assembly the navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    src=dash.get_asset_url("VOSTEU_WatchTowerLogo.png"),
                                    height="30px",
                                ),
                                
                            ],
                            className="me-2 text-primary",
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "WatchTower: Disinformation Reporting Platform",
                                className="ms-2 text-primary",
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
            ),
            nav,
        ]
    ),
    dark=True,
    className="opacity-100 p-2  text-white fw-bold rounded",
)

# page container
content = html.Div(id="page-content", children=[page_container], className="content")

# main app layout
app.layout = dbc.Container(
    [dbc.Row([dbc.Col([navbar, content], width=12)])],
    fluid=False,
    style={},
    className="bg-opacity-10 p-2 bg-primary text-dark fw-bold rounded border border-light mh-100",
)


if __name__ == "__main__":
    app.run_server(debug=True)
