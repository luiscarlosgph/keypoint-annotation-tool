#!/usr/bin/python
# 
# Runs a web server. 
#
# @author: Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date  : 20 Jan 2021.

import argparse
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash.dependencies
import os
import flask
import json
import plotly.express as px
import cv2
import numpy as np
import plotly.graph_objects as go

# My imports
import wat.page
import wat.controllers.dataloader
import wat.controllers.annotator

# Global variables
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
#app.config['suppress_callback_exceptions'] = True
args = None


## Callbacks ##


@app.callback(
    dash.dependencies.Output('page-content', 'children'), 
    dash.dependencies.Input('submit-button', 'n_clicks'),
    dash.dependencies.Input('url', 'pathname'),
)
def display_page(n_clicks, pathname):
    global args
    
    # Click on the submit button
    if n_clicks is not None:
        wat.controllers.annotator.TooltipAnnotator().save()
        return wat.page.DashboardPage(args).generate_html()
    
    # HTTP GET of any URL
    if pathname is not None:
        if pathname == '/instructions':
            return wat.page.DashboardPage(args, show_instructions=True).generate_html()
        else:
            return wat.page.DashboardPage(args).generate_html()


@app.callback(
    dash.dependencies.Output('tooltip-list', 'children'), 
    dash.dependencies.Output('canvas', 'figure'), 
    dash.dependencies.Input('canvas-div', 'n_clicks'),
    dash.dependencies.Input('canvas', 'hoverData'),
    dash.dependencies.Input('undo-button', 'n_clicks'),
    dash.dependencies.Input('missing-tip-button', 'n_clicks'),
    dash.dependencies.State('canvas', 'figure'),
)
def click_event_handler(canvas_n_clicks, hoverData, undo_n_clicks, missing_tip_n_clicks, fig):
    # Click on canvas
    if canvas_n_clicks is not None and canvas_n_clicks != click_event_handler.last_canvas_n_clicks:
        click_event_handler.last_canvas_n_clicks = canvas_n_clicks

        # Submit clicks to the controller
        x = hoverData['points'][0]['x']
        y = hoverData['points'][0]['y']
        wat.controllers.annotator.TooltipAnnotator().add_click(canvas_n_clicks, x, y)
    
    # Click on the undo button
    if undo_n_clicks is not None and undo_n_clicks != click_event_handler.last_undo_n_clicks:
        click_event_handler.last_undo_n_clicks = undo_n_clicks
        if wat.controllers.annotator.TooltipAnnotator().clicks:
            wat.controllers.annotator.TooltipAnnotator().clicks.pop()

    # Click on the missing tip button
    if missing_tip_n_clicks is not None and missing_tip_n_clicks != click_event_handler.last_missing_tip_n_clicks:
        click_event_handler.last_missing_tip_n_clicks = missing_tip_n_clicks
        wat.controllers.annotator.TooltipAnnotator().add_click('missing-tip', None, None)

    # Update the view of the list of clicked points
    tooltip_view = []
    tips = wat.controllers.annotator.TooltipAnnotator().clicks
    tip_style = {'margin-bottom': '0px'}
    for tip in tips:
        tip_html = dbc.ListGroupItem('x = ' + str(tip['x']) + ', y = ' + str(tip['y']), style=tip_style)
        tooltip_view.append(tip_html)

    # Update the view of the figure 
    #new_fig = dash.no_update
    fig['data'] = [fig['data'][0]] # Delete all the traces except the image
    clicks = wat.controllers.annotator.TooltipAnnotator().clicks
    for idx, click in enumerate(clicks):
        fig['data'].append(go.Scatter(
            x=[click['x']],
            y=[click['y']],
            showlegend=False,
            mode= 'markers',
            name='Tooltip ' + str(idx + 1),
        ))

    return tooltip_view, fig

click_event_handler.last_canvas_n_clicks = None
click_event_handler.last_undo_n_clicks = None
click_event_handler.last_missing_tip_n_clicks = None


## Functions ##


def parse_cmdline_params():
    """
    @brief Parse command line parameters to get input and output file names.
    @param[in] argv Array of command line arguments.  
    @return input and output file names if they were specified.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', required=True, help='Path to the data directory.')
    parser.add_argument('--port', required=False, default=1234, help='Listening port.')
    parser.add_argument('--maxtips', required=False, default=4, 
        help='Maximum number of tooltips to annotate.')
    args = parser.parse_args()
    return args
args = parse_cmdline_params()


def valid_cmdline_params(args):
    if not os.path.isdir(args.data_dir):
        raise ValueError('[ERROR] Data directory does not exist.')
    args.port = int(args.port)
    args.maxtips = int(args.maxtips)


def main():
    # Reading command line parameters
    valid_cmdline_params(args) 

    # Create web app basic layout
    app.title = 'Tooltip annotation'
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', children=[
            html.Div(id='submit-button-hidden-div', style={'display': 'none'}, children=[
                dbc.Button('Submit', id='submit-button', color='success'),
            ]), # Used for the callback, otherwise the page would not load
                # as a button has to be created for the callback to work
        ]),
    ])

    # Launch Singleton controller engines in the background
    wat.controllers.dataloader.DataLoader(args.data_dir)
    wat.controllers.annotator.TooltipAnnotator(args.data_dir, maxtips=args.maxtips)
    
    # Launch web server
    app.run_server(debug=False, use_reloader=False, host='0.0.0.0', port=args.port)
    
if __name__ == "__main__":
    main()
