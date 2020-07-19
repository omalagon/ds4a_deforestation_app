import dash_bootstrap_components as dbc
import dash_html_components as html

main = html.Div(
    [
        html.H1("About"),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), width=3, className="test_green"),
                dbc.Col(html.Div("One of three columns"), width=9, className="test_blue")
            ]
        ),
    ]
)