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
    "Data-insights": "Data Insights",
    "Application": "Apply to Volunteer",
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
                                    src=dash.get_asset_url("VOST_LOGO.png"),
                                    height="30px",
                                ),
                                html.Img(
                                    src=dash.get_asset_url("VOST_EU.png"), height="30px"
                                ),
                            ],
                            className="me-2 text-primary",
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Response Reporting Platform",
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
    className="bg-opacity-10 p-2 bg-primary text-dark fw-bold rounded border border-light vh-100",
)


if __name__ == "__main__":
    app.run_server(debug=True)
