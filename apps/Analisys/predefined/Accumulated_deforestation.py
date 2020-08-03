import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import geopandas
import json
from lib.map_builder import build_map_figure

from apps.Analisys.predefined import Analysis_data_handler as data_h

data_dic = {}


def register_callback(app):
    @app.callback(
        Output('accumulated-deforestation-level-output-map', 'children'),
        [Input('accumulated-deforestation-level-slider', 'value')])
    def update_output(value):
        if value is not None:
            return build_map(value)


def get_row():
    indicator = 'DEFORESTACION'
    deforestation_data = data_h.get_accumulated_indicator_depto(indicator)
    deforestation_graph = px.line(deforestation_data, x='Año', y=indicator, color='Departamento')
    years = deforestation_data['Año'].unique().astype(int)
    build_data_map(deforestation_data, years)

    return html.Div([
        html.H3("Deforestación acumulada - Departamento"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=deforestation_graph)),
            dbc.Col(html.Div(id='accumulated-deforestation-level-output-map'))
        ]),
        build_slider(years),
        html.Br(),
        html.Hr()
    ])


def build_data_map(data, years):
    columns = ['COD_DEPTO', 'NOMBRE_DEPTO', 'COD_MUNICIPIO', 'NOMBRE_MUNICIPIO', 'LOCATION', 'Año', 'DEFORESTACION',
               'geometry']
    template_df = geopandas.read_file('data/mapas/template.geojson')

    for year in years:
        tmp = data[data['Año'] == str(year)]
        data_dic[int(year)] = template_df.merge(tmp, left_on='COD_DEPTO', right_on='depto_id')[columns]


def build_map(year):
    df_geo = data_dic[year]
    map_figure = build_map_figure(pd.json_normalize(json.loads(df_geo.to_json())['features']),
                                  json.loads(df_geo.to_json()),
                                  'DEFORESTACION')

    return dcc.Graph(figure=map_figure)


def build_slider(years):
    years_dict = {}
    for year in years:
        years_dict[int(year)] = str(year)

    return dbc.Row([
        dbc.Col(),
        dbc.Col([
            dcc.Slider(
                id='accumulated-deforestation-level-slider',
                min=years.min(),
                max=years.max(),
                value=years.min(),
                marks=years_dict
            )])
    ])
