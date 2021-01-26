#!/usr/bin/python
#
# @brief  View classes for displaying information on the website.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2020.

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import cv2

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
        instructions_toast = dbc.Toast(
            [
                html.P('Press <Space> to exchange the right-left order of the tooltips.', className='mb-0'),
                html.P('Press <Enter> to submit the current annotation and get a new image.', className='mb-0'),
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
        config = {
            'displayModeBar': False,
            'doubleClick': 'reset',
        }
        
        # Create toast
        toast = dbc.Toast(
        [
            html.Div(id='hidden-div', style={'display': 'none'}), # Used for the callback
            html.Div([
                dcc.Graph(id='canvas', figure=fig, config=config),
            ], id='canvas-div'),
        ], 
        header=path, 
        style={'maxWidth': str(max_display_width + display_margin) + 'px'},
        body_style={'padding': '0px 0px 0px 0px', 'margin': '0px 0px 0px 0px'},
        )
        return toast

    def generate_html(self):
        # Produce all the different toasts we want
        display_toast = self._generate_display_toast()
        instructions_toast = self._generate_instructions_toast()

        # Produce container (everything under navbar)
        content = dbc.Container(fluid=True, className='mt-3', children=[
            dbc.Row([
                dbc.Col(display_toast, width='auto', style={'padding-right': '0px'}),
            ], className='mb-3'),
            self._generate_instructions_toast(),
        ])
        return content


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
