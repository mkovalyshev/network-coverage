from PIL import Image
from urllib import response
from dataclasses import dataclass
import numpy as np
import requests
import re


@dataclass
class Point:
    x: float
    y: float


def rgba_to_mono(image: object, threshold: int=64) -> object:
    """
    transforms RGBA image into mono
    """

    threshold = 64

    image_mono_data = list()

    for row in np.array(image):
        row_mono = list()
        for pixel in row:
            if pixel[-1] <= threshold:
                row_mono.append(np.array([0, 0, 0, 0]))
            else:
                row_mono.append(np.array([255, 255, 255, 255]))
        
        image_mono_data.append(row_mono)

    image_mono_data = np.array(image_mono_data)

    image_mono = Image.fromarray(image_mono_data.astype(np.uint8))

    return image_mono


def coordinates_from_wiki(link: str) -> tuple[float]:
    """
    returns lat/lon coordinates as tuple from Wikipedia city article (tested only on ru.wikipedia.org)
    """

    regex = re.compile(r'\"lat\":(\d+.\d*).*\"lon\":(\d+.\d*)}')

    response = requests.get(link)
    result = regex.search(response.text.replace("\n", ""))

    x_str = result.group(1)
    y_str = result.group(2)

    if "." not in x_str:
        x_str = x_str + ".0"
    
    if "." not in y_str:
        y_str = y_str + ".0"

    return Point(float(x_str), float(y_str))


def name_from_wiki(link: str) -> str:
    """
    returns city name from Wikipedia
    """

    regex = re.compile(r"wgTitle\":\"(.*?)")

    response = requests.get(link)
    result = regex.search(response.text.replace("\n", ""))

    return result.group(1)
    