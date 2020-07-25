import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import psycopg2
from dash.dependencies import Input, Output

# Indicators data is cached in order to avoid too many queries on the database
indicators_cache = {}


def set_indicator(indicator, data):
    if indicator not in indicators_cache:
        indicators_cache[indicator] = data


main = dbc.Container(
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


# TODO: use env variables
def get_connection():
    return psycopg2.connect(host="ds4a-demo-instance.cuhhesolnyxt.us-east-2.rds.amazonaws.com",
                            dbname="team34_deforestation",
                            user="postgres",
                            password="oscarmalagon")


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
                depto_graphs = generate_depto_graphs()
                rows = []
                for title in depto_graphs:
                    rows.append(html.H3(title))
                    rows.append(dcc.Graph(figure=depto_graphs[title]))
                    rows.append(html.Hr())

                return dbc.Container(rows)
            elif active_tab == "municipio":
                return dbc.Row(html.H3("Coming soon..."))
        return "No tab selected"


def generate_depto_graphs():
    deforestation = get_indicator_graph_grouped_by_departamento('DEFORESTACION')
    accumulated_deforestation = get_accumulated_indicator_graph_grouped_by_departamento('DEFORESTACION')
    forest_loss = get_forest_loss_graph()

    data = {'Niveles de deforestación': deforestation,
            'Deforestación acumulada': accumulated_deforestation,
            '% Perdida de Bosque': forest_loss}

    return data


def get_indicator_grouped_by_departamento(indicator):
    if indicator in indicators_cache:
        return indicators_cache[indicator]

    query = str("""
    with geo as (
    select m.departamento_id as depto_id, d.nombre as depto_nombre, m.id as mun_id, m.nombre as mun_nombre
    from ds4a.municipio m join ds4a.departamento d 
    on m.departamento_id = d.id)
    
    select data_year as "Año", depto_nombre as "Departamento", sum(data_value) as "{0}" 
    from ds4a.datos da join geo g
    on da.municipio_id = g.mun_id
    where da.data_category = '{0}'
    group by data_year, depto_nombre
    order by data_year, depto_nombre
    """).format(indicator)
    data = pd.read_sql_query(query, get_connection())
    set_indicator(indicator, data)

    return data


# Indicator
def get_indicator_graph_grouped_by_departamento(indicator):
    df = get_indicator_grouped_by_departamento(indicator)

    return px.line(df, x='Año', y=indicator, color='Departamento')


# Accumulated indicator
def get_accumulated_indicator_depto(indicator):
    df = get_indicator_grouped_by_departamento(indicator)

    years = pd.Series(df['Año'].unique())
    year_base = years.iloc[0]
    deptos = pd.Series(df['Departamento'].unique())

    df_acc = []
    for depto in deptos:
        df_depto = df[df['Departamento'] == depto]
        dfs_result = [df_depto[df_depto['Año'] == year_base].reset_index()]

        for current in years.iloc[1:]:
            data_previous = dfs_result[-1]
            data_current = df_depto[df_depto['Año'] == current].reset_index()

            data_current[indicator] = (data_current[indicator] + data_previous[indicator])

            dfs_result.append(data_current)
        df_acc.append(pd.concat(dfs_result, ignore_index=True))

    return pd.concat(df_acc)


def get_accumulated_indicator_graph_grouped_by_departamento(indicator):
    df = get_accumulated_indicator_depto(indicator)

    return px.line(df, x='Año', y=indicator, color='Departamento')


# Loss
def calculate_forest_loss(entry, total_forest_loss_2002):
    total_depto = total_forest_loss_2002[total_forest_loss_2002['Departamento'] == entry['Departamento']]

    return entry['DEFORESTACION'] / total_depto


def get_forest_loss():
    indicator = 'PERDIDA_BOSQUE'
    if indicator in indicators_cache:
        return indicators_cache[indicator]

    query = """
        with geo as (
        select m.departamento_id as depto_id, d.nombre as depto_nombre, m.id as mun_id, m.nombre as mun_nombre
        from ds4a.municipio m join ds4a.departamento d 
        on m.departamento_id = d.id)
        
        select data_year as "Año", depto_nombre as "Departamento", sum(data_value) as "TOTAL_BOSQUE" 
        from ds4a.datos da join geo g
        on da.municipio_id = g.mun_id
        where da.data_category ='BOSQUE' and da.data_year = '2002'
        group by data_year, depto_nombre
        order by data_year, depto_nombre

    """
    total_forest_loss_2002 = pd.read_sql_query(query, get_connection())
    deforestation = get_accumulated_indicator_depto('DEFORESTACION')

    deforestation = deforestation.apply(lambda row: calculate_forest_loss_percentage(row, total_forest_loss_2002), axis=1)
    deforestation = deforestation[deforestation['Año'] != '2002']

    set_indicator(indicator, deforestation)

    return deforestation


def calculate_forest_loss_percentage(row, forest_2002):
    row['PERDIDA_BOSQUE'] = float(row['DEFORESTACION'] / forest_2002[forest_2002['Departamento'] == row['Departamento']]['TOTAL_BOSQUE'] * 100)
    return row


def get_forest_loss_graph():
    df = get_forest_loss()

    return px.line(df, x='Año', y='PERDIDA_BOSQUE', color='Departamento')
