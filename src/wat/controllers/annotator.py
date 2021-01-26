#!/usr/bin/python
#
# @brief  This module and class represent a singleton controller that is
#         intended to store the temporary information about the current
#         annotation and save it to disk.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2021.


class BaseAnnotator(object):
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class TooltipAnnotator(BaseAnnotator):
    instance = None
    """
    @class that annotates surgical instrument tooltips. It is a Singleton.
    """
    class __TooltipAnnotator: 
        def __init__(self, data_dir):
            self.data_dir = data_dir

            # Image-specific attributes
            self.path = None         # Path to the last file being annotated
            self.scale_factor = None # Scale factor of the last file being annotated
            self.clicks = [] # [[x_0, y_0], [x_1, y_1], ... ]
            self.last_click_id = -1

        def new_image(self, path, scale_factor):
            self.path = path 
            self.scale_factor = scale_factor
            self.clicks = []
            self.last_click_id = -1

        def add_click(self, click_id, x, y):
            if click_id != self.last_click_id:
                self.last_click_id = click_id
                x_old = int(round(x / self.scale_factor))
                y_old = int(round(y / self.scale_factor))
                self.clicks.append([x_old, y_old])

        def save(self, output_folder='output'):
            # Move file to the output folder
            output_dir = os.path.join(self.data_dir, output_folder)
            #fname = 

            # Save JSON with the annotation

            # Save binary mask with the tooltip annotation


    # Singleton implementation for the Controller class 
    def __init__(self):
        if TooltipAnnotator.instance is None:
            TooltipAnnotator.instance = TooltipAnnotator.__TooltipAnnotator()


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
