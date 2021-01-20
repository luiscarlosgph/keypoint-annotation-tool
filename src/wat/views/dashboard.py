#!/usr/bin/python
#
# @brief  View classes for displaying information on the website.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2020.

import dash_bootstrap_components as dbc
import dash_html_components as html 

# My imports
import wat.views.base


class DashboardView(wat.views.base.BaseView):
    """@class that displays the dashboard content (i.e. no navbar)."""
    def __init__(self, args):
        pass
        # TODO: Create controller as an attribute here

    def _generate_alert_toast(self, msg='This is an alert toast', show_alert=True):
        alert_toast = dbc.Toast(
            msg,
            id='positioned-toast',
            header='Message notification',
            is_open=show_alert,
            dismissable=True,
            icon='info',
            # top: 66 positions the toast below the navbar
            style={'position': 'fixed', 'top': 66, 'right': 10, 'width': 350},
        )
        return alert_toast

    def _generate_example_toast(self):
        example_toast = dbc.Toast(
        [
            html.P('Sentence 1', className='mb-0'),
            html.P('Sentence 2', className='mb-0'),
        ], header='Window title', style={'maxWidth': '300px'})
        return example_toast

    def generate_html(self):
        # Produce all the different toasts we want
        example_toast = self._generate_example_toast()

        # Produce container (everything under navbar)
        content = dbc.Container(fluid=True, className='mt-3', children=[
            dbc.Row([
                dbc.Col(example_toast, width='auto', style={'padding-right': '0px'}),
                dbc.Col(example_toast, width='auto', style={'padding-right': '0px'}),
                dbc.Col(example_toast, width='auto', style={'padding-right': '0px'}),
                dbc.Col(example_toast, width='auto', style={'padding-right': '0px'}),
                dbc.Col(example_toast, width='auto', style={'padding-right': '0px'}),
            ], className='mb-3'),
            dbc.Row([
                dbc.Col(example_toast, width='auto', style={'padding-right': '0px'}),
                dbc.Col(example_toast, width='auto', style={'padding-right': '0px'}),
            ], className='mb-3'),
            self._generate_alert_toast(),
        ])
        return content 


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
