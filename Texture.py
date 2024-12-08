from pygame import Color


class Texture:
    _width:int
    _height:int
    _canvas = list[list[Color]]

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._canvas = [[Color(0,0,0) for i in range(width)] for j in range(height)]

    def get_canvas(self):
        return self._canvas