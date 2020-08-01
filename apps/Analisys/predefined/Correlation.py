import dash_bootstrap_components as dbc
import dash_html_components as html


def get_row():

    return html.Div([
        html.H3("Matriz de correlación"),
        dbc.Container(html.Img(src="../../assets/correlation.png")),
        html.Br(),
        html.Hr()
    ])