#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

#Dash Bootstrap Components
import dash_bootstrap_components as dbc

#Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

#Recall app-in my case landing
from landing import landing



###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
from lib import menu
from apps.About import About_panel
from apps.Analisys import Analisys_panel
from apps.Prediction import Prediction_panel
from apps.RawData import Raw_data_panel

#PLACE THE COMPONENTS IN THE LAYOUT
landing.layout =html.Div(
    [ 
        dcc.Location(id='url', refresh=False),
        menu.menu,
        html.Div(id='page-content')
    ],
    className="ds4a-app", 
)

###########################################################
#
#           APP CALLBACKS:
#
###########################################################

from apps.RawData import Raw_data_panel_callback

@landing.callback(Output('page-content', 'children'),
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

if __name__ == "__main__":
    landing.run_server(debug=True, port=8080)
