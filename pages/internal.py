from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from datetime import datetime
import dash_ag_grid as dag
import pandas as pd
import dash
from utils.login_handler import require_login



dash.register_page(__name__, path="/internal")
require_login(__name__)


df = pd.read_csv("pages/reports.csv")
df["response-day"] = pd.to_datetime(df["response-day"]).dt.strftime('%Y-%m-%d')
df["flag-day"] = pd.to_datetime(df["flag-day"]).dt.strftime('%Y-%m-%d')


cols = [
    {
        "headerName": "User",
        "field": "vetted-user",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["vetted-user"].unique()}
    },
    {
        "headerName": "Platform",
        "field": "platform",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["platform"].unique()}
    },
    {
        "headerName": "Content link",
        "field": "content-link",
    },
    {
        "headerName": "Flag type",
        "field": "flag-type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["flag-type"].unique()}
    },
    {
        "headerName": "Flag day",
        "field": "flag-day",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {'min': '2024-01-01'}
    },
    {
        "headerName": "Response type",
        "field": "response-type",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values": df["response-type"].unique()}
    },
    {
        "headerName": "Response notes",
        "field": "response-notes",
    },
    {
        "headerName": "Response day",
        "field": "response-day",
        "filter": "agDateColumnFilter",
        'cellEditor': 'agDateStringCellEditor',
        'cellEditorParams': {
            'min': '2024-01-01',
        }
    }
]


layout = dmc.MantineProvider(
    # theme={"colorScheme": "dark"},
    # withGlobalStyles=True,
    children=[
        dcc.Store(id='data-store', data=df.to_json()),
        html.H5(id='username', className='fw-bold text-black mt-2'),
        dag.AgGrid(
            id="reports-table",
            rowData=df.to_dict("records"),
            columnDefs=cols,
            columnSize="sizeToFit",
            defaultColDef={"editable": True, "filter": True},
            dashGridOptions={"pagination": True,
                             "paginationPageSize": 7,
                             "undoRedoCellEditing": True,
                             "rowSelection": "multiple"}
        ),
        dbc.Button(
            id="delete-row-btn",
            children="Delete row",
        ),
        dbc.Button(
            id="add-row-btn",
            children="Add row",
        ),
    ]
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
            "vetted-user": ["user1"],
            "platform": [""],
            "content-link": [""],
            # "image-link": [""],
            "flag-type": [""],
            "flag-day": [""],
            "response-type": [""],
            "response-notes": [""],
            "response-day": [""]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat(
            [pd.DataFrame(data), df_new_row]
        )  # add new row to orginal dataframe
        print(updated_table.tail())
        return False, updated_table.to_dict("records")

    elif ctx.triggered_id == "delete-row-btn":
        return True, no_update, no_update

