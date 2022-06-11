import PIL


class Operator:
    """
    base class for Operator
    """

    def __init__(self, schema: str, host: str) -> object:
        self.schema = schema
        self.host = host

    def get_tiles(self, x, y, zoom) -> PIL.PngImagePlugin.PngImageFile:
        """
        returns coverage tile for defined x, y, zoom map tile
        """

        pass
