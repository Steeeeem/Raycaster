from pygame import Color
from Raycaster import ray_caster
from Vector import Vector
from Texture import Texture

class untextured_ray_caster(ray_caster):

    def __init__(self,world_map:list[list[int]], wall_h:int, pos: Vector, textures: list[Texture]):
        super().__init__(world_map, wall_h, pos, textures)

    def drawer(self, side_EW: bool):
        wall: int = self._world_map[self._map_pos.get_x()][self._map_pos.get_y()]
        rgb = 255
        list_color:list[Color] = []
        if side_EW:
            rgb -= 50
        if wall == 1:
            list_color.append(Color(rgb, 0, 0))
        elif wall == 2:
            list_color.append(Color(0, rgb, 0))
        elif wall == 3:
            list_color.append(Color(0, 0, rgb))
        else:
            list_color.append(Color(rgb, rgb, 0))
        return list_color, [self._draw_start], [self._draw_end]

