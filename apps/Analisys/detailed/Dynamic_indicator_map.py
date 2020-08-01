import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import geopandas
import json

from apps.Analisys.detailed import Analysis_data_handler as data_h
from apps.Analisys.predefined import Analysis_data_handler as data_h_depto

data_dic = {}
selected_indicator = None


def build_departamentos_dropdown():
    return dcc.Dropdown(
        id="dropdown-detailed-analysis-departamentos-filter",
        options=[{'label': depto['nombre'], 'value': depto['nombre']} for _, depto in
                 data_h.get_departamentos().iterrows()],
        placeholder="Seleccione los departamentos",
        value='ANTIOQUIA',
        multi=True,
        clearable=False
    )


def build_indicator_dropdown():
    return dcc.Dropdown(
        id="dropdown-detailed-analysis-indicator-filter",
        options=[{'label': ind['data_category'], 'value': ind['data_category']} for _, ind in
                 data_h.get_indicadores().iterrows()],
        placeholder="Seleccione el indicador",
        value='DEFORESTACION',
        multi=False,
        clearable=False
    )


def build_button():
    return dbc.Button(
        "Aplicar filtro",
        id="button-detailed-analysis",
        className="mr-1",
        color="success"
    )


def build_menu():
    return dbc.Container(
        dbc.Form(
            [
                dbc.Row(html.H3("Filtro")),
                dbc.FormGroup([
                    build_departamentos_dropdown()
                ], className="mr-3"),
                dbc.FormGroup([
                    build_indicator_dropdown()
                ], className="mr-3"),
                build_button(),
                html.Br(),
                html.Hr(),
            ]),
        fluid=True
    )


def get_row(deptos, indicator):
    global data_dic
    data_dic = {}
    indicator_data = data_h.get_indicator_grouped_by_municipio(indicator, deptos)
    indicator_depto = data_h_depto.get_indicator_grouped_by_departamento(indicator, deptos, cache=False)
    graph = px.line(indicator_data, x='Año', y=indicator, color='Municipio', title=f"Nivel de {indicator.lower()} a nivel municipal")
    graph_depto = px.line(indicator_depto, x='Año', y=indicator, color='Departamento', title=f"Nivel de {indicator.lower()} a nivel departamental")
    years = indicator_data['Año'].unique().astype(int)
    build_data_map(indicator_data, years, indicator)

    return html.Div([
        html.H3(indicator),
        dbc.Row([
            dbc.Col(html.Div([dcc.Graph(figure=graph_depto), dcc.Graph(figure=graph)])),
            dbc.Col(html.Div(id='deforestation-level-detailed-output-map'))
        ]),
        build_slider(years),
        html.Br(),
        html.Hr()
    ])


def build_data_map(data, years, indicator):
    columns = ['COD_DEPTO', 'NOMBRE_DEPTO', 'COD_MUNICIPIO', 'NOMBRE_MUNICIPIO', 'LOCATION', 'Año', indicator,
               'geometry']
    template_df = geopandas.read_file('data/mapas/template.geojson')

    for year in years:
        tmp = data[data['Año'] == str(year)]
        data_dic[int(year)] = template_df.merge(tmp, left_on='COD_MUNICIPIO', right_on='mun_id')[columns]


def build_map(year, indicator):
    df_geo = data_dic[year]
    map = px.choropleth_mapbox(pd.json_normalize(json.loads(df_geo.to_json())['features']),  # Data
                                color=f"properties.{indicator}",  # Column giving the color intensity of the region
                                locations='properties.LOCATION',
                                featureidkey='properties.LOCATION',
                                geojson=json.loads(df_geo.to_json()),  # The GeoJSON file
                                zoom=6,  # Zoom
                                mapbox_style="carto-positron",
                                # Mapbox style, for different maps you need a Mapbox account and a token
                                center={"lat": 7.5, "lon": -75.133},  # Center
                                color_continuous_scale="jet",  # Color Scheme
                                opacity=0.5,  # Opacity of the map
                                width=900,
                                height=800
                                )
    return dcc.Graph(figure=map)


def build_slider(years):
    years_dict = {}
    for year in years:
        years_dict[int(year)] = str(year)

    return dbc.Row([
        dbc.Col(),
        dbc.Col([
            dcc.Slider(
                id='deforestation-level-detailed-slider',
                min=years.min(),
                max=years.max(),
                value=years.min(),
                marks=years_dict
            )])
    ])


def register_callback(app):
    @app.callback(
        Output('detailed-output-map', 'children'),
        [
            Input('button-detailed-analysis', 'n_clicks')

        ],
        [
            State('dropdown-detailed-analysis-departamentos-filter', 'value'),
            State('dropdown-detailed-analysis-indicator-filter', 'value')
        ]

    )
    def update_output(clicked, deptos, indicator):
        if clicked:
            global selected_indicator
            selected_indicator = indicator
            return get_row(deptos, indicator)

    @app.callback(
        Output('deforestation-level-detailed-output-map', 'children'),
        [Input('deforestation-level-detailed-slider', 'value')])
    def update_output(value):
        if value is not None:
            return build_map(value, selected_indicator)
