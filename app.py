#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization. 
#######################################################

import dash
import dash_bootstrap_components as dbc 
import dash_html_components as html
import dash_core_components as dcc
from lib import menu
from index import register_callback as register_index_callback
from apps.RawData.Raw_data_panel import register_callback as register_raw_data_callback
from apps.Analisys.Analisys_panel import register_callback as register_analysis_callback

from apps.Analisys.department.Deforestation_level import register_callback as register_deforestation_level_callback
from apps.Analisys.department.Accumulated_deforestation import register_callback as register_accumulated_deforestation_callback
from apps.Analisys.department.Forest_loss import register_callback as register_forest_loss_callback
from apps.Analisys.municipality.Dynamic_indicator_map import register_callback as register_dynaimic_indicator_map_municipality_callback

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

#We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        menu.menu,
        html.Div(id='page-content')
    ],
    className="ds4a-app",
)
register_index_callback(app)
register_raw_data_callback(app)
register_analysis_callback(app)
# Sliders' callbacks
register_deforestation_level_callback(app)
register_accumulated_deforestation_callback(app)
register_forest_loss_callback(app)
# Dynamic filter callback
register_dynaimic_indicator_map_municipality_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)