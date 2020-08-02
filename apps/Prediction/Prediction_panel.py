import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output


departamento_col = 'Departamento'
predicted_deforestation_in_m2_col = 'Deforestación en Metros Cuadrados'
predicted_percentaje_points = 'Porcentaje Deforestación % (Puntos porcentuales)'
columns = [departamento_col, predicted_deforestation_in_m2_col, predicted_percentaje_points]

calc_dict = {
    'ANTIOQUIA': {'one_percentage_gdp': 100.73989393819100, 'deforestation_m2': 2065190.3735487800, 'elasticity': 1.009},
    'BOLIVAR': {'one_percentage_gdp': 21.03007004498830, 'deforestation_m2': 1338722.1893174000, 'elasticity': 2.923},
    'CORDOBA': {'one_percentage_gdp': 90.30350654000300, 'deforestation_m2': 85256.5122694072, 'elasticity': 0.867},
    'CESAR': {'one_percentage_gdp': 19.26754302121350, 'deforestation_m2': 947791.5005296510, 'elasticity': 4.214},
    'CHOCO': {'one_percentage_gdp': 16.78503634420120, 'deforestation_m2': 634369.7426056320, 'elasticity': 0.374},
    'NORTE DE SANTANDER': {'one_percentage_gdp': 18.47801093277040, 'deforestation_m2': 2619771.4625076000, 'elasticity': 2.797},
    'SANTANDER': {'one_percentage_gdp': 68.78323269614540, 'deforestation_m2': 731470.7714521540, 'elasticity': 1.416},
    'SUCRE': {'one_percentage_gdp': 7.36369943666099, 'deforestation_m2': 22208.4573848163, 'elasticity': 0.654}
}


def calculate(project_value):
    df = pd.DataFrame.from_dict(calc_dict).T.reset_index()
    df.rename(columns={'index': departamento_col}, inplace=True)

    df[predicted_deforestation_in_m2_col] = df.apply(lambda x: project_value * x['deforestation_m2'] / x['one_percentage_gdp'], axis=1)
    df[predicted_percentaje_points] = df.apply(lambda x: project_value * x['elasticity'] / x['one_percentage_gdp'], axis=1)

    # Reducing decimal points
    df[predicted_deforestation_in_m2_col] = df[predicted_deforestation_in_m2_col].astype(int)
    df[predicted_percentaje_points] = df[predicted_percentaje_points].apply(lambda x: float("{:.2f}".format(x)))
    df = df[columns]

    return html.Div([
        html.P(f"Para un proyecto de {project_value} mil millones de pesos en la siguiente tabla se muestra en cuánto aumentería "
               f"la deforestación en metros cuadrados y su representación porcentual por cada departamento"),
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)
    ])


def build_menu():
    return dbc.Container(
        dbc.Form(
            [
                html.Br(),
                html.Br(),
                dbc.Row(html.H3("Calculadora para política pública")),
                dbc.FormGroup([
                    html.P("Ingrese el valor del proyecto en miles de millones"),
                    dbc.Input(id="calculator-input", type="number", min=0, value=1),
                    dbc.FormFeedback("El valor ingresado no es válido. Por favor ingrese un valor mayor a 0", valid=False)
                ], className="mr-3"),
                html.Br(),
                html.Br(),
                html.Br(),
            ]),
        fluid=True
    )


main = dbc.Container([
    dbc.Row([
        build_menu(),
        dbc.Container([html.Div(id='calculator')])
    ])
])


def register_callback(app):
    @app.callback(
        Output('calculator', 'children'),
        [Input('calculator-input', 'value')]

    )
    def update_output(project_value):
        if project_value and project_value > 0:
            return calculate(project_value)

    @app.callback([Output('calculator-input', 'valid'), Output('calculator-input', 'invalid')],
                  [Input('calculator-input', 'value')])
    def validate_value(value):
        valid = value and float(value) > 0
        return valid, not valid
