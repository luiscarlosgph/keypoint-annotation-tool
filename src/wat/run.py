#!/usr/bin/python
# 
# Runs a web server. 
#
# @author: Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date  : 20 Jan 2021.

import argparse
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash.dependencies
import os
import flask
import json

# My imports
import wat.page
import wat.controllers.dataloader
import wat.controllers.annotator

# Global variables
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
args = None

# Callbacks 
@app.callback(dash.dependencies.Output('page-content', 'children'), 
    dash.dependencies.Input('url', 'pathname'))
def display_page(pathname):
    global args

    if pathname == '/instructions':
        return wat.page.DashboardPage(args, show_instructions=True).generate_html()
    else:
        return wat.page.DashboardPage(args).generate_html()


@app.callback(dash.dependencies.Output('hidden-div', 'children'), 
    dash.dependencies.Input('canvas-div', 'n_clicks'),
    dash.dependencies.Input('canvas', 'hoverData'))
def click_event_handler(n_clicks, hoverData):
    if n_clicks is not None: 
        x = hoverData['points'][0]['x']
        y = hoverData['points'][0]['y']
        wat.controllers.annotator.TooltipAnnotator().add_click(n_clicks, x, y)


# Read command line parameters
def parse_cmdline_params():
    """
    @brief Parse command line parameters to get input and output file names.
    @param[in] argv Array of command line arguments.  
    @return input and output file names if they were specified.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', required=True, help='Path to the data directory.')
    parser.add_argument('--port', required=False, default=1234, help='Listening port.')
    args = parser.parse_args()
    return args
args = parse_cmdline_params()


def valid_cmdline_params(args):
    if not os.path.isdir(args.data_dir):
        raise ValueError('[ERROR] Data directory does not exist.')
    args.port = int(args.port)



def main():
    # Reading command line parameters
    valid_cmdline_params(args) 

    # Create web app basic layout
    app.title = 'Tooltip annotation'
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ])

    # Launch Singleton controller engines in the background
    wat.controllers.dataloader.DataLoader(args.data_dir)
    wat.controllers.annotator.TooltipAnnotator(args.data_dir)
    
    # Launch web server
    app.run_server(debug=False, use_reloader=False, host='0.0.0.0', port=args.port)
    
if __name__ == "__main__":
    main()
