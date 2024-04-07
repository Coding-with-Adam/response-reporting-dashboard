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

colors = {'google': '#2471A3', 'facebook': 'red', 'instagram': 'green'}


df = pd.read_csv("pages/reports.csv")
df['flag-day'] = pd.to_datetime(df['flag-day'])
df['response-day'] = pd.to_datetime(df['response-day'], errors='coerce')


df_pie = df.groupby('platform', as_index=False)['content-link'].size()
fig1 = px.pie(df_pie, values='size', names='platform', hole=.5, title='Reports per Platform',
                color='platform', color_discrete_map=colors).update_traces(marker=dict(line=dict(color='#FFFFFF', width=2)))\
                .update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5),
                legend=dict(xanchor='right', x=1))

df_line = df.groupby(['flag-day', 'platform'], as_index=False)['platform'].size()
fig2 = px.line(df_line, x='flag-day', y='size', color='platform', color_discrete_map=colors, title='Daily reports by Platform', markers=True,
              labels={'Date': 'flag-day', 'Count': 'size', 'Platform': 'platform'}).update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5),
                   )


df3 = df.copy()
df3 = df3.dropna(subset=['response-day'])
df3['response_time'] = (df3['response-day'] - df3['flag-day']).dt.days
average_response_time = df3.groupby('platform', as_index=False)['response_time'].mean()
fig3 = px.bar(average_response_time, x='platform', y='response_time', title='Responce time by platform', color='platform',
            color_discrete_map=colors).update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5),
            showlegend=False)




fig4 = px.histogram(df, x='response-type', color='platform', title='Responses by Platform', barmode='group', color_discrete_map=colors).\
    update_layout(margin=dict(l=0, r=0, t=30, b=0)).update_traces(marker=dict(line=dict(color='#FFFFFF', width=2))).update_layout(margin=dict(l=0, r=0, t=30, b=5), title=dict(font=dict(family='Arial', size=16), x=0.5),
                   legend=dict(xanchor='right', x=1))

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

#'background-color': '#F8F9F9',