from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update, register_page
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd

register_page(__name__)

df = pd.read_csv("assets/reports.csv")
df["Answer Date"] = pd.to_datetime(df["Answer Date"]).dt.strftime('%Y-%m-%d')
df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime('%Y-%m-%d')

cols = [
    {
        "headerName": "Report Date",
        "field": "Timestamp",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor'
    },
    {
        "headerName": "Reporting Entity",
        "field": "Reporting Entity",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Reporting Entity"].unique()}
    },
    {
        "headerName": "User",
        "field": "Reporting User"
    },
    {
        "headerName": "Platform",
        "field": "Platform",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Platform"].unique()}
    },
    {
        "headerName": "Content URL",
        "field": "URL",
    },
    {
        "headerName": "Report Type",
        "field": "Report Type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["Report Type"].unique()}
    },
    {
        "headerName": "Answer Date",
        "field": "Answer Date",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {
            'min': '2024-01-01',
        }
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
    },
    {
    "headerName" : "Appeal",
    "field" : "Appeal",
    "cellEditor" : "agSelectCellEditor",
    "cellEditorParams" : {"values" : ["Yes", "No"]}
    }
]



layout = dbc.Container([
        html.H1("Internal", style = {"text-align":"center"}),
        dmc.Center(html.H4("Update existing report or insert a new report.")),
        dag.AgGrid(
            id="reports-table",
            rowData=df.to_dict("records"),
            columnDefs = cols,
            columnSize = "sizeToFit",
            defaultColDef = {"editable": True, "filter": True},
            dashGridOptions = {"pagination": True,
                             "paginationPageSize": 7,
                             "undoRedoCellEditing": True,
                             "rowSelection": "multiple"}
        ),
        dbc.Button(
            id="delete-row-btn",
            children="Delete row",
            color = "danger",
            class_name = "me-1 mt-1",
        ),
        dbc.Button(
            id="add-row-btn",
            children="Add row",
            color = "primary",
            class_name = "me-1 mt-1",
        ),
    ],
    fluid = True #To fit the size of the screen
)


@callback(
    Output("reports-table", "deleteSelectedRows"),
    Output("reports-table", "rowData"),
    Input("delete-row-btn", "n_clicks"),
    Input("add-row-btn", "n_clicks"),
    State("reports-table", "rowData"),
    prevent_initial_call = True,
)
def update_table(n_dlt, n_add, data):
    if ctx.triggered_id == "add-row-btn":
        new_row = {
            "Timestamp" : [""],
            "Reporting Entity" : [""],
            "Reporting User" : [""],
            "Platform" : [""],
            "URL" : [""],
            "Report Type" : [""],
            "Answer Date" : [""],
            "Platform Decision" : [""],
            "Policy" : [""],
            "Appeal" : [""]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat(
            [pd.DataFrame(data), df_new_row]
        )  # add new row to orginal dataframe
        return False, updated_table.to_dict("records")

    elif ctx.triggered_id == "delete-row-btn":
        return True, no_update
