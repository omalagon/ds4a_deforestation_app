import os

import pandas as pd
import psycopg2


def get_connection():
    return psycopg2.connect(host=os.environ.get('DB_HOST'),
                            dbname=os.environ.get('DB_NAME'),
                            user=os.environ.get('DB_USER'),
                            password=os.environ.get('DB_PSW'))


def get_indicator_grouped_by_municipio(indicator, deptos):
    query = str("""
    with geo as (
    select m.departamento_id as depto_id, d.nombre as depto_nombre, m.id as mun_id, m.nombre as mun_nombre
    from ds4a.municipio m join ds4a.departamento d 
    on m.departamento_id = d.id)

    select data_year as "Año", depto_nombre,  mun_id, mun_nombre as "Municipio", sum(data_value) as "{0}" 
    from ds4a.datos da join geo g
    on da.municipio_id = g.mun_id
    where da.data_category = '{0}'
    group by data_year, depto_nombre, mun_id, mun_nombre
    order by data_year, depto_nombre, mun_id, mun_nombre
    """).format(indicator)
    data = pd.read_sql_query(query, get_connection())
    if deptos:
        if type(deptos) == str:
            deptos = [deptos]

        data = data[data['depto_nombre'].isin(deptos)]

    return data


def get_departamentos():
    query = "select nombre from ds4a.departamento order by nombre"
    return pd.read_sql_query(query, get_connection())


def get_indicadores():
    query = """
        select distinct data_category 
        from ds4a.datos
        order by data_category 
    """
    return pd.read_sql_query(query, get_connection())