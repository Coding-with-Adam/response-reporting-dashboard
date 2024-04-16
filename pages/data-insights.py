######################################
# MANALI JAIN'S CODES

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
mo = [{'label':m,'value':m} for m in sorted(df['Month'].unique())]
mo.insert(0, {'label': 'All months', 'value': 'all'})
yo = [{'label':y,'value':y} for y in sorted(df['Year'].unique())]
yo.insert(0, {'label': 'All years', 'value': 'all'})
df['Response Time'] = df['Answer Date'] - df['Timestamp']
df['Response Days'] = df['Response Time'].dt.days

# Report table
grid = dag.AgGrid(
            id = "reports-table",
            rowData = df.to_dict("records"),
            columnDefs = [{"field": i} for i in df.columns],
            columnSize = "sizeToFit",
            defaultColDef = {"filter": True},
            dashGridOptions = {"pagination": True, "paginationPageSize":13},
            style = {"height": 650}
        )

# Avg response time line chart 
fig3 = px.line(df, x=df['Platform'].unique(), y=df.groupby(['Platform'])['Response Days'].mean(), text=df.groupby(['Platform'])['Response Days'].mean())
fig3.update_layout(xaxis_title="Platforms", yaxis_title="Avg Response Time (days)")
fig3.update_traces(textposition="top center", texttemplate='%{y:.2f}')

app = Dash(suppress_callback_exceptions=True)
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        html.H1(children=["Transparency Reporting Data Insights"], style={"color": "white"}),
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab(html.B("Reports Table"), value="1"),
                        dmc.Tab(html.B("Reports by Platform and Types"), value="2"),
                        dmc.Tab(html.B("Platform Decisions on Report Types"), value="3"),
                        dmc.Tab(html.B("Avg Response Time by Platform"), value="4")
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
            html.P(children=["Choose the options from the dropdown menus and click on the 'Submit' button to get the desired results"], style={"color": "white"}),
            html.P(children=["Hovering upon a particular Platform slice, will show the count of the Report Types of that particular Platform"], style={"color": "white"}),
            html.Div([
                html.Label(children=['Month:'], style={'color': 'white', 'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='month-variable',
                    options=mo,
                    value=['all'], 
                    multi=True,
                    searchable=True,
                    clearable=False,
                    style={'color': 'black'}
                ),
            ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
            html.Div([
                html.Label(children=['Year:'], style={'color': 'white', 'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='year-variable',
                    options=yo,
                    value=['all'], 
                    multi=True,
                    searchable=True,
                    clearable=False,
                    style={'color': 'black'}
                ),
            ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
            html.Div([
                dbc.Button(
                    id='pie-button', 
                    children="Submit",
                    style={'height': 50, 'width': 300}
                ),
            ], style={'display': 'inline-block', 'margin-right': 20, 'height': 50, 'width': 300}),
            dcc.Graph(id='graph1', clear_on_unhover=True, style={"height": 600}), 
            dcc.Tooltip(id="graph-tooltip")
        ]
    elif active == "3":
        return [
            html.P(children=["Choose the options from the dropdown menus and click on the 'Submit' button to get the desired results"], style={"color": "white"}),
            html.Div([
                html.Label(children=['Month:'], style={'color': 'white', 'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='month-variable',
                    options=mo,
                    value=['all'], 
                    multi=True,
                    searchable=True,
                    clearable=False,
                    style={'color': 'black'}
                ),
            ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
            html.Div([
                html.Label(children=['Year:'], style={'color': 'white', 'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='year-variable',
                    options=yo,
                    value=['all'], 
                    multi=True,
                    searchable=True,
                    clearable=False,
                    style={'color': 'black'}
                ),
            ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
            html.Div([
                dbc.Button(
                    id='bar-button', 
                    children="Submit",
                    style={'height': 50, 'width': 300}
                ),
            ], style={'display': 'inline-block', 'margin-right': 20, 'height': 50, 'width': 300}),
            dcc.Graph(id='graph2')
        ]
    else:
        return [
            dcc.Graph(id='graph3', figure=fig3, style={"height": 600})
        ]

@callback(
    Output('graph1', 'figure'),
    Input('pie-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value'),
    prevent_initial_call=True
)
def update_pie_chart(_, selected_month, selected_year):
    if selected_month==['all'] and selected_year==['all']:
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
    Input('graph1', 'hoverData'),
    prevent_initial_call=True
)
def update_tooltip_content(hoverData):
    if hoverData is None:
        return no_update
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    dff = df[df.Platform == pt["label"]]
    prt_counts = dff['Report Type'].value_counts().sort_values(ascending=True)
    fig_bar = px.bar(dff, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting - {pt['label']}", text=prt_counts.values, orientation='h')
    fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
    children = [dcc.Graph(id='tooltip-bar', figure=fig_bar, style={"height": 300, "width": 600})]
    return True, bbox, children

@callback(
    Output('tooltip-bar', 'figure'),
    Input('pie-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value'),
    prevent_initial_call=True
)
def update_tooltip_chart(_, selected_month, selected_year):
    if selected_month==['all'] and selected_year==['all']:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    prt_counts = df_sub['Report Type'].value_counts().sort_values(ascending=True)
    fig_bar = px.bar(df_sub, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting", text=prt_counts.values, orientation='h')
    fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
    # pt = hoverData["points"][0]
    # bbox = pt["bbox"]
    # dff = df[df.Platform == pt["label"]]
    # prt_counts = dff['Report Type'].value_counts().sort_values(ascending=True)
    # fig_bar = px.bar(dff, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting - {pt['label']}", text=prt_counts.values, orientation='h')
    # fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
    # children = [dcc.Graph(figure=fig_bar, style={"height": 300, "width": 600})]
    return fig_bar

@callback(
    Output('graph2', 'figure'),
    Input('bar-button', 'n_clicks'),
    State('month-variable', 'value'),
    State('year-variable', 'value'),
    prevent_initial_call=True
)
def update_bar_chart(_, selected_month, selected_year):
    if selected_month==['all'] and selected_year==['all']:
        df_sub = df
    else:
        df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
    #rt_counts = df['Report Type'].value_counts().sort_values(ascending=False)
    #df['Platform Decision'].fillna("Unknown", inplace=True)
    #color_map = {"Removed": "green", "Demoted": "blue", "No Action": "red", "Unknown": "gray"}
    fig2 = px.bar(df, x="Report Type", height=600, color="Platform Decision", barmode="group")
    fig2.update_layout(xaxis_title="Report Types", yaxis_title="Count")
    return fig2

if __name__ == '__main__':
    app.run(debug=True)
