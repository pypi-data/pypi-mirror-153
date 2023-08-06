import string
from typing import Tuple
from .supported_colors import SupportedColors


__all__ = ["ColorParser"]


class ColorParser:
    """
    the color parser class, used to parse: color names, strings, ints, hex ints and tuples into color tuples
    """

    @classmethod
    def parse(cls, color) -> Tuple[int, int, int]:
        """
        parses the string, int, or hex colors into color tuples
        :param color: either color name string, int, hex int, or tuple of the color
        raises:
            ValueError when passed an invalid color
        """
        from .color import Color

        if isinstance(color, str):
            if color.upper() in SupportedColors.__members__:
                return cls._parse_color_name(color)

            if color.startswith("#"):
                color = color.removeprefix("#")
                if all(c in string.hexdigits for c in color):
                    return cls._parse_hex_string(color)

        if isinstance(color, int):
            if color in range(0xFFFFFF+1):
                return cls._parse_int(color)

        if isinstance(color, tuple):
            if all(rgb in range(0xFF+1) for rgb in color):
                return color

        if isinstance(color, Color):
            color = color.r, color.g, color.b

        raise ValueError("{} is not a valid color!".format(color))

    @classmethod
    def _parse_color_name(cls, color: str) -> Tuple[int, int, int]:
        return SupportedColors[color.upper()].value

    @classmethod
    def _parse_hex_string(cls, color: str) -> Tuple[int, int, int]:
        try:
            color = tuple(bytes.fromhex(color))
        except ValueError as exc:
            raise ValueError("{} is not a valid hex color!".format(color)) from exc

        if not all(rgb in range(0xFF+1) for rgb in color) or len(color) != 3:
            raise ValueError("{} is not a valid hex color!".format(color))

        return color

    @classmethod
    def _parse_int(cls, color: int) -> Tuple[int, int, int]:
        blue  =   color %  256
        green = ((color -  blue) // 256) % 256
        red   = ((color -  blue) // 256 ** 2) - green // 256
        return red, green, blue

    @classmethod
    def _color_char(cls, color: Tuple[int, int, int]) -> str:
        return "\033[38;2;{0};{1};{2}m".format(*color)
