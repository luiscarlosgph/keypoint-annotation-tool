# Description
This repository contains a template for a basic Python 
web application based on Dash. 
If you want to change the name of the package ```wat``` 
needs to be changed in the setup.py. In addition, the
name of the folder inside ```src``` and also the package 
imports need to be changed.

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

# License
See LICENSE file.
