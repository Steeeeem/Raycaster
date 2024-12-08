from pygame import Color

from Raycaster import ray_caster
from Texture import Texture
from Vector import Vector
from math import floor
from constants import TEXWIDTH, TEXHEIGHT


class textured_ray_caster(ray_caster):
    def __init__(self, world_map: list[list[int]], wall_h: int, pos: Vector, textures: list[Texture]):
        super().__init__(world_map, wall_h, pos, textures)

    def wall_pos_calculator(self, side_EW: bool):
        wallX: float
        if not side_EW:
            wallX = self._pos.get_y() + self._perp_wall_dist * self._ray_dir.get_y()
        else:
            wallX = self._pos.get_x() + self._perp_wall_dist * self._ray_dir.get_x()
        wallX -= floor(wallX)
        texX: int = int(wallX * float(TEXWIDTH))
        if not side_EW and self._ray_dir.get_x() > 0:
            texX = TEXWIDTH - texX - 1
        if side_EW and self._ray_dir.get_y() < 0:
            texX = TEXWIDTH - texX - 1
        return texX

    def drawer(self, side_EW:bool):
        percentage = 0.30
        texNum: int = self._world_map[self._map_pos.get_x()][self._map_pos.get_y()] - 1
        texX: int = self.wall_pos_calculator(side_EW)
        step: float = 1.0 * TEXHEIGHT / self._line_height
        texPos: float = (self._draw_start - self._wall_h/2 + self._line_height/2) * step
        line_buffer:list[Color] = []
        draw_start_buffer:list[float] = []
        draw_end_buffer:list[float] = []
        for y in range(int(self._draw_start), int(self._draw_end)):
            texY = int(texPos) & (TEXHEIGHT - 1)
            texPos += step
            color: Color = self._textures[texNum].get_canvas()[texY][texX]
            if side_EW:
                color = Color(int(color.r - percentage * color.r), int(color.g - percentage * color.g),
                              int(color.b - percentage * color.b))
            if not line_buffer:
                line_buffer.append(color)
                draw_start_buffer.append(y)
            elif color != line_buffer[-1]:
                line_buffer.append(color)
                draw_end_buffer.append(y-1)
                draw_start_buffer.append(y)
        if line_buffer and len(draw_end_buffer) < len(line_buffer):
            draw_end_buffer.append(self._draw_end - 1)
        if len(draw_start_buffer) != len(draw_end_buffer):
            draw_end_buffer.append(self._draw_end - 1)
        return line_buffer, draw_start_buffer, draw_end_buffer

