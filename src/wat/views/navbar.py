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
                dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand('Title here', className='ml-2')),
                ],
                align='center',
                no_gutters=True,
                ),
                href='/',
            ),
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink('Dashboard', active=True, href='/')),
                dbc.NavItem(dbc.NavLink('Page 1', active=True,
                    href='/page1')),
                dbc.NavItem(dbc.NavLink('Page 2', active=True,
                    href='/page2')),
                dbc.DropdownMenu(label='Dropdown', children=[
                    dbc.DropdownMenuItem('Option 1', href='/whatever/url'),
                    dbc.DropdownMenuItem('Option 2', href='/whatever/url'),
                ], nav=True),
            ],
            ),
            dbc.Row(
                [
                html.A(dbc.Button('Button 1', color='success'), href='/whatever1', className='mr-2'),
                html.A(dbc.Button('Button 2', color='danger'), href='/whatever2', className='mr-2'),
                html.A(dbc.Button('Button 3', color='primary'), href='/whatever3'),
                ],
                className='ml-auto mr-2',
            ),
        ],
        color='dark',
        dark=True,
        )
        return nav


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
