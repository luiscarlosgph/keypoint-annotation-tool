#!/usr/bin/python
#
# @brief  View classes for displaying information on the website.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2020.

import dash_bootstrap_components as dbc
import dash_html_components as html

# My imports
import wat.views.base

class NavbarView(wat.views.base.BaseView):
    """@class that displays just the top navigation bar of the website."""
    def generate_html(self):
        nav = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of 
                # logo / brand
                dbc.Row([
                    dbc.Col(dbc.NavbarBrand('Tooltip annotation', className='ml-0')),
                ], className='ml-1', align='center', no_gutters=True),
                href='/',
            ),
            dbc.Nav([
                dbc.NavItem([], className='ml-5'),
                dbc.Button('Submit', id='submit-button', color='success'),
                dbc.NavItem([], className='ml-5'),
                dbc.NavItem([], className='ml-5'),
                dbc.Button('Undo', id='undo-button', color='secondary'),
                dbc.NavItem([], className='ml-5'),
                dbc.NavItem([], className='ml-5'),
                dbc.Button('Missing tip', id='missing-tip-button', color='info'),
            ]),
            dbc.Row([
                html.A(dbc.Button('Instructions', color='primary'), href='/instructions', className='mr-0'),
            ], className='ml-auto mr-1'),
        ],
        color='dark',
        dark=True,
        )
        return nav


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
