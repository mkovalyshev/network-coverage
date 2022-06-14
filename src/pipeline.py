from src.common.functions import get_logger
from src.map.functions import coordinates_from_wiki, name_from_wiki
from src.map.models import BoundingBox, Tile
from src.operator.models import Operator
from src.operator.beeline.models import Beeline
from src.operator.beeline.enum import NetworkType as NetworkTypeBeeline
from src.operator.megafon.models import Megafon
from src.operator.megafon.enum import NetworkType as NetworkTypeMegafon
from src.operator.mts.models import Mts
from src.operator.mts.enum import NetworkType as NetworkTypeMts
from typing import Union
from shapely.geometry import Point
import datetime


def lookup_wiki(city: str) -> str:
    pass


def check_network_coverage(
    city: str, operator: Operator, lookup: bool = False, zoom: int = 8
) -> dict:

    # logger = get_logger(f"network-coverage {operator.name}")
    # logger.info("start")

    print(
        f"[INFO] [{datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')}] [network-coverage] {operator.name}"
    )

    if lookup:
        pass
    else:
        coordinates = coordinates_from_wiki(city)
        city_name = name_from_wiki(city)

    response = {"operator": operator.name, "city": city_name}

    tile = Tile.from_coordinates(coordinates.x, coordinates.y, zoom)

    if operator.name == "Beeline":
        network = NetworkTypeBeeline
    elif operator.name == "Megafon":
        network = NetworkTypeMegafon
    elif operator.name == "MTS":
        network = NetworkTypeMts
    else:
        raise KeyError(f"invalid operator {operator}")

    for network_type in [network.TYPE_2G, network.TYPE_3G, network.TYPE_4G]:
        image = operator.get_tiles(tile.x, tile.y, tile.zoom, network_type)

        if image is None:
            # logger.info(f"no content for {network_type}")
            print(
                f"[INFO] [{datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')}] [network-coverage] no content for {network_type}"
            )
            continue

        coverage_vector = list(tile.get_coverage_polygons(image))
        city_point = Point(coordinates.y, coordinates.x)

        city_polygon = list(
            filter(lambda x: x[1].contains(city_point), coverage_vector)
        )

        if len(city_polygon) == 0:
            # logger.info("city polygon not found")
            print(
                f"[INFO] [{datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')}] [network-coverage] city polygon not found"
            )
        else:
            response[network_type.name] = city_polygon[0][0] == 255

    return response
