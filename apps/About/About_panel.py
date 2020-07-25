import dash_bootstrap_components as dbc
import dash_html_components as html

main = html.Div(
    [
        html.Br(),
        html.Br(),
        html.Center(html.H1(html.Strong("Team 34"))),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="../../assets/carolina.jpeg", top=True),
                        dbc.CardBody(
                            [
                                html.H4(html.Strong("Carolina Albis Arrieta")),
                                html.P("+ 8 years of project management, strategy, and procurement experience in "
                                       "telecommunications and public sectors. In my previous work as Project Manager "
                                       "at the Ministry of Information and Communications Technologies, I worked at "
                                       "the definition and implementation of Colombia’s Technology Policy Plan to "
                                       "foster Internet's access and adoption to bridge digital gap.")
                            ]
                        ),
                    ], color="primary", inverse=True
                )),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="../../assets/oscar.png", top=True),
                        dbc.CardBody(
                            [
                                html.H4(html.Strong("Oscar Darío Malagón Murcia")),
                                html.P("Estudiante de Maestría en Ingeniería de Información en la Universidad de los Andes"),
                                html.P("Ingeniero de sistemas de la Pontificia Universidad Javeriana"),
                                html.P("Desarrollador de Software en PSL (Ahora parte de Perficient)"),
                                html.Br(), html.Br(), html.Br()
                            ]
                        ),
                    ], color="secondary"
                )),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="../../assets/dario.jpeg", top=True),
                        dbc.CardBody(
                            [
                                html.H4(html.Strong("Dario Alejandro Segura Torres")),
                                html.P("Ingeniero Electrónico de la universidad Santo Tomás, Magister en Ciencias de "
                                       "la Información y las Comunicaciones de la Universidad Distrital Francisco "
                                       "José de Caldas. Actualmente Docente Investigador Facultad de Ingeniería "
                                       "Electrónica de la Universidad Santo Tomás"),
                                html.Br(), html.Br()
                            ]
                        ),
                    ], color="primary", inverse=True
                )),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="../../assets/manuel.jpeg", top=True),
                        dbc.CardBody(
                            [
                                html.H4(html.Strong("Manuel Alfonso Saavedra Quintero")),
                                html.P("Profesional en estadística y tecnólogo en desarrollo de software. Experiencia "
                                       "en análisis multivariado, series de tiempo, métodos de clasificación, "
                                       "generación de modelos predictivos, minería de datos, machine learning y "
                                       "desarrollo de software; dirección de equipos de trabajo interdisciplinarios "
                                       "en business analytics."),
                                html.Br()
                            ]
                        ),
                    ], color="secondary"
                )),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="../../assets/carlos.jpeg", top=True),
                        dbc.CardBody(
                            [
                                html.H4(html.Strong("Carlos Uriel Romero Cepeda")),
                                html.P("Estadístico egresado de la Facultad de Ciencias de la Universidad Nacional de "
                                       "Colombia. Maestría en Economía de la Universidad Externado de Colombia. DS4A. "
                                       "Director de Annalect."),
                                html.Br(), html.Br(), html.Br(), html.Br(), html.Br()
                            ]
                        ),
                    ], color="primary", inverse=True
                ))
        ], justify="center")
    ]
)
