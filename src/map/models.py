from dataclasses import dataclass
from webbrowser import get
from shapely import Polygon
import numpy as np
import math
import PIL


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
        self, image: PIL.PngImagePlugin.PngImageFile
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

        x_pairs = get_coordinate_pairs(bbox[1][0], bbox[0][0])
        y_pairs = get_coordinate_pairs(bbox[0][1], bbox[1][1])

        polygon_list = []

        for y in y_pairs:
            for x in x_pairs:
                polygon_list.append(
                    Polygon([[x[0], y[1]], [x[1], y[1]], [x[1], y[0]], [x[0], y[0]]])
                )

        return polygon_list
