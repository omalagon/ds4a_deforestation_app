from dash.dependencies import Input, Output
import dash_html_components as html
import datetime
import dash
import dash_table
import pandas as pd


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
    def display(raw_dane_es_po, raw_dane_cnd_2016_2018, raw_dane_cnd_2016, raw_dane_cnd_2017, raw_dane_cnd_2018,
                raw_CMH_AS_1981_2012, raw_CMH_SC_1970_2010):
        print('->');
        ctx = dash.callback_context
        if ctx.triggered:
            caso = ctx.triggered[0]['prop_id'].split('.')[0]
            if (caso == 'raw_dane_es_po'):
                return CreateTableFromFile("data/Dane/anexo-Estimaciones_de_Poblacion_2005-2017-Municipal.csv", '\t',
                                           'anexo-Estimaciones_de_Poblacion_2005-2017-Municipal');
            if (caso == 'raw_dane_cnd_2016_2018'):
                return CreateTableFromFile("data/Dane/2018-provisional-valor-agregado-municipio.txt", '\t',
                                           'Cuentas nacionales departamentales consolidado 2016-2018');
            if (caso == 'raw_dane_cnd_2016'):
                return CreateTableFromFile("data/Dane/2018-provisional-valor-agregado-municipio_2016.txt", '\t',
                                           'Cuentas nacionales departamentales 2016');
            if (caso == 'raw_dane_cnd_2017'):
                return CreateTableFromFile("data/Dane/2018-provisional-valor-agregado-municipio_2017.txt", '\t',
                                           'Cuentas nacionales departamentales 2017');
            if (caso == 'raw_dane_cnd_2018'):
                return CreateTableFromFile("data/Dane/2018-provisional-valor-agregado-municipio_2018.txt", '\t',
                                           'Cuentas nacionales departamentales 2018');
            if (caso == 'raw_CMH_AS_1981_2012'):
                return CreateTableFromFile("data/CentroMemoriaHistorico/AsesinatosSelectivos1981-2012.csv", ',',
                                           'Asesinatos en colombia 1981 - 2012');
            if (caso == 'raw_CMH_SC_1970_2010'):
                return CreateTableFromFile("data/CentroMemoriaHistorico/SecuestrosColombia1970-2010.csv", ',',
                                           'Secuestros en colombia 1970 - 2010');
            else:
                return 'No implementado: ' + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S");
        return ''

    def CreateTableFromFile(file, demitador, titulo):
        print('Inicia lectura de: ' + file);
        df = pd.read_csv(file, delimiter=demitador, decimal=".", encoding='ISO-8859-1', skiprows=0, nrows=20);
        print(df.describe());
        return html.Div(
            [
                html.H1(titulo),
                html.Div([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df[0:100].to_dict('records'),
                        merge_duplicate_headers=True
                    )
                ], className="tablas scroll", ),
            ]
        );