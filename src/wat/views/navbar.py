#!/usr/bin/python
#
# @brief  View classes for displaying information on the website.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2020.

import dash_bootstrap_components as dbc
from dash import html

# My imports
import wat.views.base

class NavbarView(wat.views.base.BaseView):
    """@class that displays just the top navigation bar of the website."""
    def generate_html(self):
        # Get the number of images in the input folder (to be annotated)
        im_rem = str(wat.controllers.dataloader.DataLoader().remaining())

        nav = dbc.Navbar(
            html.Div([
                dbc.Row([
                    dbc.Col(html.A(
                        dbc.NavbarBrand('Keypoint annotator'),
                        href='/',
                    ), width=2, style={'padding-top': '3px', 'padding-left': '25px'}),
                    dbc.Col([
                        dbc.Button('Submit', id='submit-button', color='success', style={'margin-right': '20px'}),
                        dbc.Button('Undo', id='undo-button', color='secondary', style={'margin-right': '20px'}),
                        dbc.Button('Missing tip', id='missing-tip-button', color='info'),
                    ], width=2),
                    dbc.Col(html.P('Remaining: ' + im_rem), width=1),
                    dbc.Col(html.A(dbc.Button('Instructions', color='primary'), href='/instructions'), width={'size': 1, 'offset': 6}),
                ]),
            ], style={'width': '100%'}), 
            color='dark', 
            dark=True,
        )
        return nav


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
