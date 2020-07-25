from dash.dependencies import Input, Output

# LOAD THE DIFFERENT FILES
from apps.About import About_panel
from apps.Analisys import Analisys_panel
from apps.Prediction import Prediction_panel
from apps.RawData import Raw_data_panel

routes = {'/RawData': Raw_data_panel.main,
          '/Analisys': Analisys_panel.main,
          '/Predictions': Prediction_panel.main,
          '/About': About_panel.main}


def register_callback(app):
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname in routes:
            return routes[pathname]
        else:
            return Raw_data_panel.main
