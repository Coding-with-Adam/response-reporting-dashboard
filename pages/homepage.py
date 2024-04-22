from dash import html, dcc, callback, Input, Output, ctx
import dash_bootstrap_components as dbc
import dash
import pandas as pd

dash.register_page(__name__, path="/", order=0)

##### success story cards and container ###############


card_icon = {
    "color": "primary",
    "textAlign": "center",
    "fontSize": 80,
    "margin": "auto",
}

###### card data prep #######
# Active Users
df = pd.read_csv(
    "https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/dummy_data_1000_wNan.csv"
)

activeUsers = "{0}".format(df["Reporting User"].nunique())
# update time footnote
updateTime = (
    f"Last Update on {pd.to_datetime(pd.Timestamp.today()).strftime('%Y-%m-%d')}"
)
# submitted reports
submittedReports = f"{df.shape[0]}"
# success rate
successRate = "{0}%".format(100 * (df[df["Appeal"] == "No"].shape[0] / df.shape[0]))
# turnaround Time
avgTurnAroundTime = "{0} days".format(
    (
        int(
            (pd.to_datetime(df["Answer Date"]) - pd.to_datetime(df["Timestamp"]))
            .dropna()
            .astype(str)
            .str.replace(" days", "")
            .astype(int)
            .mean()
        )
    )
)


def create_card(ico, title, value, note):
    card = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                # dbc.CardImg(
                                #     src=dash.get_asset_url("VOST_LOGO.png"),
                                #     className="img-fluid rounded-start",
                                # ),
                                html.I(className=ico),
                                className="col-md-4 ",
                                style=card_icon,
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(title, className="card-title"),
                                        html.H1(
                                            value,
                                            className="card-text",
                                        ),
                                        html.Small(
                                            note,
                                            className="card-text text-muted",
                                        ),
                                    ]
                                ),
                                className="col-md-8 ",
                            ),
                        ],
                        className="g-0 d-flex align-items-center",
                    )
                ],
                className="mb-3 bg-opacity-10  mt-3 shadow my-2 bg-light text-primary  rounded  ",
            ),
            dbc.Card(
                className="mb-3 mt-3 bg-primary shadow my-2 bg-opacity-80  ",
                style={"maxWidth": 75},
            ),
        ],
        className="",
    )

    return card


# create card instances
card1 = create_card(
    "bi bi-sunrise-fill me-2",
    "Active Since",
    "January 2023",
    "A new tool against disinformation",
)
card2 = create_card(
    "bi bi-graph-up-arrow  me-2", "Active Users", activeUsers, updateTime
)
card3 = create_card(
    "bi bi-file-text-fill me-2", "Submitted Reports", submittedReports, updateTime
)
card4 = create_card("bi bi-trophy-fill me-2", "Success Rate", successRate, updateTime)
card5 = create_card(
    "bi bi bi-clock-history me-2", "Avg Turnaround Time", avgTurnAroundTime, updateTime
)


########### Accordion design section ####################
# dropdown w/ quick links to navigate to the other pages
accordion = html.Div(
    [
        html.H2(
            "Discover More ",  # "VOST Fight Against Disinformation",
            className="text-primary fw-bold  ms-5 ",
        ),
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        html.P(
                            "Provide support in hoax and abusive behavior, disinformation and misinformation detection, by monitoring multiple channels and by establishing direct communication channels with online platforms"
                        ),
                        dcc.Link("Learn more", href="https://vosteurope.org/"),
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
                # dbc.AccordionItem(
                #     [
                #         html.P("Note social media reports. For vetted users only"),
                #         dcc.Link("Go reports input page", href="/internal"),
                #     ],
                #     title="Note Social Media Report",
                #     className="bg-opacity-10 me-5  ms-5  mt-3 mb-5 border-primary border-1 bg-primary text-primary  rounded",
                # ),
            ],
            start_collapsed=True,
        ),
    ],
    className="  text-primary fw-bold ",
)
# assembly the home page layout - banner and accordion instantiation
layout = dbc.Container(
    [
        dcc.Interval(
            id="card_interval-id",
            disabled=False,
            n_intervals=0,
            interval=1 * 3000,
        ),
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
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col([], width=1),
                                        dbc.Col(
                                            html.H2(
                                                "VOST Facts ",
                                                className="text-primary fw-bold mt-2 ms-5 m",
                                            ),
                                            width=8,
                                        ),
                                    ],
                                    align="center",
                                    className=" me-5 ms-5",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col([], width=1),
                                        dbc.Col(
                                            dbc.Container(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col([], width=2),
                                                            dbc.Col(
                                                                [card1],
                                                                id="card-id",
                                                                width=7,
                                                            ),
                                                            dbc.Col([], width=3),
                                                        ],
                                                        className="my-4 ",
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                [
                                                                    dbc.Pagination(
                                                                        max_value=0,
                                                                        first_last=True,
                                                                        previous_next=True,
                                                                        id="pagination-id",
                                                                    ),
                                                                ],
                                                                width=1,
                                                            ),
                                                        ],
                                                        className="",
                                                        align="center",
                                                    ),
                                                ],
                                                fluid=False,
                                                className="",
                                            )
                                        ),
                                    ],
                                    align="center",
                                    className=" ",
                                ),
                                dbc.Row(
                                    [dbc.Col(html.Hr())],
                                    align="center",
                                    className=" ",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col([], width=1),
                                        dbc.Col(
                                            [
                                                dbc.Container(
                                                    accordion,
                                                    fluid=False,
                                                ),
                                            ],
                                            width=10,
                                        ),
                                        dbc.Col([], width=1),
                                    ],
                                    align="center",
                                    className=" p-5",
                                ),
                            ],
                            className=" shadow text-primary fw-bold rounded p-5  ",
                        )
                    ],
                    width=10,
                )
            ],
            align="center",
            class_name="mt-3 d-flex justify-content-center",
        ),
    ],
    className=" vh-100",
)


@callback(
    Output("card-id", "children"),
    [
        Input("pagination-id", "active_page"),
        Input("card_interval-id", "n_intervals"),
    ],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def change_page(page, num):
    event_in = ctx.triggered_id

    pageMap = {"k3": card3, "k1": card1, "k2": card2, "k4": card4, "k5": card5}
    if event_in == "pagination-id":

        if page > 5:
            page = 1
        currentCard = pageMap[f"k{page}"]
        print(type(page))
    else:
        page = num % 5 + 1
        # pageMap = {"k3": card3, "k1": card1, "k2": card2, "k4": card4}
        # if page > 4:
        #     page = 1
        currentCard = pageMap[f"k{page}"]
    print(type(page))
    return currentCard
