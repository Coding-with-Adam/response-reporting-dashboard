import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, callback
import dash
import pandas as pd
import plotly.express as px
import numpy as np

# from datetime import datetime
dash.register_page(__name__, path="/data-insights", order=1, suppress_callback_exceptions=True)


#####################support functions########################
def create_insight_card(title, value, note=""):
    card = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.Row(
                        [
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


################### data retrieval#############################
df = pd.read_csv(
    "https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/dummy_data_10000_wNan.csv"
)

#################### data Prep section#########################
##add extra-cols to df -- for overall views
df["isOpen"] = np.where(df["Answer Date"].isna(), True, False)
df["reportAge"] = (
    (pd.to_datetime(pd.Timestamp.today(), unit="s") - pd.to_datetime(df["Timestamp"]))
    .dropna()
    .astype(str)
    .str.replace(" days.*$", "", regex=True)
).astype(int)
df["reportLifetime"] = (
    (pd.to_datetime(df["Answer Date"]) - pd.to_datetime(df["Timestamp"]))
    .dropna()
    .astype(str)
    .str.replace(" days", "")
    .astype(int)
)
##data aggregation,subset for Report status view container "view1"
group1_1 = df.groupby(by=["Platform", "isOpen"]).count().reset_index()
df1_1 = (
    df[df.isOpen == True]
    .sort_values(by=["reportAge"], ascending=False)
    .reset_index()
    .loc[0:10][["Timestamp", "Platform", "Report Type"]]
)
##data aggregation, subset for Report status view container "view2" #########
group2_1 = df.groupby(by=["Platform", "Report Type"]).count().reset_index()
group2_2 = df.groupby(by=["Platform", "Report Type", "Appeal"]).count().reset_index()
group2_3 = df.groupby(by=["Report Type", "Appeal"]).count().reset_index()
##data aggregation view3
# group3_1 = df.groupby(by=[pd.to_datetime(df["Answer Date"]), "Platform"]).count()
df3_1 = df[["Timestamp", "Reporting User"]].drop_duplicates(subset=["Reporting User"])
df3_1["Timestamp"] = pd.to_datetime(df3_1.Timestamp).dt.strftime("%Y-%m")

group3_1 = df3_1.groupby(by="Timestamp").count()
group3_1.rename(columns={"Reporting User": "New Users"}, inplace=True)

# get total active users, last month new users for "view3" cards
totalActiveUsers = df["Reporting User"].nunique()
currentMonth = pd.to_datetime(pd.Timestamp.today(), unit="s").strftime("%Y-%m")
newActiveUsers_currentMonth = df3_1[df3_1["Timestamp"] == currentMonth].shape[0]


df3_2 = df[["Timestamp", "Platform"]]
df3_2["Timestamp"] = pd.to_datetime(df3_2.Timestamp).dt.strftime("%Y-%m-%d")
group3_2 = df3_2.groupby(by=["Timestamp"]).count().reset_index()
group3_2.set_index(pd.DatetimeIndex(group3_2["Timestamp"]), inplace=True)
group3_2.drop(columns="Timestamp", inplace=True)
group3_2_2 = group3_2.resample("W").sum()
group3_2_2.rename(columns={"Platform": "New Reports"}, inplace=True)

df3_3 = df.groupby(by="Reporting User")["Timestamp"].count().reset_index()
group3_3 = df3_3.groupby(by="Timestamp").count()
updateCardTime = (
    f"Last Update on {pd.to_datetime(pd.Timestamp.today()).strftime('%Y-%m-%d')}"
)
###############################################################################
# print(group3_1.columns)
platformSelector = dcc.Dropdown(
    options=df.Platform.unique().tolist(),
    placeholder="Select Platforms",
    clearable=True,
    multi=True,
    id="platformSelector-id",
    className="ms-5 border-primary border-1 bg-dark text-primary fw-normal rounded",
)


############# view1 --> Report status vizs ######################
fig1_1 = px.treemap(
    group1_1,
    path=[px.Constant("All Platforms"), "Platform", "isOpen"],
    values="Timestamp",
    color="isOpen",
    # color_continuous_midpoint=np.average(group["isOpen"]),
    color_discrete_map={"(?)": "#d0e0e3", True: "#0b5394", False: "lightgrey"},
    hover_data=["Platform"],
    # color_continuous_scale="Blues",
)
# fig1_1.update_layout(showlegend=True)

fig1_1.data[0].textinfo = "percent parent+value"
# color_continuous_midpoint=np.average(group['isOpen']))
fig1_1.update_layout(
    title="<b>Reports Status ( % open/closed) by Platform</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
)
fig1_1.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig1_1.update_traces(
    textposition="middle center",
    textfont_size=14,
)

fig2 = px.bar(
    group1_1,
    x="Timestamp",
    y="Platform",
    color="isOpen",
    orientation="h",
    # hover_data=["tip", "size"],
    # height=400,
    color_discrete_sequence={"(?)": "#d0e0e3", True: "#0b5394", False: "lightgrey"},
    title="<b>Reports Status ( open/closed count) by Platform</b>",
    text="Timestamp",
)
fig2.update_layout(
    title="<b>Reports Status ( open/closed count) by Platform</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
)

fig1_3 = px.bar(
    df[df.isOpen == True]
    .sort_values(by=["reportAge"], ascending=False)
    .reset_index()
    .loc[0:10],
    x="reportAge",
    y="Timestamp",
    color="Platform",
    orientation="h",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    text="reportAge",
)
fig1_3.update_layout(
    title="<b>Open Report - Oldest Top 10 [days]</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
)


table1_1 = dash_table.DataTable(
    data=df1_1.to_dict("records"),
    columns=[{"name": i, "id": i} for i in df1_1.columns],
    style_cell={"textAlign": "left"},
    style_header={"backgroundColor": "#446e9b", "fontWeight": "bold", "color": "white"},
    style_data={"color": "grey", "backgroundColor": "white"},
)


fig1_2 = px.ecdf(
    df[df.isOpen == 0],
    x="reportLifetime",
    color="Platform",
    markers=True,
    lines=False,
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
fig1_2.update_layout(
    title="<b>Closed Report Lifetime Distribution by Platform</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
)
fig1_2.add_hline(
    y=0.5, line_width=1, line_dash="dash", line_color="blue", annotation_text="median"
)

############# view2 --> Report type vizs ######################
fig2_1 = px.treemap(
    group2_1,
    path=[px.Constant("all"), "Platform", "Report Type"],
    values="Timestamp",
    color="Timestamp",
    hover_data=["Platform"],
    color_continuous_scale="RdBu_r",
)
fig2_1.update_layout(showlegend=True)
fig2_1.data[0].textinfo = "label+percent parent+value"
fig2_1.update_layout(
    title="<b>Reports Type by Platform</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
)
fig2_1.update_layout(margin=dict(t=50, l=25, r=25, b=25))
fig2_1.update_traces(
    textposition="middle center",
    textfont_size=14,
)

fig2_2 = px.bar(
    group2_2[group2_2["Report Type"] == df["Report Type"].unique().tolist()[0]],
    x="Platform",
    y="Timestamp",
    color="Appeal",
    facet_col="Report Type",
    title="<b>Report Appeal by Platform, Report Type </b>",
    text="Timestamp",
    color_discrete_sequence=["#0b5394", "lightgrey"],
)
fig2_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
fig2_2.update_layout(yaxis_title="Report Count")
##############view3 vizs##########################
fig3_1 = px.bar(
    group3_1,
    x=group3_1.index,
    y=group3_1["New Users"],
    color="New Users",
    color_continuous_scale="Blues",
    color_continuous_midpoint=group3_1["New Users"].min(),
)
# fig3_1.update_traces(marker_color="#0b5394")
fig3_1.update_layout(yaxis_title="New Users Count")
fig3_1.update_layout(
    title="<b>New Users - Montly Basis</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
    xaxis=dict(
        rangeslider=dict(visible=True, thickness=0.03),  # , bgcolor="#636EFA"
        type="date",
    ),
)
fig3_2 = px.bar(
    group3_2_2,
    x=group3_2_2.index,
    y=group3_2_2["New Reports"],
    color="New Reports",
    color_continuous_scale="Blues",
)
# fig3_2.update_traces(marker_color="#0b5394")
fig3_2.update_layout(yaxis_title="New Reports")
fig3_2.update_layout(
    title="<b>New Reports - Weekly Basis</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
    xaxis=dict(
        rangeslider=dict(visible=True, thickness=0.03),  # , bgcolor="#636EFA"
        type="date",
    ),
)


fig3_3 = px.pie(
    group3_3,
    values="Reporting User",
    names=group3_3.index,
    color=group3_3.index,
    color_discrete_sequence=px.colors.sequential.Blues_r,
)
fig3_3.update_traces(textposition="inside", textinfo="percent")
fig3_3.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
fig3_3.update_layout(
    title="<b>Report Count by User</b>",
    title_font=dict(
        size=16,
        color="#446e9b",
        family="Arial, Helvetica, sans-serif",
    ),
)

card3_1 = create_insight_card("Active Users", totalActiveUsers, updateCardTime)
card3_2 = create_insight_card(
    "New Users", newActiveUsers_currentMonth, f"current Month:{currentMonth}"
)
############ view1 assembly ####################
view1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(figure=fig1_1),
                    ],
                    width=5,
                ),
                dbc.Col(
                    [
                        dcc.Graph(figure=fig1_2),
                    ],
                    width=5,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(figure=fig1_3),
                    ],
                    width=5,
                ),
                dbc.Col(
                    [
                        html.P(
                            "Open Reports - oldest Top 10 - details",
                            className="ps-5 pt-3 text-primary fw-bold",
                        ),
                        table1_1,
                    ],
                    width=5,
                ),
            ]
        ),
    ],
    fluid=False,
    id="view1-id",
    className="ms-5 vh-100 ",
)


############ view2 assembly ####################
view2 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(figure=fig2_1),
                    ],
                    width=11,
                ),
            ],
            className="mb-2 ",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            "Report Type Selector",
                            className="ps-5 pt-3 text-primary fw-bold",
                        ),
                        dcc.Dropdown(
                            options=df["Report Type"].unique().tolist(),
                            clearable=False,
                            value=df["Report Type"].unique().tolist()[0],
                            id="ReportTypeSelector-id",
                            className="ms-5 border-primary border-1 bg-dark text-primary fw-normal rounded",
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        dcc.Graph(figure=fig2_2, id="fig2_2-id"),
                    ],
                    width=7,
                ),
            ]
        ),
    ],
    fluid=False,
    id="view2-id",
    className="ms-5 vh-100 ",
    style={"display": "flex", "flex-direction": "column"},
)
#### view3 container
view3 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        card3_1,
                    ],
                    width=5,
                ),
                dbc.Col(
                    [
                        card3_2,
                    ],
                    width=5,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(figure=fig3_2),
                    ],
                    width=10,
                ),
                # dbc.Col(
                #     [
                #         dcc.Graph(figure=fig3_2),
                #     ],
                #     width=5,
                # ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(figure=fig3_1),
                    ],
                    width=5,
                ),
                dbc.Col(
                    [
                        # html.P(
                        #     "Open Reports - oldest Top 10 - details",
                        #     className="ps-5 pt-3 text-primary fw-bold",
                        # ),
                        # # table1_1,
                        dcc.Graph(figure=fig3_3),
                    ],
                    width=5,
                ),
            ]
        ),
    ],
    fluid=False,
    id="view3-id",
    className="ms-5 vh-100 ",
)

######################################################################
viewContent = dbc.Container([view1], id="viewContent-id")

# page layout
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Hr(),
                    ],
                    className="pe-5",
                ),
            ],
            align="center",
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Report Status", tab_id="tab-1"),
                            dbc.Tab(label="Report Type", tab_id="tab-2"),
                            dbc.Tab(label="Users Activities", tab_id="tab-3"),
                        ],
                        id="tabs",
                        active_tab="tab-1",
                    ),
                    html.Br(),
                    viewContent,
                ]
            ),
            align="center",
        ),
    ],
    className="",
)


@callback(
    Output("viewContent-id", "children"),
    Input("tabs", "active_tab"),
    prevent_initial_call=True
)
def updateView(selTab):
    if selTab == "tab-1":
        return view1
    if selTab == "tab-2":
        return view2
    else:
        return view3


@callback(
    Output("fig2_2-id", "figure"),
    Input("ReportTypeSelector-id", "value"),
    prevent_initial_call=True
)
def updateFig(selValue):
    group2_2ff = group2_2[group2_2["Report Type"] == selValue]
    fig2_2 = px.bar(
        group2_2ff,
        x="Platform",
        y="Timestamp",
        color="Appeal",
        facet_col="Report Type",
        title="<b>Report Appeal by Platform, Report Type </b>",
        text="Timestamp",
        color_discrete_sequence=["#0b5394", "lightgrey"],
    )
    fig2_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    fig2_2.update_layout(yaxis_title="Report Count")
    return fig2_2
