"""Everything you need for texture mapping."""

from PIL import Image as im
import numpy as np

class BaseTexture:
    """Class describes base class for textures."""

    def __init__(self):
        self.modificator = lambda x: x

    def get_color(self, point):
        """Returns color of point."""

    def set_modificator(self, modificator):
        """Sets modificator for colors."""
        self.modificator = modificator

    def reset_modificator(self):
        """Resets modificator for colors."""
        self.modificator = lambda x: x

class ColorTexture(BaseTexture):
    """Class describing single color texture."""
    def __init__(
        self,
        color
    ):
        super().__init__()
        self.color = color

    def get_color(self, point):
        return self.modificator(self.color)

class ImageTexture(BaseTexture):
    """Class describing texture made from external image."""

    def __init__(
        self,
        address
    ):
        super().__init__()
        self.image = im.open(address)
        self.width, self.height = self.image.size

    def get_color(self, point):
        s_u, s_v = point
        i = int((self.height - 1) * s_u)
        j = int((self.width - 1 ) * s_v)
        return self.modificator(np.array(self.image.getpixel((j, i))) / 255)

class CheckersTexture(BaseTexture):
    """Class describing texture made from checkers pattern."""

    def __init__(
        self,
        color1,
        color2,
        length
    ):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.length = length

    def get_color(self, point):
        s_u, s_v = point
        s_u = s_u * 100 % (2 * self.length)
        s_v = s_v * 100 % (2 * self.length)
        use_color2 = False
        if s_u // self.length:
            use_color2 = not use_color2
        if not s_v // self.length:
            use_color2 = not use_color2
        if use_color2:
            return self.modificator(self.color2)
        return self.modificator(self.color1)
