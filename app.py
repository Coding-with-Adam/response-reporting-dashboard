# This file is typically the entry page to a multipage app using Dash Page -- https://dash.plotly.com/urls#dash-pages
# More multipage app examples by Ann Marie: https://github.com/AnnMarieW/dash-multi-page-app-demos
# Here is some code to get started:

import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Response Reporting Platform -- VOST Europe'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
