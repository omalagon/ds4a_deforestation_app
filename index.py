from dash.dependencies import Input, Output

# LOAD THE DIFFERENT FILES
from apps.About import About_panel
from apps.Analisys import Analisys_panel
from apps.Prediction import Prediction_panel
from apps.RawData import Raw_data_panel


def register_callback(app):
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        print('algo');
        if pathname == '/RawData':
            return Raw_data_panel.main
        elif pathname == '/Analisys':
            return Analisys_panel.main
        elif pathname == '/Predictions':
            return Prediction_panel.main
        elif pathname == '/About':
            return About_panel.main
        else:
            return Raw_data_panel.main
