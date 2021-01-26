import os
import pathlib
import json
import base64


def encode_image(path):
    with open(path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    encoded_image = 'data:image/png;base64,' + encoded_string
    return encoded_image


def mv(src, dst):
    os.rename(src, dst)


def save_json(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def fname_no_ext(path):
    return os.path.splitext(path)[0]


def listdir(path, ext=None, onlyfiles=False):
    """
    @param[in]  onlyfiles  Boolean.
    @param[in]  ext        If not None, a list of valid extensions.
    """
    listing = os.listdir(path)
    
    # If specified, remove directories from the list
    if onlyfiles:
        listing = [f for f in listing if os.path.isfile(os.path.join(path, f))]
    
    # If specified, remove files that do not have the wanted extensions
    if ext is not None:
        listing = [f for f in listing if os.path.splitext(f)[1] in ext]

    return listing


def mkdir(path):
    """
    @brief Create folder.
    @param[in] path to the new folder.
    @returns nothing.
    """
    if os.path.exists(path):
        raise RuntimeError('[mkdir] Error, this path already exists so a folder cannot be created.')
    os.makedirs(path)


def dir_exists(dpath):
    """
    @param[in] path Path to the folder whose existance you want to check.
    @returns true if folder exists, otherwise returns false.
    """
    return True if os.path.isdir(dpath) else False


def file_exists(fpath):
    """
    @param[in] path Path to the file whose existance you want to check.
    @returns true if the file exists, otherwise returns false.
    """
    return True if os.path.isfile(fpath) else False


def dir_exists(dpath):
    """
    @param[in] path Path to the folder whose existance you want to check.
    @returns true if folder exists, otherwise returns false.
    """
    return True if os.path.isdir(dpath) else False


def touch(path):
    pathlib.Path(path).touch()
