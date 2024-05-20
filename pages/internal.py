import dash
from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update, clientside_callback
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from datetime import datetime
from datetime import date
import dash_ag_grid as dag
import pandas as pd
from utils.login_handler import require_login

dash.register_page(__name__)
require_login(__name__)


df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/dummy_data_100_wNan.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime('%Y-%m-%d')
df["Answer Date"] = pd.to_datetime(df["Answer Date"]).dt.strftime('%Y-%m-%d')
rowData = df.to_dict("records")


cols = [
    {
        "headerName": "Timestamp",
        "field": "Timestamp"
    },
    {
        "headerName": "Reporting Entity",
        "field": "Reporting Entity",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Reporting Entity"].unique()}
    },
    {
        "headerName": "Reporting User",
        "field": "Reporting User",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Reporting User"].unique()}
    },
    {
        "headerName": "Platform",
        "field": "Platform",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Platform"].unique()}
    },
    {
        "headerName": "URL",
        "field": "URL",
    },
    {
        "headerName": "Report Type",
        "field": "Report Type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Report Type"].unique()}
    },
    {
        "headerName": "Screenshot URL",
        "field": "Screenshot URL",
    },
    {
        "headerName": "Answer Date",
        "field": "Answer Date",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {'min': '2023-01-01'}
    },
    {
        "headerName": "Platform Decision",
        "field": "Platform Decision",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Platform Decision"].unique()}
    },
    {
        "headerName": "Policy",
        "field": "Policy",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Policy"].unique()}
    },
    {
        "headerName": "Appeal",
        "field": "Appeal",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Appeal"].unique()}
    }
]



layout = dbc.Container(
    children=[
        html.Br(),
        # html.H1("Transparency Reporting Platform - Internal"),
        # dmc.Center(html.H4('This page content to be visible after vetted user has logged in.')),
        dbc.Row([
            dbc.Col([
                html.H5(id='username', className='fw-bold text-black mt-2'),
                dag.AgGrid(
                    id="reports-table",
                    rowData=rowData,
                    getRowId="params.data.id",
                    columnDefs=cols,
                    columnSize="sizeToFit",
                    defaultColDef={"editable": True, "filter": True},
                    dashGridOptions={
                                    # "pagination": True,
                                    #  "paginationPageSize": 7,
                                     "undoRedoCellEditing": True,
                                     "rowSelection": "multiple",
                                     "animateRows": False}
                )
            ], width=12)
        ]),
        dbc.Button(
            id="delete-row-btn",
            children="Delete row",
        ),
        dbc.Button(
            id="add-row-btn",
            children="Add row",
        ),
        html.Br(),
        dcc.Input(id='dd-scroll-to-data', type='text'),

    ], 	fluid = True
)


@callback(
    Output("reports-table", "deleteSelectedRows"),
    Output("reports-table", "rowData"),
    Input("delete-row-btn", "n_clicks"),
    Input("add-row-btn", "n_clicks"),
    State("reports-table", "rowData"),
    prevent_initial_call=True,
)
def update_table(n_dlt, n_add, data):
    if ctx.triggered_id == "add-row-btn":
        new_row = {
            "Timestamp": [date.today().isoformat()],
            "Reporting Entity": [""],
            "Reporting User": [""],
            "Platform": [""],
            "URL": [""],
            "Report Type": [""],
            "Screenshot URL": [""],
            "Answer Date": [""],
            "Platform Decision": [""],
            "Policy": [""],
            "Appeal": [""]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat(
            [pd.DataFrame(data), df_new_row]
        )  # add new row to orginal dataframe
        return False, updated_table.to_dict("records")

    elif ctx.triggered_id == "delete-row-btn":
        return True, no_update

@callback(
    Output("reports-table", "scrollTo"),
    Input("dd-scroll-to-data", "value"),
    prevent_initial_call=True,
)
def scroll_to_data(value):
    if value is None:
        return no_update
    for row in rowData:
        if row["Platform"] == value:
            break
    return {"data": row}



