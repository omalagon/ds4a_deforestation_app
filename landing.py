#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization. 
#######################################################




import dash
import dash_bootstrap_components as dbc 


landing = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = landing.server

#We need this for function callbacks not present in the app.layout
landing.config.suppress_callback_exceptions = True