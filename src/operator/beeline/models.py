import requests
import PIL
from PIL import Image
import io
from ..models import Operator
from .enum import NetworkType


class Beeline(Operator):
    """
    class for handling Beeline data
    """

    def __init__(
        self,
        schema: str = "https",
        host: str = "static.beeline.ru",
        method: str = "upload/tiles",
    ) -> object:
        super().__init__(schema=schema, host=host)
        self.method = method

    def get_tiles(self, x: int, y: int, zoom: int, network: NetworkType) -> Image.Image:
        """
        returns Beeline coverage tile for defined x, y, zoom map tile
        """

        response = requests.get(
            f"{self.schema}://{self.host}/{self.method}/{network.value}/current/{zoom}/{x}/{y}.png"
        )

        image = PIL.Image.open(io.BytesIO(response.content))

        return image
