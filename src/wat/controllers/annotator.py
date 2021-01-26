#!/usr/bin/python
#
# @brief  This module and class represent a singleton controller that is
#         intended to store the temporary information about the current
#         annotation and save it to disk.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2021.

import ntpath


class BaseAnnotator(object):
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class TooltipAnnotator(BaseAnnotator):
    instance = None
    """
    @class that annotates surgical instrument tooltips. It only works for 
           scenes that contain a maximum of two tooltips. It is a Singleton.
    """
    class __TooltipAnnotator: 
        def __init__(self, data_dir, input_dir='input', output_dir='output', 
                max_tooltips=2, gt_suffix='_seg'):
            self.data_dir = data_dir
            self.input_dir = os.path.join(self.data_dir, input_dir)
            self.output_dir = os.path.join(self.data_dir, output_dir)
            self.max_tooltips = max_tooltips
            self.gt_suffix = gt_suffix

            # Image-specific attributes
            self.path = None          # Path to the last file being annotated
            self.scale_factor = None  # Scale factor of the last file being annotated
            self.clicks = []          # [[x_0, y_0], [x_1, y_1], ... ]
            self.last_click_id = -1

        def new_image(self, path, scale_factor):
            self.path = path 
            self.scale_factor = scale_factor
            self.clicks = []
            self.last_click_id = -1

        def add_click(self, click_id, x, y):
            if click_id != self.last_click_id and len(self.clicks) < self.max_tooltips:
                self.last_click_id = click_id
                x_original = int(round(x / self.scale_factor))
                y_original = int(round(y / self.scale_factor))
                self.clicks.append({'x': x_original, 'y': y_original})

        def save(self, output_folder='output'):
            # Move file to the output folder
            im_fname = ntpath.basename(self.path)
            src_path = self.path
            dst_path = os.path.join(self.output_dir, im_fname)
            wat.common.mv(src_path, dst_path) 
            
            # Save JSON with the annotation
            json_fname = wat.common.fname_no_ext(im_fname) + '.json'
            dst_path = os.path.join(self.output_dir, json_fname)
            json_annotation = self._create_json_annotation()
            with open(dst_path, 'w') as f: 
                json.dump(json_annotation, f)
            
            # Save binary mask with the tooltip annotation
            im_annot_fname = wat.common.fname_no_ext(im_fname) + self.gt_suffix + '.png'
            dst_path = os.path.join(self.output_dir, im_annot_fname)
            im_annot = self._create_image_annotation()
            cv2.imwrite(dst_path, im_annot)

        def switch_left_right(self):
            """@brief If we are labelling a bimanual system, we can change the order of
                      the tooltips so that the left instrument goes first in the array
                      of clicks.
            """
            if len(self.clicks) == 1:
                self.clicks = [None, self.clicks[0]]
            elif len(self.clicks) == 2:
                self.clicks = [self.clicks[1], self.clicks[0]]

        def _create_json_annotation(self):
            json_annotation = {'tooltips': self.clicks}
            return json_annotation

        def _create_image_annotation(self):
            # Get image dimensions
            im = cv2.imread(self.path)
            width = im.shape[1]
            height = im.shape[0]

            # Create black image
            im_annot = np.zeros([height, width], dtype=np.uint8)

            # Add tooltip annotations
            counter = 0
            for tooltip in self.clicks:
                counter += 1
                x = tooltip['x']
                y = tooltip['y']
                if x is not None and y is not None:
                    im_annot[y, x] = counter
            
            return im_annot

    # Singleton implementation for the Controller class 
    def __init__(self):
        if TooltipAnnotator.instance is None:
            TooltipAnnotator.instance = TooltipAnnotator.__TooltipAnnotator()


if __name__ == '__main__':
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
