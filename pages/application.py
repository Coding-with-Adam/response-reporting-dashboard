# This application page will be built later later in April

import dash
from dash import html
dash.register_page(__name__, path="/application")


layout = html.Div(
    [
        html.H1('Join Us', className="text-center mt-3 fw-bolder", style={'color': '#2471A3'}),

    ]
)