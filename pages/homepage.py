import dash_bootstrap_components as dbc
from dash import html, dcc
import dash

dash.register_page(__name__, path="/", order=0)

########### Accordion design section ####################
# accordion items for each action - no direct access to the internal page
accordion = html.Div(
    [
        html.H4(
            "WatchTower by VOST Europe",
            className="text-primary fw-bold mt-3 ms-5 ",
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P(
                            "By facilitating a centralized repository of disinformation reports, WATCHTOWER enhances transparency and accountability among online entities, ultimately contributing to more effective detection and mitigation of disinformation on a global scale."
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
                            "To ensure the integrity and effectiveness of our platform, WATCHTOWER implements a thorough registration process for new users. Entities that are already signatories of the Code of Practice on Disinformation benefit from a streamlined, fast-track registration, acknowledging their established commitment to combating disinformation. Non-signatory participants will undergo a standard vetting process, ensuring that all contributors are equipped and dedicated to maintaining the highest standards of information accuracy."
                        ),
                        # dbc.Button("Don't click me!", color="danger"),
                        dcc.Link("Go to the application page", href="/application"),
                    ],
                    title="Become a WATCHTOWER user",
                    className="bg-opacity-10 me-5  ms-5  mt-3 border-primary border-1 bg-primary text-primary  rounded",
                ),
                dbc.AccordionItem(
                    [
                        html.P(
                            "In our public analytics dashboard, you can access major insights into the ongoing efforts by WATCHTOWER's users to combat online disinformation. This interactive tool showcases the impact and reach of collective actions taken against disinformation, all visualized through publicly available data."
                        ),
                        dcc.Link("Go to data insight page", href="/data-insights"),
                    ],
                    title="WATCHTOWER insights",
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
                                src=dash.get_asset_url("VOSTEU_WATCHTOWER_TOPBANNER.svg"),
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
