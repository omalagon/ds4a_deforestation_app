import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

cluster_dict = {
    '2002': "../../assets/cluster_2002.png",
    '2004': "../../assets/cluster_2004.png",
    '2006': "../../assets/cluster_2006.png",
    '2008': "../../assets/cluster_2008.png",
    '2010': "../../assets/cluster_2010.png",
    '2012': "../../assets/cluster_2012.png",
    '2013': "../../assets/cluster_2013.png",
    '2014': "../../assets/cluster_2014.png",
    '2015': "../../assets/cluster_2015.png",
    '2016': "../../assets/cluster_2016.png",
    '2017': "../../assets/cluster_2017.png",
}


def get_row():
    return html.Div([
        html.H3("Autocorrelación espacial"),
        dbc.Container([
            dbc.Row(dbc.Container(id="cluster-image", style={'textAlign': 'center'})),
            html.Br(), html.Br(),
            dbc.Row(dbc.Container(build_slider(pd.DataFrame.from_dict(cluster_dict.keys()).astype(int)[0])))
        ]),
        html.Br()
    ])


def build_slider(years):
    years_dict = {}
    for year in years:
        years_dict[int(year)] = str(year)

    return dcc.Slider(
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

