from abc import ABC, abstractmethod

from pygame import Color

from Vector import Vector, fVector
from math import floor
from Texture import Texture


def calculate_delta_x(ray_dir:fVector):
    x = ray_dir.get_x()
    if x == 0:
        x = 1e-30
    return abs(1/x)


def calculate_delta_y(ray_dir:fVector):
    y = ray_dir.get_y()
    if y == 0:
        y = 1e-30
    return abs(1/y)


class ray_caster(ABC):
    _map_pos: Vector
    _side_dist: fVector
    _delta_dist: fVector
    _step: Vector
    _side_dist: fVector
    _world_map: list[list[int]]
    _buffer: list[list[int]]
    _textures: list[Texture]
    _pos: Vector
    _perp_wall_dist: float
    _ray_dir: fVector
    _line_height: float
    _draw_start: float
    _draw_end: float
    _textures: list[Texture]
    _wall_h:int

    def __init__(self, world_map:list[list[int]], wall_h:int, pos: Vector, textures: list[Texture]):
        self._world_map = world_map
        self._wall_h = wall_h
        self._pos = pos
        self._textures = textures

    def dda(self, width:int,dir_vector:fVector, plane: fVector):
        draw_start_list:list[list[float]] = []
        draw_end_list:list[list[float]] = []
        color_line_list:list[list[Color]] = []
        for i in range(width):
            CAMERA_X:float = 2 * i / float(width) - 1
            self._ray_dir: fVector = fVector(dir_vector.get_x() + plane.get_x() * CAMERA_X, dir_vector.get_y() + plane.get_y() * CAMERA_X)
            self._map_pos = Vector(int(self._pos.get_x()), int(self._pos.get_y()))
            self._side_dist: fVector
            self._delta_dist = fVector(calculate_delta_x(self._ray_dir), calculate_delta_y(self._ray_dir))
            self.calculate_step()
            hit, side_EW = self.hit_check()
            if not side_EW:
                self._perp_wall_dist = self._side_dist.get_x() - self._delta_dist.get_x()
            else:
                self._perp_wall_dist = self._side_dist.get_y() - self._delta_dist.get_y()
            self._line_height: int = int(self._wall_h/self._perp_wall_dist)
            self._draw_start = -floor(self._line_height/2) + floor(self._wall_h/2)
            if self._draw_start < 0:
                self._draw_start = 0
            self._draw_end = floor(self._line_height/2) + floor(self._wall_h/2)
            if self._draw_end >= self._wall_h:
                self._draw_end = self._wall_h-1
            color_line, draw_start_buffer, draw_end_buffer = self.drawer(side_EW)
            draw_start_list.append(draw_start_buffer)
            draw_end_list.append(draw_end_buffer)
            color_line_list.append(color_line)
        return draw_start_list, draw_end_list, color_line_list

    def hit_check(self):
        hit: bool = False
        side_EW: bool = False
        while not hit:
            if self._side_dist.get_x() < self._side_dist.get_y():
                self._side_dist.set_x(self._side_dist.get_x() + self._delta_dist.get_x())
                self._map_pos.set_x(self._map_pos.get_x() + self._step.get_x())
                side_EW = False
            else:
                self._side_dist.set_y(self._side_dist.get_y() + self._delta_dist.get_y())
                self._map_pos.set_y(self._map_pos.get_y() + self._step.get_y())
                side_EW = True
            if self._world_map[self._map_pos.get_x()][self._map_pos.get_y()] > 0:
                hit = True
        return hit, side_EW

    def calculate_step(self):
        self._step = Vector(0,0)
        self._side_dist = fVector(0,0)
        if self._ray_dir.get_x() < 0:
            self._step.set_x(-1)
            self._side_dist.set_x((self._pos.get_x() - self._map_pos.get_x())*self._delta_dist.get_x())
        else:
            self._step.set_x(1)
            self._side_dist.set_x((self._map_pos.get_x() + 1.0 - self._pos.get_x())*self._delta_dist.get_x())
        if self._ray_dir.get_y() < 0:
            self._step.set_y(-1)
            self._side_dist.set_y((self._pos.get_y() - self._map_pos.get_y()) * self._delta_dist.get_y())
        else:
            self._step.set_y(1)
            self._side_dist.set_y((self._map_pos.get_y() + 1.0 - self._pos.get_y()) * self._delta_dist.get_y())

    @abstractmethod
    def drawer(self, side_EW: bool):
        pass


