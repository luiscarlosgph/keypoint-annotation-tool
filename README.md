# Description
This repository contains a Python [Dash](https://dash.plotly.com/introduction) application for annotating keypoints in images.

# Install dependencies
* OpenCV
```
# Ubuntu/Debian
$ sudo apt update
$ sudo apt install libopencv-dev python3-opencv

# Other platforms
$ python3 -m pip install opencv-python --user
```

# Install this package
```
# Install pip dependencies
$ python3 -m pip install numpy dash dash_bootstrap_components --user

# Download repo
$ git clone git@github.com:luiscarlosgph/keypoint-annotation-tool.git
$ cd keypoint-annotation-tool

# Install package
$ python3 setup.py install --user
```

# Run
``` 
# You should be already inside the repo, where there is a sample 'data' folder to make this command work
$ python3 -m wat.run --data-dir data --port 1234 --maxtips 4
```
The ```--data-dir``` parameter should contain two folders: ```input``` and ```output```.
The ```input``` folder should contain the images (```*.jpg``` or ```*.png```) to be annotated.
The ```output``` folder should be empty. The annotations will be stored there.
The ```--maxtips``` parameter sets the maximum number of tooltips that can be annotated per image.
By default this is set to four as there are typically two instruments in the scene with two tooltips 
each (one per clasper).

# Deployment
[http://localhost:1234](http://localhost:1234)

# Annotations
When an image is annotated, the image file is moved from the ```input``` to the ```output``` folder.
Each image in the output folder (e.g. ```example.png```) is accompanied by two annotation files:

* ```example_seg.png```: single-channel PNG image. All pixels are set to zero except those that 
                         have been clicked during the annotation process. The first keypoint 
                         clicked is annotated with intensity 1, then second with intensity 2, and so on.

* ```demo.json```:       contains a list of annotations in JSON format, for example, 
                         if four tooltips are clicked, it will contain something like
    ```
    {"tooltips": [{"x": 263, "y": 168}, {"x": 586, "y": 301}, {"x": 581, "y": 210}, {"x": 500, "y": 116}]}
    ```

# Reading the annotations
The script ()[read_annotations.py] is provided as a staring point to process your annotated images.
```
# Assuming you are already inside the repository
$ python3 src/read_annotations.py --data-dir data
```

# Demo image
![alt text](https://github.com/luiscarlosgph/keypoint-annotation-tool/blob/main/demo/demo.jpg?raw=true)

# License
See [LICENSE](https://github.com/luiscarlosgph/keypoint-annotation-tool/blob/main/LICENSE) file.
