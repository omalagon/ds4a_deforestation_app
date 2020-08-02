import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps.Analisys.predefined import Deforestation_level, Forest_loss, Accumulated_deforestation, Correlation, Cluster
from apps.Analisys.detailed import Dynamic_indicator_map as Dynamic_municipality_indicator_map

main = html.Div(
    [
        dcc.Store(id="store"),
        html.Br(),
        dbc.Tabs(
            [
                dbc.Tab(label="Predefinido", tab_id="predefined"),
                dbc.Tab(label="Detalle indicadores", tab_id="detailed"),
            ],
            id="tabs",
            active_tab="predefined",
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
            if active_tab == "predefined":
                rows = [
                    Deforestation_level.get_row(),
                    Accumulated_deforestation.get_row(),
                    Forest_loss.get_row(),
                    Correlation.get_row(),
                    Cluster.get_row()
                ]
                return html.Div(rows)
            elif active_tab == "detailed":
                rows = [
                    Dynamic_municipality_indicator_map.build_menu(),
                    html.Div(id='detailed-output-map')
                ]
                return html.Div(rows)
        return "No tab selected"

