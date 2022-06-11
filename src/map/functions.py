import math


def get_tile_from_coordinates(lat: float, lon: float, zoom: int) -> tuple[int]:
    """
    returns tuple of web map tile x/y/zoom for defined coordinates and zoom
    """

    x_tile = int((lon + 180) / 360 * (2**zoom))

    y_tile = int(
        (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * (2**zoom)
    )

    return x_tile, y_tile, zoom
