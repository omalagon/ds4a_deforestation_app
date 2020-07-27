import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps.Analisys import Deforestation_level, Forest_loss
from apps.Analisys import Accumulated_deforestation


main = html.Div(
    [
        dcc.Store(id="store"),
        html.Br(),
        dbc.Tabs(
            [
                dbc.Tab(label="Departamento", tab_id="depto"),
                dbc.Tab(label="Municipio", tab_id="municipio"),
            ],
            id="tabs",
            active_tab="depto",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


# TODO: add button to force data refresh
def register_callback(app):
    @app.callback(
        Output("tab-content", "children"),
        [Input("tabs", "active_tab")]
    )
    def render_tab_content(active_tab):
        """
        This callback takes the 'active_tab' property as input, as well as the
        stored graphs, and renders the tab content depending on what the value of
        'active_tab' is.
        """
        if active_tab:
            if active_tab == "depto":
                rows = [
                    Deforestation_level.get_row(),
                    Accumulated_deforestation.get_row(),
                    Forest_loss.get_row()
                ]
                return html.Div(rows)
            elif active_tab == "municipio":
                return dbc.Row(html.H3("Coming soon..."))
        return "No tab selected"

