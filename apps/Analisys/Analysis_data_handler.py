import os

import pandas as pd
import psycopg2

# Indicators data is cached in order to avoid too many queries on the database
indicators_cache = {}


def set_indicator(indicator, data):
    if indicator not in indicators_cache:
        indicators_cache[indicator] = data


def get_connection():
    return psycopg2.connect(host=os.environ.get('DB_HOST'),
                            dbname=os.environ.get('DB_NAME'),
                            user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PSW'))


def get_indicator_grouped_by_departamento(indicator):
    if indicator in indicators_cache:
        return indicators_cache[indicator]

    query = str("""
    with geo as (
    select m.departamento_id as depto_id, d.nombre as depto_nombre, m.id as mun_id, m.nombre as mun_nombre
    from ds4a.municipio m join ds4a.departamento d 
    on m.departamento_id = d.id)

    select data_year as "Año", depto_id, depto_nombre as "Departamento", sum(data_value) as "{0}" 
    from ds4a.datos da join geo g
    on da.municipio_id = g.mun_id
    where da.data_category = '{0}'
    group by data_year, depto_id, depto_nombre
    order by data_year, depto_id, depto_nombre
    """).format(indicator)
    data = pd.read_sql_query(query, get_connection())
    set_indicator(indicator, data)

    return data


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

        select data_year as "Año", depto_id, depto_nombre as "Departamento", sum(data_value) as "TOTAL_BOSQUE" 
        from ds4a.datos da join geo g
        on da.municipio_id = g.mun_id
        where da.data_category ='BOSQUE' and da.data_year = '2002'
        group by data_year, depto_id, depto_nombre
        order by data_year, depto_id, depto_nombre

    """
    total_forest_loss_2002 = pd.read_sql_query(query, get_connection())
    deforestation = get_accumulated_indicator_depto('DEFORESTACION')

    deforestation = deforestation.apply(lambda row: calculate_forest_loss_percentage(row, total_forest_loss_2002),
                                        axis=1)
    deforestation = deforestation[deforestation['Año'] != '2002']

    set_indicator(indicator, deforestation)

    return deforestation


def calculate_forest_loss_percentage(row, forest_2002):
    row['PERDIDA_BOSQUE'] = float(
        row['DEFORESTACION'] / forest_2002[forest_2002['Departamento'] == row['Departamento']]['TOTAL_BOSQUE'] * 100)
    return row