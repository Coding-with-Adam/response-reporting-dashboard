import dash
from dash import Dash, html, dcc, callback, Output, Input, State, no_update
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/dummy_data_10000_wNan.csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M')
df['Month'] = df['Timestamp'].dt.month
df['Year'] = df['Timestamp'].dt.year
df['Answer Date'] = pd.to_datetime(df['Answer Date'], format='%m/%d/%Y %H:%M')
df['Response Time'] = df['Answer Date'] - df['Timestamp']
df['Response Days'] = df['Response Time'].dt.days
x = len(df.index)

# Report table
grid = dag.AgGrid(
            id = "reports-table",
            rowData = df.to_dict("records"),
            columnDefs = [
                {"field": 'Timestamp'},
                {"field": 'Reporting Entity'},
                {"field": 'Reporting User'},
                {"field": 'Platform'},
                {"field": 'URL'},
                {"field": 'Report Type'},
                {"field": 'Screenshot URL'},
                {"field": 'Answer Date'},
                {"field": 'Platform Decision'},
                {"field": 'Policy'},
                {"field": 'Appeal'}
            ],
            columnSize = "sizeToFit",
            defaultColDef = {"filter": True},
            dashGridOptions = {"pagination": True, "paginationPageSize":13},
            style = {"height": 650}
        )

app = Dash(suppress_callback_exceptions=True)
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        html.H1(children=[f"Transparency Reporting Data Insights of {x} reports"], style={"color": "white"}),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab(html.B("Reports Table"), value="1"),
                        dmc.Tab(html.B("Reports by Platform and Types"), value="2"),
                        dmc.Tab(html.B("Platform Decisions on Report Types"), value="3"),
                        dmc.Tab(html.B("Avg Response Time by Platform"), value="4"),
                        dmc.Tab(html.B("Policies Implemented"), value="5"),
                        dmc.Tab(html.B("User Appeal on Platform Decision"), value="6"),
                        dmc.Tab(html.B("Reporting User per Month"), value="7")
                    ]
                ),
            ],
            id="tabs-example",
            value="1",
        ),
        html.Div(id="tabs-content", style={"paddingTop": 10}),
    ]
)

@callback(
    Output("tabs-content", "children"),
    Input("tabs-example", "value"))
def render_content(active):
    if active == "1":
        return [grid]
    elif active == "2":
        return [
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=[
                            {'label': "January", 'value': 1},
                            {'label': "February", 'value': 2},
                            {'label': "March", 'value': 3},
                            {'label': "April", 'value': 4},
                            {'label': "May", 'value': 5},
                            {'label': "June", 'value': 6},
                            {'label': "July", 'value': 7},
                            {'label': "August", 'value': 8},
                            {'label': "September", 'value': 9},
                            {'label': "October", 'value': 10},
                            {'label': "November", 'value': 11},
                            {'label': "December", 'value': 12}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select month",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=[
                            {'label': '2023', 'value': 2023}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select year",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    dbc.Button(
                        id='pie-button', 
                        children="Submit",
                        color="info",
                        style={'font-weight': 'bold', 'font-size': 15, 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'bottom'})
            ]), 
            dcc.Graph(id='graph1', clear_on_unhover=True, style={"height": 600}), 
            dcc.Tooltip(id="graph-tooltip") 
        ]
    elif active == "3":
        return [
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=[
                            {'label': "January", 'value': 1},
                            {'label': "February", 'value': 2},
                            {'label': "March", 'value': 3},
                            {'label': "April", 'value': 4},
                            {'label': "May", 'value': 5},
                            {'label': "June", 'value': 6},
                            {'label': "July", 'value': 7},
                            {'label': "August", 'value': 8},
                            {'label': "September", 'value': 9},
                            {'label': "October", 'value': 10},
                            {'label': "November", 'value': 11},
                            {'label': "December", 'value': 12}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select month",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=[
                            {'label': '2023', 'value': 2023}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select year",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    dbc.Button(
                        id='bar-button', 
                        children="Submit",
                        color="info",
                        style={'font-weight': 'bold', 'font-size': 15, 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'bottom'})
            ]),
            dcc.Graph(id='graph2', style={'height': 600})
        ]
    elif active == "4":
        return [
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=[
                            {'label': "January", 'value': 1},
                            {'label': "February", 'value': 2},
                            {'label': "March", 'value': 3},
                            {'label': "April", 'value': 4},
                            {'label': "May", 'value': 5},
                            {'label': "June", 'value': 6},
                            {'label': "July", 'value': 7},
                            {'label': "August", 'value': 8},
                            {'label': "September", 'value': 9},
                            {'label': "October", 'value': 10},
                            {'label': "November", 'value': 11},
                            {'label': "December", 'value': 12}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select month",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=[
                            {'label': '2023', 'value': 2023}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select year",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    dbc.Button(
                        id='avg-button', 
                        children="Submit",
                        color="info",
                        style={'font-weight': 'bold', 'font-size': 15, 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'bottom'})
            ]),
            dcc.Graph(id='graph3', style={"height": 600})
        ]
    elif active == "5":
        return [
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=[
                            {'label': "January", 'value': 1},
                            {'label': "February", 'value': 2},
                            {'label': "March", 'value': 3},
                            {'label': "April", 'value': 4},
                            {'label': "May", 'value': 5},
                            {'label': "June", 'value': 6},
                            {'label': "July", 'value': 7},
                            {'label': "August", 'value': 8},
                            {'label': "September", 'value': 9},
                            {'label': "October", 'value': 10},
                            {'label': "November", 'value': 11},
                            {'label': "December", 'value': 12}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select month",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=[
                            {'label': '2023', 'value': 2023}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select year",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    dbc.Button(
                        id='policy-button', 
                        children="Submit",
                        color="info",
                        style={'font-weight': 'bold', 'font-size': 15, 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'bottom'})
            ]),
            dcc.Graph(id='graph4', style={'height': 600})
        ]
    elif active == "6":
        return[
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=[
                            {'label': "January", 'value': 1},
                            {'label': "February", 'value': 2},
                            {'label': "March", 'value': 3},
                            {'label': "April", 'value': 4},
                            {'label': "May", 'value': 5},
                            {'label': "June", 'value': 6},
                            {'label': "July", 'value': 7},
                            {'label': "August", 'value': 8},
                            {'label': "September", 'value': 9},
                            {'label': "October", 'value': 10},
                            {'label': "November", 'value': 11},
                            {'label': "December", 'value': 12}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select month",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=[
                            {'label': '2023', 'value': 2023}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select year",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    dbc.Button(
                        id='appeal-button', 
                        children="Submit",
                        color="info",
                        style={'font-weight': 'bold', 'font-size': 15, 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'bottom'})
            ]),
            dcc.Graph(id='graph5', style={'height': 600})
        ]
    else:
        return[
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=[
                            {'label': "January", 'value': 1},
                            {'label': "February", 'value': 2},
                            {'label': "March", 'value': 3},
                            {'label': "April", 'value': 4},
                            {'label': "May", 'value': 5},
                            {'label': "June", 'value': 6},
                            {'label': "July", 'value': 7},
                            {'label': "August", 'value': 8},
                            {'label': "September", 'value': 9},
                            {'label': "October", 'value': 10},
                            {'label': "November", 'value': 11},
                            {'label': "December", 'value': 12}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select month",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=[
                            {'label': '2023', 'value': 2023}
                        ],
                        value=[], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        placeholder="Select year",
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    dbc.Button(
                        id='user-button', 
                        children="Submit",
                        color="info",
                        style={'font-weight': 'bold', 'font-size': 15, 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'bottom'})
            ]),
            dcc.Graph(id='graph6', style={'height': 600})
        ]

@callback(
    Output('graph1', 'figure'),
    Input('pie-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_platform_chart(_, selected_month, selected_year):
    if not selected_month and not selected_year:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    fig1 = px.pie(df_sub, names='Platform', hole=0.8, color_discrete_sequence=px.colors.sequential.Agsunset)
    fig1.update_traces(textposition='outside', textinfo='value+percent+label', rotation=50)
    fig1.update_layout(margin=dict(t=50, b=35, l=0, r=0), showlegend=False,
                  plot_bgcolor='#fafafa', paper_bgcolor='#fafafa',
                  font=dict(size=17, color='#000000'),
                  hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
    fig1.add_layout_image(
        dict(
            source="https://i.postimg.cc/zXr1NjnK/platforms.jpg",
            xref="paper", yref="paper",
            x=0.48, y=0.48,
            sizex=0.47, sizey=0.47,
            xanchor="center", yanchor="middle", sizing="contain",
        )
    )
    return fig1

@callback(
    Output('graph-tooltip', 'show'),
    Output('graph-tooltip', 'bbox'),
    Output('graph-tooltip', 'children'),
    Input('graph1', 'hoverData')
)
def update_tooltip_content(hoverData):
    if hoverData is None:
        return False, no_update, no_update
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    dff = df[df.Platform == pt["label"]]
    prt_counts = dff['Report Type'].value_counts().sort_values(ascending=True)
    fig_bar = px.bar(dff, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting - {pt['label']}", text=prt_counts.values, orientation='h')
    fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
    children = [dcc.Graph(id='tooltip-bar', figure=fig_bar, style={"height": 300, "width": 600})]
    return True, bbox, children

# @callback(
#     Output('tooltip-bar', 'figure'),
#     Input('pie-button', 'n_clicks'),
#     State('month-variable', 'value'),
#     State('year-variable', 'value')
# )
# def update_tooltip_chart(_, selected_month, selected_year):
#     fig_bar_my = px.bar()  # Create an empty figure
#     if selected_month or selected_year:
#         df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
#         prt_counts = df_sub['Report Type'].value_counts().sort_values(ascending=True)
#         fig_bar_my = px.bar(df_sub, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting", text=prt_counts.values, orientation='h')
#         fig_bar_my.update_layout(yaxis_title="Report Types", xaxis_title="Count")
#     return fig_bar_my
    # if not selected_month and not selected_year:
    #     df_sub = df
    # else:
    #     df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    # prt_counts = df_sub['Report Type'].value_counts().sort_values(ascending=True)
    # fig_bar.add_trace(px.bar(df_sub, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting", text=prt_counts.values, orientation='h'))
    # fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
    # return fig_bar

@callback(
    Output('graph2', 'figure'),
    Input('bar-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_report_type_chart(_, selected_month, selected_year):
    if not selected_month and not selected_year:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    rt_pd = df_sub.groupby(['Report Type', 'Platform Decision']).size().reset_index(name='Count')
    fig2 = px.bar(rt_pd, x="Report Type", y="Count", facet_col="Platform Decision", text="Count")
    return fig2

@callback(
    Output('graph3', 'figure'),
    Input('avg-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_avg_chart(_, selected_month, selected_year):
    if not selected_month and not selected_year:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    fig3 = px.bar(df_sub, x=df_sub['Platform'].unique(), y=df_sub.groupby(['Platform'])['Response Days'].mean(), text=df_sub.groupby(['Platform'])['Response Days'].mean())
    fig3.update_layout(xaxis_title="Platforms", yaxis_title="Avg Response Time (days)")
    fig3.update_traces(textposition="outside", texttemplate='%{y:.2f}')
    return fig3

@callback(
    Output('graph4', 'figure'),
    Input('policy-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_policy_chart(_, selected_month, selected_year):
    if not selected_month and not selected_year:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    py_counts = df_sub['Policy'].value_counts().sort_values(ascending=False)
    fig4 = px.bar(df_sub, x=py_counts.index, y=py_counts.values, text=py_counts.values)
    fig4.update_layout(xaxis_title="Policies", yaxis_title="Count")
    return fig4

@callback(
    Output('graph5', 'figure'),
    Input('appeal-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_appeal_chart(_, selected_month, selected_year):
    if not selected_month and not selected_year:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    al_pd = df_sub.groupby(['Appeal', 'Platform Decision']).size().reset_index(name='Count')
    fig5 = px.bar(al_pd, height=600, x="Appeal", y="Count", facet_col="Platform Decision", text="Count")
    return fig5

@callback(
    Output('graph6', 'figure'),
    Input('user-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_user_chart(_, selected_month, selected_year):
    if not selected_month and not selected_year:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    uu = df_sub.drop_duplicates(subset=['Reporting User'])
    my_ru = uu.groupby(['Year', 'Month'])['Reporting User'].nunique().reset_index(name='Unique Users Count')
    fig6 = px.bar(my_ru, x="Month", y="Unique Users Count", text="Unique Users Count")
    return fig6

if __name__ == '__main__':
    app.run(debug=True)

