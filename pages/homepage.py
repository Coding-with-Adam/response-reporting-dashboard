import dash_bootstrap_components as dbc
from dash import html, dcc
import dash

dash.register_page(__name__, path="/", order=0)

########### Accordion design section ####################
# accordion items for each action - no direct access to the internal page
accordion = html.Div(
    [
        html.H4(
            "VOST Fight Against Disinformation",
            className="text-primary fw-bold mt-3 ms-5 ",
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P(
                            "Provide support in hoax and abusive behavior, disinformation and misinformation detection, by monitoring multiple channels and by establishing direct communication channels with online platforms"
                        ),
                        dcc.Link(
                            "Learn more",
                            href="https://vosteurope.org/",
                            target="_blank",
                        ),
                    ],
                    title="Core Mission",
                    className="bg-opacity-10 me-5  ms-5  mt-3 border-primary border-1 bg-primary text-primary  rounded",
                ),
                dbc.AccordionItem(
                    [
                        html.P(
                            "A registration process is needed to become a vetted user"
                        ),
                        # dbc.Button("Don't click me!", color="danger"),
                        dcc.Link("Go to the application page", href="/application"),
                    ],
                    title="Apply to Volunteer",
                    className="bg-opacity-10 me-5  ms-5  mt-3 border-primary border-1 bg-primary text-primary  rounded",
                ),
                dbc.AccordionItem(
                    [
                        html.P(
                            "Analytics dashboard for trending reports, data drill-down, highlight outstanding issue"
                        ),
                        dcc.Link("Go to data insight page", href="/data-insights"),
                    ],
                    title="Data Insights",
                    className="bg-opacity-10 me-5  ms-5  mt-3 mb-5 border-primary border-1 bg-primary text-primary  rounded",
                ),
            ],
            start_collapsed=True,
        ),
    ],
    className=" border border-primary border-1 text-primary fw-bold rounded ",
)
# assembly the home page layout - banner and accordion instantiation
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Container(
                            html.Img(
                                src=dash.get_asset_url("Banner.png"),
                                style={
                                    "margin-left": "auto",
                                    "margin-right": "auto",
                                    "display": "block",
                                    "width": "100%",
                                },
                            ),
                            className="p-2 ",
                            fluid=False,
                        ),
                    ],
                ),
            ],
            align="center",
        ),
        # html.Br(),
        dbc.Row(
            [
                dbc.Col([], width=2),
                dbc.Col(
                    [
                        dbc.Container(
                            accordion,
                            fluid=False,
                        ),
                    ],
                    width=8,
                ),
                dbc.Col([], width=2),
            ],
            align="center",
            className=" p-5",
        ),
    ],
)
