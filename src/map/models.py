from dataclasses import dataclass
from shapely.geometry import Polygon
import numpy as np
import math
from PIL import Image


@dataclass
class BoundingBox:
    x0: float
    y0: float
    x1: float
    y1: float


class Tile:
    """
    class for web map tile methods
    """

    def __init__(self, x: int, y: int, zoom: int) -> object:
        self.x = x
        self.y = y
        self.zoom = zoom

    @staticmethod
    def from_coordinates(lat: float, lon: float, zoom: int) -> object:
        """
        returns instance of Tile class from WGS-84 coordinates for defined zoom
        """

        x_tile = int((lon + 180) / 360 * (2**zoom))

        y_tile = int(
            (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * (2**zoom)
        )

        return Tile(x_tile, y_tile, zoom)

    def get_bbox(self) -> BoundingBox:
        """
        returns WGS-84 BoundingBox for Tile
        credit: https://www.flother.is/til/map-tile-bounding-box-python/
        """

        def get_tile_lon(x, zoom) -> int:
            return x / (2**zoom) * 360 - 180

        def get_tile_lat(y, zoom) -> int:
            return math.degrees(
                math.atan(math.sinh(math.pi - (2 * math.pi * y) / (2**zoom)))
            )

        lon0 = get_tile_lon(self.x, self.zoom)
        lon1 = get_tile_lon(self.x + 1, self.zoom)
        lat0 = get_tile_lat(self.y + 1, self.zoom)
        lat1 = get_tile_lat(self.y, self.zoom)

        return BoundingBox(lon0, lat0, lon1, lat1)

    def get_coverage_polygons(
        self, image: Image.Image, threshold: int = 254
    ) -> tuple[tuple]:
        """
        returns tuple of (polygon, coverage) tuples from defined image
        """

        bbox = self.get_bbox()

        def get_coordinate_pairs(start: float, stop: float) -> list[tuple]:
            length = stop - start
            range_ = np.arange(start, stop + length / 256, length / 256)
            pairs = list(
                map(
                    lambda x: tuple([x, range_[list(range_).index(x) + 1]]),
                    range_[:256],
                )
            )

            return pairs

        x_pairs = get_coordinate_pairs(bbox.x0, bbox.x1)
        y_pairs = get_coordinate_pairs(bbox.y1, bbox.y0)

        polygons = []

        for y in y_pairs:
            for x in x_pairs:
                polygons.append(
                    Polygon([[x[0], y[1]], [x[1], y[1]], [x[1], y[0]], [x[0], y[0]]])
                )

        image_mono = image.convert("L").point(
            lambda x: 255 if x > threshold else 0, mode="1"
        )

        pixels = []

        for row in np.array(image_mono.convert("L")):
            for el in row:
                pixels.append(el)

        coverage_polygons = zip(pixels, polygons)

        return coverage_polygons
