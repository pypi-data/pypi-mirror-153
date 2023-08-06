from os import PathLike
import numpy as np
import cv2

from .MCImage import MCImage

__version__ = "CellClass v0.0.4"

import matplotlib.pyplot as plt

        
def imread(p: PathLike) -> np.ndarray:

    im = cv2.imread(p)
    #im = normalize_image(im)
    return (im/im.max()).astype("float32")

def normalize_image(im: np.ndarray):

    im = (im-im.min())/(im.max()-im.min())
    return im


if __name__ == "__main__":
    print(__version__)
    
    tif = imread("/Users/simon.gutwein/pypi/MICCAI/test/image.tif")
    jpg = imread("/Users/simon.gutwein/pypi/MICCAI/test/image.jpg")
    png = imread("/Users/simon.gutwein/pypi/MICCAI/test/image.png")
    
    assert tif.shape == (100,100,3), "Wrong Shape for TIF"
    assert jpg.shape == (100,100,3), "Wrong Shape for jpg"
    assert png.shape == (100,100,3), "Wrong Shape for png"

    assert tif.min() == 0, "Wrong MIN for TIF"
    assert jpg.min() == 0, "Wrong MIN for jpg"
    assert png.min() == 0, "Wrong MIN for png"

    assert tif.max() == 255, "Wrong MAX for TIF"
    assert jpg.max() == 255, "Wrong MAX for jpg"
    assert png.max() == 255, "Wrong MAX for png"