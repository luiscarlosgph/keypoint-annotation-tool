# Description
This repository contains a Dash application for annotating keypoints in images.

# Installation
```
$ python setup.py install --user
```

# Execution
```
$ python -m wat.run --data-dir ~/data --port 1234
```
The ```--data-dir``` parameter should contain two folders: ```input``` and ```output```.
The ```input``` folder should contain the images (```*.jpg``` or ```*.png```) to be annotated.
The ```output``` folder should be empty. The annotations will be stored there.

# Deployment
```http://localhost:1234```

# Demo image
![alt text](https://github.com/luiscarlosgph/keypoint-annotation-tool/blob/main/demo/demo.jpg?raw=true)

# License
See LICENSE file.
