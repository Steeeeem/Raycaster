class fVector:
    _x:float
    _y:float

    def __init__(self, x:float, y:float):
        self._x = x
        self._y = y

    def get_y(self):
        return self._y

    def get_x(self):
        return self._x

    def set_y(self, y:float):
        self._y = y

    def set_x(self, x:float):
        self._x = x
        
class Vector:
    _x: int
    _y: int

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def get_y(self):
        return self._y

    def get_x(self):
        return self._x

    def set_y(self, y: int):
        self._y = y

    def set_x(self, x: int):
        self._x = x