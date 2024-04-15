import dash
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import load_figure_template

dash.register_page(__name__)


def create_graph_card(id, fig, className='p-2'):
    height = "100%"
    card = dbc.Card(
    [dcc.Graph(id=id, figure=fig, style={'height': height}, config={'displayModeBar': False})],
    style={'height': height},
    className=className
    )
    return card


df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/dummy_data_100_wNan.csv")
df.columns = ['timestamp', 'reporting_entity', 'reporting_user', 'platform', 'url', 'report_type', 'screenshot_url', 'answer_date', 'platform_decision', 'policy', 'appeal']
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['answer_date'] = pd.to_datetime(df['answer_date'], errors='coerce')


unique_platforms = df['platform'].unique()
color_mapping = dict(zip(unique_platforms, px.colors.qualitative.G10))


df_pie = df.groupby('platform', as_index=False)['timestamp'].size().sort_values(by='size', ascending=False)
fig1 = px.pie(df_pie, values='size', names='platform', hole=.5, title='Total reports by platform',
                color='platform', color_discrete_map=color_mapping)\
    .update_traces(marker=dict(line=dict(color='#FFFFFF', width=2)), sort=True, direction='clockwise')\
    .update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5), legend=dict(xanchor='right', x=1))

df_line = df.groupby(['timestamp', 'platform'], as_index=False)['platform'].size()
fig2 = px.line(df_line, x='timestamp', y='size', color='platform', color_discrete_map=color_mapping,
    title='Daily reports by Platform', markers=True,
    labels={'Date': 'timestamp', 'Count': 'size', 'Platform': 'platform'})\
    .update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5))

df_average_response_time = df.copy().dropna(subset=['answer_date'])
df_average_response_time['response_time'] = (df_average_response_time['answer_date'] - df_average_response_time['timestamp']).dt.days
average_response_time = df_average_response_time.groupby('platform', as_index=False)['response_time'].mean().sort_values(by='response_time', ascending=False)
fig3 = px.bar(average_response_time, x='platform', y='response_time', title='Average responce time by platform (Days)',
            ).update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5),
            showlegend=False)

fig4 = px.histogram(df, x='platform_decision', color='platform', color_discrete_map=color_mapping,
                    title='Decisions by platform', barmode='group').\
    update_layout(margin=dict(l=0, r=0, t=30, b=0)).update_traces(marker=dict(line=dict(color='#FFFFFF', width=2))).update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5),
                   ).update_yaxes(categoryorder='total descending')

fig1_card = create_graph_card('fig1', fig1)
fig2_card = create_graph_card('fig2', fig2)
fig3_card = create_graph_card('fig3', fig3)
fig4_card = create_graph_card('fig4', fig4)


load_figure_template("yeti")

column_heigh_style = {"height": "100%"}
layout = dbc.Container(
    [
        dbc.Row([dbc.Col(fig1_card, width=6, style=column_heigh_style), dbc.Col(fig2_card, width=6, style=column_heigh_style)],
                className='my-4',
                style={"height": '45vh'},
                justify='around'),
        dbc.Row([dbc.Col(fig3_card, width=6, style=column_heigh_style), dbc.Col(fig4_card, width=6, style=column_heigh_style)],
                className='my-4',
                style={"height": '45vh'},
                justify='around'),
        ],
    fluid=True,
    style={"height": '100vh', 'background-color': '#F4F6F7'},
)

######################################
# MANALI JAIN'S CODES

# import dash
# from dash import Dash, html, dcc, callback, Output, Input, State, no_update
# import dash_mantine_components as dmc
# import dash_bootstrap_components as dbc
# import dash_ag_grid as dag
# import pandas as pd
# import plotly.express as px

# df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/dummy_data_10000_wNan.csv")
# df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M')
# df['Month'] = df['Timestamp'].dt.month
# df['Year'] = df['Timestamp'].dt.year
# df['Answer Date'] = pd.to_datetime(df['Answer Date'], format='%m/%d/%Y %H:%M')
# mo = [{'label':m,'value':m} for m in sorted(df['Month'].unique())]
# mo.insert(0, {'label': 'All months', 'value': 'all'})
# yo = [{'label':y,'value':y} for y in sorted(df['Year'].unique())]
# yo.insert(0, {'label': 'All years', 'value': 'all'})
# df['Response Time'] = df['Answer Date'] - df['Timestamp']
# df['Response Days'] = df['Response Time'].dt.days

# # Report table
# grid = dag.AgGrid(
#             id = "reports-table",
#             rowData = df.to_dict("records"),
#             columnDefs = [{"field": i} for i in df.columns],
#             columnSize = "sizeToFit",
#             defaultColDef = {"filter": True},
#             dashGridOptions = {"pagination": True, "paginationPageSize":13},
#             style = {"height": 650}
#         )

# # Avg response time line chart 
# fig3 = px.line(df, x=df['Platform'].unique(), y=df.groupby(['Platform'])['Response Days'].mean(), text=df.groupby(['Platform'])['Response Days'].mean())
# fig3.update_layout(xaxis_title="Platforms", yaxis_title="Avg Response Time (days)")
# fig3.update_traces(textposition="top center", texttemplate='%{y:.2f}')

# app = Dash(suppress_callback_exceptions=True)
# app.layout = dmc.MantineProvider(
#     theme={"colorScheme": "dark"},
#     withGlobalStyles=True,
#     children=[
#         html.H1(children=["Transparency Reporting Data Insights"], style={"color": "white"}),
#         dmc.Tabs(
#             [
#                 dmc.TabsList(
#                     [
#                         dmc.Tab(html.B("Reports Table"), value="1"),
#                         dmc.Tab(html.B("Reports by Platform and Types"), value="2"),
#                         dmc.Tab(html.B("Platform Decisions on Report Types"), value="3"),
#                         dmc.Tab(html.B("Avg Response Time by Platform"), value="4")
#                     ]
#                 ),
#             ],
#             id="tabs-example",
#             value="1",
#         ),
#         html.Div(id="tabs-content", style={"paddingTop": 10}),
#     ]
# )

# @callback(
#     Output("tabs-content", "children"),
#     Input("tabs-example", "value"))
# def render_content(active):
#     if active == "1":
#         return [grid]
#     elif active == "2":
#         return [
#             html.P(children=["Choose the options from the dropdown menus and click on the 'Submit' button to get the desired results"], style={"color": "white"}),
#             html.P(children=["Hovering upon a particular Platform slice, will show the count of the Report Types of that particular Platform"], style={"color": "white"}),
#             html.Div([
#                 html.Label(children=['Month:'], style={'color': 'white', 'font-weight': 'bold'}),
#                 dcc.Dropdown(
#                     id='month-variable',
#                     options=mo,
#                     value=['all'], 
#                     multi=True,
#                     searchable=True,
#                     clearable=False,
#                     style={'color': 'black'}
#                 ),
#             ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
#             html.Div([
#                 html.Label(children=['Year:'], style={'color': 'white', 'font-weight': 'bold'}),
#                 dcc.Dropdown(
#                     id='year-variable',
#                     options=yo,
#                     value=['all'], 
#                     multi=True,
#                     searchable=True,
#                     clearable=False,
#                     style={'color': 'black'}
#                 ),
#             ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
#             html.Div([
#                 dbc.Button(
#                     id='pie-button', 
#                     children="Submit",
#                     style={'height': 50, 'width': 300}
#                 ),
#             ], style={'display': 'inline-block', 'margin-right': 20, 'height': 50, 'width': 300}),
#             dcc.Graph(id='graph1', clear_on_unhover=True, style={"height": 600}), 
#             dcc.Tooltip(id="graph-tooltip")
#         ]
#     elif active == "3":
#         return [
#             html.P(children=["Choose the options from the dropdown menus and click on the 'Submit' button to get the desired results"], style={"color": "white"}),
#             html.Div([
#                 html.Label(children=['Month:'], style={'color': 'white', 'font-weight': 'bold'}),
#                 dcc.Dropdown(
#                     id='month-variable',
#                     options=mo,
#                     value=['all'], 
#                     multi=True,
#                     searchable=True,
#                     clearable=False,
#                     style={'color': 'black'}
#                 ),
#             ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
#             html.Div([
#                 html.Label(children=['Year:'], style={'color': 'white', 'font-weight': 'bold'}),
#                 dcc.Dropdown(
#                     id='year-variable',
#                     options=yo,
#                     value=['all'], 
#                     multi=True,
#                     searchable=True,
#                     clearable=False,
#                     style={'color': 'black'}
#                 ),
#             ], style={'display': 'inline-block', 'margin-right': 20, 'width': 300}),
#             html.Div([
#                 dbc.Button(
#                     id='bar-button', 
#                     children="Submit",
#                     style={'height': 50, 'width': 300}
#                 ),
#             ], style={'display': 'inline-block', 'margin-right': 20, 'height': 50, 'width': 300}),
#             dcc.Graph(id='graph2')
#         ]
#     else:
#         return [
#             dcc.Graph(id='graph3', figure=fig3, style={"height": 600})
#         ]

# @callback(
#     Output('graph1', 'figure'),
#     Input('pie-button', 'n_clicks'),
#     State('month-variable', 'value'),
#     State('year-variable', 'value'),
#     prevent_initial_call=True
# )
# def update_pie_chart(_, selected_month, selected_year):
#     if selected_month==['all'] and selected_year==['all']:
#         df_sub = df
#     else:
#         df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
#     fig1 = px.pie(df_sub, names='Platform', hole=0.8, color_discrete_sequence=px.colors.sequential.Agsunset)
#     fig1.update_traces(textposition='outside', textinfo='value+percent+label', rotation=50)
#     fig1.update_layout(margin=dict(t=50, b=35, l=0, r=0), showlegend=False,
#                   plot_bgcolor='#fafafa', paper_bgcolor='#fafafa',
#                   font=dict(size=17, color='#000000'),
#                   hoverlabel=dict(bgcolor="#444", font_size=13, font_family="Lato, sans-serif"))
#     fig1.add_layout_image(
#         dict(
#             source="https://i.postimg.cc/zXr1NjnK/platforms.jpg",
#             xref="paper", yref="paper",
#             x=0.48, y=0.48,
#             sizex=0.47, sizey=0.47,
#             xanchor="center", yanchor="middle", sizing="contain",
#         )
#     )
#     return fig1

# @callback(
#     Output('graph-tooltip', 'show'),
#     Output('graph-tooltip', 'bbox'),
#     Output('graph-tooltip', 'children'),
#     Input('graph1', 'hoverData'),
#     prevent_initial_call=True
# )
# def update_tooltip_content(hoverData):
#     if hoverData is None:
#         return no_update
#     pt = hoverData["points"][0]
#     bbox = pt["bbox"]
#     dff = df[df.Platform == pt["label"]]
#     prt_counts = dff['Report Type'].value_counts().sort_values(ascending=True)
#     fig_bar = px.bar(dff, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting - {pt['label']}", text=prt_counts.values, orientation='h')
#     fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
#     children = [dcc.Graph(figure=fig_bar, style={"height": 300, "width": 600})]
#     return True, bbox, children

# @callback(
#     Output('graph-tooltip', 'figure'),
#     Input('pie-button', 'n_clicks'),
#     Input('graph1', 'hoverData'),
#     State('month-variable', 'value'),
#     State('year-variable', 'value'),
#     prevent_initial_call=True
# )
# def update_tooltip_chart(_, selected_month, selected_year):
#     if selected_month==['all'] and selected_year==['all']:
#         df_sub = df
#     else:
#         df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
#     pt = hoverData["points"][0]
#     bbox = pt["bbox"]
#     dff = df[df.Platform == pt["label"]]
#     prt_counts = dff['Report Type'].value_counts().sort_values(ascending=True)
#     fig_bar = px.bar(dff, y=prt_counts.index, x=prt_counts.values, title=f"Types of Reporting - {pt['label']}", text=prt_counts.values, orientation='h')
#     fig_bar.update_layout(yaxis_title="Report Types", xaxis_title="Count")
#     children = [dcc.Graph(figure=fig_bar, style={"height": 300, "width": 600})]
#     return fig_bar

# @callback(
#     Output('graph2', 'figure'),
#     Input('bar-button', 'n_clicks'),
#     State('month-variable', 'value'),
#     State('year-variable', 'value'),
#     prevent_initial_call=True
# )
# def update_bar_chart(_, selected_month, selected_year):
#     if selected_month==['all'] and selected_year==['all']:
#         df_sub = df
#     else:
#         df_sub = df[(df['Month'].isin(selected_month)) & (df['Year'].isin(selected_year))]
#     rt_counts = df['Report Type'].value_counts().sort_values(ascending=False)
#     df['Platform Decision'].fillna("Unknown", inplace=True)
#     color_map = {"Removed": "green", "Demoted": "blue", "No Action": "red", "Unknown": "gray"}
#     fig2 = px.bar(df, x="Report Type", height=600, color="Platform Decision")
#     fig2.update_layout(xaxis_title="Report Types", yaxis_title="Count")
#     return fig2

# if __name__ == '__main__':
#     app.run(debug=True)
