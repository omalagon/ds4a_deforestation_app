import dash_bootstrap_components as dbc

from apps.RawData.Raw_data_panel import dropdown

menu = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dropdown),
        dbc.NavItem(dbc.NavLink("Análisis", href="/Analisys")),
        dbc.NavItem(dbc.NavLink("Predicciones", href="/Predictions")),
        dbc.NavItem(dbc.NavLink("Acerca", href="/About")),
    ],
    brand="Deforestation Predictor (DS4)",
    brand_href="#",
    color="primary",
    dark=True,
)
