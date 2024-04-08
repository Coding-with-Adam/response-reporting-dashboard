from dash import Dash, html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from datetime import datetime
import dash
from utils.login_handler import require_login
from pages.funcs import create_graph_card


dash.register_page(__name__, path="/insights")
require_login(__name__)


df = pd.read_csv("pages/data.csv")
df.columns = ['timestamp', 'reporting_entity', 'reporting_user', 'platform', 'url', 'report_type', 'screenshot_url', 'answer_date', 'platform_decision', 'policy', 'appeal']
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['answer_date'] = pd.to_datetime(df['answer_date'], errors='coerce')

# primary_color = '#2471A3'  # For example, red
# custom_G10 = list(px.colors.qualitative.G10)
# custom_G10[0] = primary_color

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

df3 = df.copy().dropna(subset=['answer_date'])
df3['response_time'] = (df3['answer_date'] - df3['timestamp']).dt.days
average_response_time = df3.groupby('platform', as_index=False)['response_time'].mean().sort_values(by='response_time', ascending=False)
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
    style={"height": '100vh'}
)
