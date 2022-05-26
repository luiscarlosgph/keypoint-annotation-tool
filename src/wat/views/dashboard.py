#!/usr/bin/python
#
# @brief  View classes for displaying information on the website.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2020.

from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import cv2
import os

# My imports
import wat.common
import wat.views.base
import wat.controllers.dataloader


class DashboardView(wat.views.base.BaseView):
    """@class that displays the dashboard content (i.e. no navbar)."""
    def __init__(self, args, show_instructions=False):
        self.show_instructions = show_instructions

        # Create controllers here
        self.data_loader = wat.controllers.dataloader.DataLoader()
        self.annotator = wat.controllers.annotator.TooltipAnnotator()

    def _generate_instructions_toast(self):
        instructions_toast = dbc.Toast([
                html.P('The label for the background is zero.', className='mb-0'),
                html.P('Each tooltip will be annotated with a number corresponding to the clicking order.', 
                    className='mb-0'),
        ],
        id='positioned-toast',
        header='Instructions of use',
        is_open=self.show_instructions,
        dismissable=True,
        icon='info',
        # top: 66 positions the toast below the navbar
        style={'position': 'fixed', 'top': 66, 'right': 15, 'max-width': 640},
        )
        return instructions_toast

    def _generate_display_toast(self, max_display_width=960, display_margin=10):
        # Get the path of the next image to annotate
        path = self.data_loader.next()
        
        # If there are images in the input folder
        if path:
            # Read image
            img = cv2.imread(path)

            # Resize image to the standard width
            resized = None
            scale_factor = 1.0
            if img.shape[1] > max_display_width:
                scale_factor = max_display_width / img.shape[1] 
                width = int(round(img.shape[1] * scale_factor))
                height = int(round(img.shape[0] * scale_factor))
                resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)
            else:
                resized = img

            # Tell the annotator the info about the image we are currently annotating
            self.annotator.new_image(path, scale_factor)

            # Plot image
            rgb = resized[...,::-1].copy()
            fig = px.imshow(rgb)

            # Configure axes
            fig.update_xaxes(
                visible=False,
                range=[0, resized.shape[1]],
                fixedrange=True, # This removes the zooming option
            )
            fig.update_yaxes(
                visible=False,
                range=[resized.shape[0], 0],
                # the scaleanchor attribute ensures that the aspect ratio stays constant
                scaleanchor='x'
            )
            
            # Configure figure layout
            fig.update_layout(
                width=resized.shape[1],
                height=resized.shape[0],
                margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            )
            fig.update_traces(hovertemplate=None, hoverinfo='none')
            config = {
                'displayModeBar': False,
                'doubleClick': 'reset',
                #'editable': True,
            }

            # Create canvas
            graph = dcc.Graph(id='canvas', figure=fig, config=config)
            header = os.path.basename(path)
        else:
            # If there are no images in the input folder
            graph = html.P('There are no images in the input folder.',
                style={'padding': '15px', 'margin-bottom': '0px'})
            header = 'Good job!'
        
        # Create toast
        toast = dbc.Toast([
            html.Div([
                #dcc.Graph(id='canvas', figure=fig, config=config),
                graph,
            ], id='canvas-div'),
        ], 
        header=header, 
        style={'maxWidth': str(max_display_width + display_margin) + 'px'},
        body_style={'padding': '0px 0px 0px 0px', 'margin': '0px 0px 0px 0px'},
        )
        return toast

    def _generate_click_toast(self):
        toast = dbc.Toast([
            dbc.ListGroup(id='tooltip-list', children=[], 
                style={'border': '0px', 'border-radius': '0%'}, className='mb-0'),
        ], 
        header='Tooltips', 
        style={'width': '200px', 'maxWidth': '200px'},
        body_style={'padding': '0px 0px 0px 0px', 'margin': '0px 0px 0px 0px'},
        )
        return toast

    def generate_html(self):
        # Produce all the different toasts we want
        display_toast = self._generate_display_toast()
        instructions_toast = self._generate_instructions_toast()
        click_toast = self._generate_click_toast()

        # Produce container (everything under navbar)
        content = html.Div(className='mt-3', children=[
            dbc.Row([
                dbc.Col(display_toast, style={'padding-right': '0px'}),
                dbc.Col(click_toast, style={'padding-right': '0px'}),
            ], className='mb-3'),
            self._generate_instructions_toast(),
        ], style={'width': '100%'})
        return content


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
