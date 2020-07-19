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
from apps.RawData.Raw_data_panel_callback import register_callback as register_raw_data_callback

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
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

if __name__ == '__main__':
    app.run_server(debug=True)