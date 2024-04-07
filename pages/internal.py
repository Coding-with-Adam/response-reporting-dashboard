from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_mantine_components as dmc
from datetime import datetime
from datetime import date
import dash_ag_grid as dag
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/response-reporting-dashboard/main/dummy_data_100_wNan.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime('%Y-%m-%d')
df["Answer Date"] = pd.to_datetime(df["Answer Date"]).dt.strftime('%Y-%m-%d')


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


app = Dash()
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        html.H1("Transparency Reporting Platform - Internal"),
        dmc.Center(html.H4('This page content to be visible after vetted user has logged in.')),
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
        dmc.Button(
            id="delete-row-btn",
            children="Delete row",
        ),
        dmc.Button(
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



if __name__ == '__main__':
    app.run_server(debug=True)
