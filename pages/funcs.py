from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


def create_main_graph(df, x, y, title, value):
    if value == 'orders':
        df = df.groupby(x, as_index=False)[y].nunique().sort_values(by=value, ascending=False)
    else:
        df = df.groupby(x, as_index=False)[y].sum().sort_values(by=value, ascending=False)
    fig = px.bar(df, x=x, y=y, text_auto='0.2s', hover_data={x: True, value:':,.0f'},
                 title=f'<b>{value.capitalize()}</b> by {title}').update_layout(yaxis_title=None,
                 xaxis_title=None, margin=dict(l=0, r=0, t=30, b=0), yaxis=dict(showticklabels=False, visible=False),
                 title=dict(font=dict(family='Arial', size=16), x=0.5))
    return fig


def create_graph_card(id, fig, className='p-2'):
    height = "100%"
    card = dbc.Card(
    [dcc.Graph(id=id, figure=fig, style={'height': height}, config={'displayModeBar': False})],
    style={'height': height},
    className=className
)
    return card




def graph_highlight(graph, selected_mark):
    if 'bar' in graph.data[0].type:
        graph["data"][0]["marker"]["opacity"] = [1 if c == selected_mark else 0.2 for c in graph["data"][0]["x"]]
        graph["data"][0]["marker"]["line"]['color'] = ['black' if c == selected_mark else 'grey' for c in graph["data"][0]["x"]]
        graph["data"][0]["marker"]["line"]['width'] = [2 if c == selected_mark else 1 for c in graph["data"][0]["x"]]
    elif 'choropleth' in graph.data[0].type:
        graph["data"][0]["marker"]["line"]['color'] = ['black' if c == selected_mark else 'lavender' for c in graph["data"][0]['locations']]
        graph["data"][0]["marker"]["line"]['width'] = [3 if c == selected_mark else 0.2 for c in graph["data"][0]['locations']]
        graph['data'][0]['z'] = [max(graph['data'][0]['z'] / 1.5) if c == selected_mark else 0 for c in graph["data"][0]['locations']]
    return graph

