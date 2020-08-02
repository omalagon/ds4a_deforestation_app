import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

cluster_dict = {
    '2001': "../../assets/carolina.jpeg",
    '2002': "../../assets/carlos.jpeg",
    '2003': "../../assets/dario.jpeg",
    '2004': "../../assets/manuel.jpeg",
    '2005': "../../assets/oscar.png"
}


def get_row():
    return html.Div([
        html.H3("Cluster"),
        dbc.Container([
            dbc.Row([
                dbc.Container(id="cluster-image", style={'textAlign': 'center'}),
                dbc.Container(build_slider(pd.DataFrame.from_dict(cluster_dict.keys()).astype(int)[0]))
            ])
        ]),
        html.Br()
    ])


def build_slider(years):
    years_dict = {}
    for year in years:
        years_dict[int(year)] = str(year)

    return dcc.Slider (
        id='cluster-slider',
        min=years.min(),
        max=years.max(),
        value=years.min(),
        marks=years_dict
    )


def register_callback(app):
    @app.callback(
        Output('cluster-image', 'children'),
        [Input('cluster-slider', 'value')])
    def update_output(key):
        if key is not None:
            return html.Img(src=cluster_dict[str(key)])

