#!/usr/bin/python
#
# @brief  This module and class represent a singleton controller.
# @author Luis Carlos Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   20 Jan 2021.

import os
import random

# My imports
import wat.common

class DataLoader(object):
    """
    @class that keeps the database updated. It is a Singleton.
    """
    class __DataLoader: 
        def __init__(self, data_dir, log_file='log.txt'):
            assert(wat.common.dir_exists(data_dir))
            self.data_dir = data_dir
            self.input_dir = os.path.join(data_dir, 'input')
            self.output_dir = os.path.join(data_dir, 'output')
            self.log_file = os.path.join(data_dir, log_file)

            # Create an output folder if it does not exist
            if not wat.common.dir_exists(self.output_dir):
                wat.common.mkdir(self.output_dir)

            # Create log file if it does not exist
            if not wat.common.file_exists(self.log_file):
                wat.common.touch(self.log_file)

        def next(self):
            """@returns an absolute path to the next image to annotate."""
            ldir = wat.common.listdir(self.input_dir, ext=['.png', '.jpg'], onlyfiles=True)
            if ldir:
                fname = random.choice(ldir)  
                abs_path = os.path.abspath(os.path.join(self.input_dir, fname))
            else:
                abs_path = None
            return abs_path

        def remaining(self):
            """@returns the number of images to be annotated."""
            return len(wat.common.listdir(self.input_dir, ext=['.png', '.jpg'], onlyfiles=True))
        
        """
        def annotate(self, fname, data_dic):
            # Move file to output folder
            src_path = os.path.abspath(os.path.join(self.input_dir, fname))
            dst_path = os.path.abspath(os.path.join(self.output_dir, fname))
            wat.common.mv(src_path, dst_path)

            # Save JSON annotation to output folder
            json_fname = wat.common.fname_no_ext(fname) + '.json'
            json_path = os.path.abspath(os.path.join(self.output_dir, json_fname))
            wat.common.save_json(data_dic, json_path)
        """
        
    # Singleton implementation for the Controller class 
    instance = None
    def __init__(self, data_dir=None):
        if DataLoader.instance is None:
            DataLoader.instance = DataLoader.__DataLoader(data_dir)
        else:
            if data_dir is None or data_dir == DataLoader.instance.data_dir:
                pass # Same database, nothing to do
            else:
                raise RuntimeError('[ERROR] You cannot change the data directory during execution.')

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
    

if __name__ == "__main__":
    raise RuntimeError('[ERROR] This module cannot be run like a script.')
