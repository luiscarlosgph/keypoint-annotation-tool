# Description
This repository contains a Dash application for annotating keypoints in images.

# Installation
```
$ cd ~
$ git clone git@github.com:luiscarlosgph/keypoint-annotation-tool.git
$ cd keypoint-annotation-tool
$ python setup.py install --user
```

# Execution
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
See LICENSE file.
