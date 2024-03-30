from dash import Dash, html, dcc, callback, Output, Input, State, ctx, no_update
import dash_ag_grid as dag
import pandas as pd
import dash_mantine_components as dmc
from datetime import datetime

df = pd.read_csv("reports.csv")


app = Dash()
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalStyles=True,
    children=[
        html.H1("Transparency Reporting Platform - Internal Page"),
        dmc.Center(html.H4('This page content to be visible after vetted user has logged in.')),
        dag.AgGrid(
            id="reports-table",
            rowData=df.to_dict("records"),
            columnDefs=[{"field": i} for i in df.columns],
            columnSize="sizeToFit",
            defaultColDef={"editable": True},
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
            "vetted-user": ["user1"],
            "platform": [""],
            "content-link": [""],
            "report-type": [""],
            "report-time": [""],
            "response-type": [""],
            "response-notes": [""],
            "response-time": [""]
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
