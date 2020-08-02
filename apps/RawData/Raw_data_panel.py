import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
import datetime
import dash
import pandas as pd
import boto3
import io

dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem("Ir a visualizador", active=True, href="/RawData"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("DANE", header=True),
        dbc.DropdownMenuItem("Estimaciones de Poblacion 2005-2017 Municipal", id="raw_dane_es_po"),
        dbc.DropdownMenuItem("DANE - Cuentas nacionales departamentales", header=True),
        dbc.DropdownMenuItem("Agregado 2016-2018", id="raw_dane_cnd_2016_2018"),
        dbc.DropdownMenuItem("Serie 2016", id="raw_dane_cnd_2016"),
        dbc.DropdownMenuItem("Serie 2017", id="raw_dane_cnd_2017"),
        dbc.DropdownMenuItem("Serie 2018", id="raw_dane_cnd_2018"),
        dbc.DropdownMenuItem("Centro de Memoria Histórico", header=True),
        dbc.DropdownMenuItem("Asesinatos selectivos 1981-2012", id="raw_CMH_AS_1981_2012"),
        dbc.DropdownMenuItem("Secuestros Colombia 1970-2010", id="raw_CMH_SC_1970_2010")
    ],
    label="Datos",
    color="primary",
    in_navbar=True,
    nav=True
)

main = dbc.Container(
    [
        html.Div(id='page-content2'),
        html.Br(),
        html.H2("Visualizador"),
        html.P("Seleccione el conjunto de datos que desea visualizar en el menú 'Datos'. "),
        dbc.Alert("Solo se muestra una parte del archivo, para más detalle lo puede "
                  "descargar en el correspondiente enlace", color='warning'),
        html.Div(id='raw_content')
    ]
)


s3 = boto3.client(service_name='s3', region_name="sa-east-1")
base_s3_url = "https://deforestation-app.s3-sa-east-1.amazonaws.com/"

file_dict = {
    'raw_dane_es_po':
        {'file_key': "Dane/anexo-Estimaciones_de_Poblacion_2005-2017-Municipal.csv",
         'sep': '\t',
         'encoding': 'UTF-8',
         'title': 'Estimaciones de Poblacion 2005-2017 Municipal'},
    'raw_dane_cnd_2016_2018':
        {'file_key': "Dane/2018-provisional-valor-agregado-municipio.txt",
         'sep': '\t',
         'encoding': 'UTF-8',
         'title': 'Cuentas nacionales departamentales consolidado 2016-2018'},
    'raw_dane_cnd_2016':
        {'file_key': "Dane/2018-provisional-valor-agregado-municipio_2016.txt",
         'sep': '\t',
         'encoding': 'UTF-8',
         'title': 'Cuentas nacionales departamentales 2016'},
    'raw_dane_cnd_2017':
        {'file_key': "Dane/2018-provisional-valor-agregado-municipio_2017.txt",
         'sep': '\t',
         'encoding': 'UTF-8',
         'title': 'Cuentas nacionales departamentales 2017'},
    'raw_dane_cnd_2018':
        {'file_key': "Dane/2018-provisional-valor-agregado-municipio_2018.txt",
         'sep': '\t',
         'encoding': 'UTF-8',
         'title': 'Cuentas nacionales departamentales 2018'},
    'raw_CMH_AS_1981_2012':
        {'file_key': "CentroMemoriaHistorico/AsesinatosSelectivos1981-2012.csv",
         'sep': ',',
         'encoding': 'ISO-8859-1',
         'title': 'Asesinatos en colombia 1981 - 2012'},
    'raw_CMH_SC_1970_2010':
        {'file_key': "CentroMemoriaHistorico/SecuestrosColombia1970-2010.csv",
         'sep': ',',
         'encoding': 'ISO-8859-1',
         'title': 'Secuestros en Colombia 1970 - 2010'}
}


def register_callback(app):
    @app.callback(Output('raw_content', 'children'),
                  [
                      Input('raw_dane_es_po', 'n_clicks'),
                      Input('raw_dane_cnd_2016_2018', 'n_clicks'),
                      Input('raw_dane_cnd_2016', 'n_clicks'),
                      Input('raw_dane_cnd_2017', 'n_clicks'),
                      Input('raw_dane_cnd_2018', 'n_clicks'),
                      Input('raw_CMH_AS_1981_2012', 'n_clicks'),
                      Input('raw_CMH_SC_1970_2010', 'n_clicks'),
                  ])
    def display(raw_dane_es_po, raw_dane_cnd_2016_2018, raw_dane_cnd_2016, raw_dane_cnd_2017,
                raw_dane_cnd_2018, raw_CMH_AS_1981_2012, raw_CMH_SC_1970_2010):
        ctx = dash.callback_context
        if ctx.triggered:
            caso = ctx.triggered[0]['prop_id'].split('.')[0]
            if caso in file_dict:
                found_file = file_dict.get(caso)

                return create_table_from_file(found_file['file_key'],
                                              found_file['sep'],
                                              found_file['encoding'],
                                              found_file['title'])

            else:
                return 'No implementado: ' + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S");
        return ''

    def create_table_from_file(file, demitador, encoding, titulo):
        print('Inicia lectura de: ' + file)
        obj = s3.get_object(Bucket='deforestation-app', Key=file)

        df = pd.read_csv(io.BytesIO(obj['Body'].read()),
                         delimiter=demitador,
                         decimal=".",
                         encoding=encoding,
                         skiprows=0,
                         nrows=20)
        df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

        return html.Div(
            [
                html.H1(titulo),
                html.A("Descargar..", href=f"{base_s3_url}{file}", target="_blank"),
                html.Br(),
                html.Div(dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True))
            ]
        )
