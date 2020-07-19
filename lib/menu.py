import dash_bootstrap_components as dbc
menu = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Raw Data", href="/RawData")),
        dbc.NavItem(dbc.NavLink("Analysis", href="/Analisys")),
        dbc.NavItem(dbc.NavLink("Predictions", href="/Predictions")),
        dbc.NavItem(dbc.NavLink("About", href="/About")),
    ],
    brand="Deforestation Predictor (DS4)",
    brand_href="#",
    color="primary",
    dark=True,
)