import dash
from dash import Dash, html, dcc, callback, Output, Input, State, no_update, ctx
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
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
df['Month'] = df['Month'].map(lambda x: month_order[x-1])
mo = [{'label':m,'value':m} for m in df['Month'].unique()]
mo.insert(0, {'label': 'All months', 'value': 'all'})
yo = [{'label':y,'value':y} for y in sorted(df['Year'].unique())]
yo.insert(0, {'label': 'All years', 'value': 'all'})
n_row = len(df.index)

# Report Table (Tab 1) 
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
        html.H1(children=[f"Transparency Reporting Data Insights of {n_row} reports"], style={"color": "white"}),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab(html.B("Reports Table"), value="1"),
                        dmc.Tab(html.B("Users and Reports per Month"), value="2"),
                        dmc.Tab(html.B("Platform Reports"), value="3"), 
                        dmc.Tab(html.B("Platform Decisions on Report Types"), value="4"),
                        dmc.Tab(html.B("Policies Implemented"), value="5"),
                        dmc.Tab(html.B("Appeal on Platform Decision"), value="6")
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
    Input("tabs-example", "value")
)
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
                        options=mo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=yo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
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
            dcc.Graph(id='graph1', clear_on_unhover=True, style={'height': 600}),
            dcc.Tooltip(id="report-tooltip", style={'height': 100})
        ]
    elif active == "3":
        return [
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=mo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=yo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    dbc.Button(
                        id='platform-button', 
                        children="Submit",
                        color="info",
                        style={'font-weight': 'bold', 'font-size': 15, 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'bottom'})
            ]), 
            html.Div([
                dcc.Graph(id='graph2', clear_on_unhover=True, style={'height': 400, 'margin-bottom': 10, 'margin-right': 10}),
                dcc.Tooltip(id="graph-tooltip")
            ]),
            html.Div([
                dcc.Graph(id='graph3', style={'display': 'inline-block', 'margin-right': 10}),
                dcc.Graph(id='graph4', style={'display': 'inline-block', 'margin-right': 10})
            ])     
        ]
    elif active == "4":
        return [
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=mo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=yo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
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
            dcc.Graph(id='graph5', style={'height': 600})
        ]
    elif active == "5":
        return[
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=mo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=yo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
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
            dcc.Graph(id='graph6', style={'height': 600})
        ]
    else:
        return[
            html.Div([
                html.Div([
                    html.Label('Month:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='month-variable',
                        options=mo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
                        style={'color': 'black', 'width': 300, 'height': 40}
                    )
                ], style={'display': 'inline-block', 'margin-right': 20, 'margin-bottom': 10, 'vertical-align': 'top'}),
                html.Div([
                    html.Label('Year:', style={'color': 'white', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-variable',
                        options=yo,
                        value=['all'], 
                        multi=True,
                        searchable=True,
                        clearable=False,
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
            dcc.Graph(id='graph7', style={'height': 600})
        ]

# Users and Reports per Month (Tab 2)
@callback(
    Output('graph1', 'figure'),
    Input('user-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_user_chart(_, selected_month, selected_year):
    dp_df = df.drop_duplicates(subset=['Reporting User'], keep='first')
    if selected_month==['all'] and selected_year==['all']:
        df_sub = dp_df
    else:
        df_sub = dp_df[(dp_df['Month'].isin(selected_month)) & (dp_df['Year'].isin(selected_year))]
    my_ru = df_sub.groupby(['Year', 'Month'])['Reporting User'].size().reset_index(name='Unique Users Count')
    fig1 = px.bar(
        my_ru, 
        x="Month", 
        y="Unique Users Count", 
        text="Unique Users Count", 
        hover_data={'Unique Users Count': False, 'Month': False}, 
        color="Month",
        color_discrete_sequence=px.colors.qualitative.Dark24,
        category_orders={"Month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
    )
    fig1.update_layout(showlegend=False)
    return fig1
@callback(
    Output('report-tooltip', 'show'),
    Output('report-tooltip', 'bbox'),
    Output('report-tooltip', 'children'),
    Input('graph1', 'hoverData')
)
def update_report_content(hoverData):
    if hoverData is None:
        return False, no_update, no_update
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    dfr = df[df.Month == pt["label"]]
    nr = len(dfr.index)
    card = dbc.Card(
        dbc.CardBody(
            [
                html.P(html.B("Reports submitted:")),
                html.P(f"{nr}")
            ]
        ), style={"color": "black"}
    )
    return True, bbox, card

# Platform Reports (Tab 3)
@callback(
    Output('graph2', 'figure'),
    Input('platform-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_platform_chart(_, selected_month, selected_year):
    if selected_month==['all'] and selected_year==['all']:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    fig2 = px.pie(
        df_sub, 
        names="Platform", 
        hole=0.8, 
        hover_data={"Platform": False},
        color_discrete_map={
            'YouTube': px.colors.qualitative.Set1[0], 'Facebook': px.colors.qualitative.Set1[1], 
            'WhatsApp': px.colors.qualitative.Set1[2], 'Instagram': px.colors.qualitative.Set1[3],
            'Google': px.colors.qualitative.Set1[4], 'TikTok': px.colors.qualitative.Set1[5],
            'Bing': px.colors.qualitative.Set1[6], 'LinkedIn': px.colors.qualitative.Set1[7]
        },
        title="Reports Distribution"
    )
    fig2.update_traces(textposition='outside', textinfo='value+percent+label', rotation=50)
    fig2.update_layout(margin=dict(t=50, b=35, l=0, r=0), showlegend=False,
        plot_bgcolor='#fafafa', paper_bgcolor='#fafafa',
        font=dict(size=17, color='#000000'),
        hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
    fig2.add_layout_image(
        dict(
            source="https://i.postimg.cc/zXr1NjnK/platforms.jpg",
            xref="paper", yref="paper",
            x=0.50, y=0.50,
            sizex=0.50, sizey=0.50,
            xanchor="center", yanchor="middle", sizing="contain",
        )
    )
    return fig2
@callback(
    Output('graph-tooltip', 'show'),
    Output('graph-tooltip', 'bbox'),
    Output('graph-tooltip', 'children'),
    Input('graph2', 'hoverData'),
    Input('platform-button', 'n_clicks'),
    State('month-variable', 'value'), 
    State('year-variable', 'value')
)
def update_tooltip_content(hoverData, _, selected_month, selected_year):
    if hoverData is None:
        return False, no_update, no_update
    tmp = df[(df["Month"].isin(selected_month)) & (df["Year"].isin(selected_year))].index.tolist()
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    if len(tmp) > 0:
        dff = df[(df.Platform == pt["label"]) & (df["Month"].isin(selected_month)) & (df["Year"].isin(selected_year))]
    else:
        dff = df[df["Platform"] == pt["label"]]
    prt_counts = dff['Report Type'].value_counts().sort_values(ascending=True)
    fig_bar = px.bar(
        dff, 
        y=prt_counts.index, 
        x=prt_counts.values, 
        title=f"Types of Reporting - {pt['label']}", 
        text=prt_counts.values, 
        orientation='h'
    )
    fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
    children = [dcc.Graph(id='tooltip-bar', figure=fig_bar, style={"height": 300, "width": 600})]
    return True, bbox, children
@callback(
    Output('graph3', 'figure'),
    Input('platform-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_avg_chart(_, selected_month, selected_year):
    if selected_month == ['all'] and selected_year == ['all']:
        df_sub = df
    else:
        df_sub = df[(df["Month"].isin(selected_month)) & (df["Year"].isin(selected_year))]    
    art = df_sub.groupby(['Platform'])['Response Days'].mean().reset_index(name="Avg Response Time (days)")
    fig3 = px.bar(
        art, 
        x="Platform", 
        y="Avg Response Time (days)", 
        text="Avg Response Time (days)", 
        hover_data={"Platform": False, "Avg Response Time (days)": False},
        color="Platform",
        color_discrete_map={
            'YouTube': px.colors.qualitative.Set1[0], 'Facebook': px.colors.qualitative.Set1[1], 
            'WhatsApp': px.colors.qualitative.Set1[2], 'Instagram': px.colors.qualitative.Set1[3],
            'Google': px.colors.qualitative.Set1[4], 'TikTok': px.colors.qualitative.Set1[5],
            'Bing': px.colors.qualitative.Set1[6], 'LinkedIn': px.colors.qualitative.Set1[7]
        },
        title="Avg Response Time (days)"
        )
    fig3.update_traces(textposition="inside", texttemplate='%{y:.2f}')
    fig3.update_xaxes(title_text="")
    fig3.update_yaxes(title_text="")
    fig3.update_layout(showlegend=False)
    return fig3
@callback(
    Output('graph4', 'figure'),
    Input('platform-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_platform_decision_chart(_, selected_month, selected_year):
    if selected_month == ['all'] and selected_year == ['all']:
        df_sub = df
    else:
        df_sub = df[(df["Month"].isin(selected_month)) & (df["Year"].isin(selected_year))]
    pf_pd = df_sub.groupby(['Platform', 'Platform Decision']).size().reset_index(name='Count')
    fig4 = px.bar(
        pf_pd, 
        x="Platform Decision", 
        y="Count", 
        facet_col="Platform", 
        text="Count", 
        hover_data={"Platform Decision": False, "Count": False, "Platform": False},
        color="Platform",
        color_discrete_map={
            'YouTube': px.colors.qualitative.Set1[0], 'Facebook': px.colors.qualitative.Set1[1], 
            'WhatsApp': px.colors.qualitative.Set1[2], 'Instagram': px.colors.qualitative.Set1[3],
            'Google': px.colors.qualitative.Set1[4], 'TikTok': px.colors.qualitative.Set1[5],
            'Bing': px.colors.qualitative.Set1[6], 'LinkedIn': px.colors.qualitative.Set1[7]
        },
        title="Platform Decision"
    )
    fig4.update_xaxes(title_text="")
    fig4.update_yaxes(title_text="")
    fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    fig4.update_layout(showlegend=False)
    return fig4

# Platform Desicions on Report Types (Tab 4)  
@callback(
    Output('graph5', 'figure'),
    Input('bar-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_report_type_chart(_, selected_month, selected_year):
    if selected_month==['all'] and selected_year==['all']:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    rt_pd = df_sub.groupby(['Report Type', 'Platform Decision']).size().reset_index(name='Count')
    fig5 = px.bar(
        rt_pd, 
        x="Report Type", 
        y="Count", 
        facet_col="Platform Decision", 
        text="Count", 
        hover_data={"Report Type": False, "Count": False, "Platform Decision": False},
        color="Platform Decision",
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    fig5.update_xaxes(title_text="")
    fig5.update_yaxes(title_text="")
    fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    fig5.update_layout(showlegend=False)
    return fig5

# Policies Implemented (Tab 5)
@callback(
    Output('graph6', 'figure'),
    Input('policy-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_policy_chart(_, selected_month, selected_year):
    if selected_month==['all'] and selected_year==['all']:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    py = df_sub.groupby(['Policy']).size().reset_index(name='Count')
    fig6 = px.bar(
        py, 
        x="Policy", 
        y="Count", 
        text="Count", 
        hover_data={"Policy": False, "Count": False},
        color="Policy",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig6.update_xaxes(title_text="")
    fig6.update_yaxes(title_text="")
    fig6.update_layout(showlegend=False)
    return fig6

# Appeal on Platform Desicions (Tab 6)
@callback(
    Output('graph7', 'figure'),
    Input('appeal-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value')
)
def update_appeal_chart(_, selected_month, selected_year):
    if selected_month==['all'] and selected_year==['all']:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    al_pd = df_sub.groupby(['Appeal', 'Platform Decision']).size().reset_index(name='Count')
    fig7 = px.bar(
        al_pd, 
        x="Platform Decision", 
        y="Count", 
        facet_col="Appeal", 
        text="Count", 
        hover_data={"Platform Decision": False, "Count": False, "Appeal": False},
        color="Appeal",
        color_discrete_sequence=px.colors.qualitative.Light24
    )
    fig7.update_xaxes(title_text="")
    fig7.update_yaxes(title_text="")
    fig7.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    fig7.update_layout(showlegend=False)
    return fig7

if __name__ == '__main__':
     app.run(debug=True)