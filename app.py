# This file is typically the entry page to a multipage app using Dash Page -- https://dash.plotly.com/urls#dash-pages
# More multipage app examples by Ann Marie: https://github.com/AnnMarieW/dash-multi-page-app-demos
# Here is some code to get started:

from flask import Flask, request, redirect, session, url_for, flash, render_template
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, page_container, ctx
import dash_bootstrap_components as dbc
from utils.login_handler import restricted_page
from dash_bootstrap_templates import load_figure_template
from datetime import datetime, timedelta


global_username = ''
## Routing For Login and Registartion and Logout


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
server.config.update(SECRET_KEY='5791628bb0b13ce0c676dfde280ba245')
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(server)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.password}', '{self.registration_date}')"

with server.app_context():
    db.create_all()


@server.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('/'))



# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(username):
    u = User.query.get(username)
    return u

load_figure_template("spacelab")

app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP],
    use_pages=True,
    # pages_folder="pages",
    suppress_callback_exceptions=True
)

server = app.server

########### Navbar design section####################
# dropdown w/ quick links to navigate to the other pages
home_page = dbc.NavLink(html.Div("Home", className="fw-bold fs-6 text"), href="/", active="exact")
internal_page = dbc.NavLink(html.Div("Internal", className="fw-bold fs-6 text"), href="/internal", active="exact")
insights_page = dbc.NavLink(html.Div("Insights", className="fw-bold fs-6 text"), href="/insights", active="exact")
application_page = dbc.NavLink(html.Div("Application", className="fw-bold fs-6 text"), href="/application", active="exact")
register_page = dbc.NavLink(html.Div("Register", className="fw-bold fs-6 text"), href="/register", active="exact")
login_page = dbc.NavLink(html.Div("Login", className="fw-bold fs-6 text"), href="/login", active="exact")
logout_page = dbc.NavLink(html.Div("Logout", className="fw-bold fs-6 text"), href="/logout", active="exact")



nav = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(home_page),
        dbc.DropdownMenuItem(insights_page),
        dbc.DropdownMenuItem(application_page),
        dbc.DropdownMenuItem(id='pg1'),
        dbc.DropdownMenuItem(id='pg2'),
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
            dcc.Location(id="url")
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

@app.callback(
    Output("username-input", "invalid"),
    Output("password-input", "invalid"),
    Output("username_feedback_message", "children"),
    Output("the_alert", "children"),
    Input("registration_submit_button", "n_clicks"),
    State("username-input", "value"),
    State("password-input", "value"),
)
def register_user(button, username, password):
    alert_message = dash.no_update
    if "registration_submit_button" == ctx.triggered_id:
        if (username == None or username == '') and (password == None or password == ''):
            return True, True, 'username cannot be empty', alert_message
        if username == None or username == '':
            return True, False, 'username cannot be empty', alert_message
        if password == None or password == '':
            return False, True, '', alert_message
        if User.query.first() is not None:
                if User.query.filter_by(username=username).first() is not None:
                    return True, False, 'username already exists', alert_message
        with server.app_context():
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            alert_message = dbc.Alert("User registered successfully", color="#2e8cbc",
                                      dismissable=True, className="text-center fw-bold")
    return False, False, '', alert_message


@app.callback(
    Output("login-username-input", "invalid"),
    Output("login-password-input", "invalid"),
    Output('login-test', 'children'),
    Input("login-submit-button", "n_clicks"),
    State("login-username-input", "value"),
    State("login-password-input", "value"),
)
def login_the_user(button, username, password):
    if ctx.triggered_id == 'login-submit-button':
        if (username == None or username == '') and (password == None or password == ''):
            return True, True, dash.no_update
        if username == None or username == '':
            return True, False, dash.no_update
        if password == None or password == '':
            return False, True, dash.no_update
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return True, True, dash.no_update
        login_user(user)
        return False, False, ' '
    return False, False, dash.no_update

@app.callback(Output('url', 'pathname'),
              Input('login-test', 'children'))
def route_login(input):
    if input == ' ':
        return '/internal'
    return dash.no_update

@app.callback(
     Output("pg1", "children"),
     Output("pg2", "children"),
     Output('url', 'pathname', allow_duplicate=True),
     Input("url", "pathname"),
     Input({'index': ALL, 'type':'redirect'}, 'n_intervals'),
    prevent_initial_call=True
)
def update_authentication_status(path, n):
    if n:
        if not n[0]:
            return '', '', dash.no_update,
        else:
            return '', '', '/'

    ### test if user is logged in
    if current_user.is_authenticated:
        if path == '/login':
            return internal_page, logout_page, '/',

        return internal_page, logout_page, dash.no_update
    else:
        ### if page is restricted, redirect to login and save path
        if path in restricted_page:
            session['url'] = path
            return login_page, '', '/login'

    ### if path not login and logout display login link
    if current_user and path not in ['/register', '/login', '/logout']:
        return login_page, '', dash.no_update
    elif path == '/register':
        return login_page, '', dash.no_update

    ### if path login and logout hide links
    if path in ['/login', '/logout', '/register']:
        return login_page, '', dash.no_update


@app.callback(
    Output("username", "children"),
    Input('url', 'pathname'))
def current_username(url):
    if url == '/internal' and current_user.is_authenticated:
        current_username = "Welcome, " + current_user.username + '!'
        return current_username


if __name__ == "__main__":
    app.run_server(debug=True)
