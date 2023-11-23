import numpy as np
from PIL import Image


def load_image(path):
    img = Image.open(path)
    return np.array(img)