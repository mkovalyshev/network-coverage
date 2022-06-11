import requests
import PIL
import io
from ..models import Operator
from .enum import NetworkType


class Megafon(Operator):
    """
    class for handling Megafon data
    """

    def __init__(
        self,
        schema: str = "https",
        host: str = "coverage-map.megafon.ru",
    ) -> object:
        super().__init__(schema=schema, host=host)

    def get_tiles(
        self, x: int, y: int, zoom: int, network: NetworkType
    ) -> PIL.PngImagePlugin.PngImageFile:
        """
        returns Megafon coverage tile for defined x, y, zoom map tile
        """

        response = requests.get(
            f"{self.schema}://{self.host}/{zoom}/{x}/{y}.png?layers={network.value}"
        )

        image = PIL.Image.open(io.BytesIO(response.content))

        return image
