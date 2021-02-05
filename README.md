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
$ python3 -m pip install dash dash_bootstrap_components

# Install this repo
$ cd ~
$ git clone git@github.com:luiscarlosgph/keypoint-annotation-tool.git
$ cd keypoint-annotation-tool
$ python3 setup.py install --user
```

# Run
```
$ python3 -m wat.run --data-dir ~/keypoint-annotation-tool/data --port 1234 --maxtips 4
```
The ```--data-dir``` parameter should contain two folders: ```input``` and ```output```.
The ```input``` folder should contain the images (```*.jpg``` or ```*.png```) to be annotated.
The ```output``` folder should be empty. The annotations will be stored there.
The ```--maxtips``` parameter sets the maximum number of tooltips that can be annotated per image.
By default this is set to four as there are typically two instruments in the scene with two tooltips 
each (one per clasper).

# Deployment
```http://localhost:1234```

# Demo image
![alt text](https://github.com/luiscarlosgph/keypoint-annotation-tool/blob/main/demo/demo.jpg?raw=true)

# License
See [LICENSE](https://github.com/luiscarlosgph/keypoint-annotation-tool/blob/main/LICENSE) file.
