import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

Options = dbc.ButtonGroup(
    [
        dbc.Button("Geográficos",id="raw_geo"),
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Estimaciones_de_Poblacion_2005-2017-Municipal",id="raw_dane_es_po"), 
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Agregado 2016 -2018",id="raw_dane_cnd_2016_2018"), 
                        dbc.DropdownMenuItem("Serie 2016",id="raw_dane_cnd_2016"), 
                        dbc.DropdownMenuItem("Serie 2017",id="raw_dane_cnd_2017"), 
                        dbc.DropdownMenuItem("Serie 2018",id="raw_dane_cnd_2018"), 
                    ],
                    label="Cuentas nacionales departamentales",
                    group=True,
                ),
            ],
            label="DANE",
            group=True,
        ),
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Asesinatos selectivos 1981-2012",id="raw_CMH_AS_1981_2012"), 
                dbc.DropdownMenuItem("SecuestrosColombia1970-2010.csv",id="raw_CMH_SC_1970_2010"), 
            ],
            label="Centro de memoria histórico",
            group=True,
        ),
    ],
    vertical=True,
)

main = html.Div(
    [
        html.Div(id='page-content2'),
        html.H1("Raw data"),
        dbc.Row(
            [
                dbc.Col(html.Div(Options), width=3, className=""),
                dbc.Col(html.Div(id='raw_content',), width=9,className="")
            ]
        ),        
    ]
)

