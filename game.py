import string
from math import cos, sin

import imageio as iio
import pygame
from pygame import Surface, Color

from Raycaster import ray_caster
from Texture import Texture
from TexturedRaycaster import textured_ray_caster
from UntexturedRaycaster import untextured_ray_caster
from Vector import Vector, fVector
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TEXWIDTH, TEXHEIGHT, world_map, WALL_HEIGHT, MAP_WIDTH, MAP_HEIGHT


def setup_pygame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    return screen


def load_image(uri: string)->Texture:
    image = iio.imread_v2(uri=uri)
    width = int(image.shape[0])
    height = int(image.shape[1])
    texture:Texture = Texture(width=width, height=height)
    for x in range(width):
        for y in range(height):
            texture.get_canvas()[x][y] = Color(int(image[x, y, 0]),int(image[x, y, 1]),int(image[x, y, 2]))
    return texture


class Game:
    _screen = Surface
    _pos:Vector
    _dir_vector:fVector
    _move_speed:float
    _rot_speed:float
    _plane_vector:fVector
    _ray_caster:ray_caster
    _font_obj:pygame.font.Font
    _textures: list[Texture] = [Texture(TEXWIDTH, TEXHEIGHT) for i in range(8)]
    _textured: bool
    _draw_start:list[list[float]]
    _draw_end:list[list[float]]
    _color_line_list=list[list[Color]]
    _old_fps:int

    def __init__(self, pos:Vector, dir_vector:fVector, plane_vector:fVector, textured:bool):
        self._textured = textured
        if textured:
            self._ray_caster: textured_ray_caster = textured_ray_caster(world_map, WALL_HEIGHT, pos, self._textures)
        else:
            self._ray_caster: untextured_ray_caster = untextured_ray_caster(world_map, WALL_HEIGHT, pos, self._textures)
        self._pos = pos
        self._dir_vector = dir_vector
        self._plane_vector = plane_vector
        self._screen = setup_pygame()
        self._font_obj = pygame.font.Font(None, 32)
        self.set_textures()

    def init_speeds(self, move_speed:float, rot_speed:float):
        self._move_speed = move_speed
        self._rot_speed = rot_speed

    def draw_dda(self):
        self._draw_start, self._draw_end, self._color_line_list = self._ray_caster.dda(SCREEN_WIDTH, self._dir_vector, self._plane_vector)
        self.draw_old_dda()

    def draw_old_dda(self):
        for i in range(SCREEN_WIDTH):
            if self._textured:
                for j in range(0,len(self._color_line_list[i])):
                    current = self._color_line_list[i][j]
                    pygame.draw.line(surface=self._screen, color=current, start_pos=[i,self._draw_start[i][j]], end_pos=[i,self._draw_end[i][j]], width=1)
            else:
                pygame.draw.line(surface=self._screen, color=self._color_line_list[i][0],start_pos=[i, self._draw_start[i][0]], end_pos=[i, self._draw_end[i][0]], width=1)

    def clear_screen(self):
        self._screen.fill((0,0,0))

    def read_keys(self, event):
        if event.key == pygame.K_UP:
            if self.walkable_up_x() and world_map[int(self._pos.get_x() + self._dir_vector.get_x() * self._move_speed)][int(self._pos.get_y())] == 0:
                self._pos.set_x(self._pos.get_x() + self._dir_vector.get_x()*self._move_speed)
            if self.walkable_up_y() and world_map[int(self._pos.get_x())][int(self._pos.get_y() + self._dir_vector.get_y() * self._move_speed)] == 0:
                self._pos.set_y(self._pos.get_y() + self._dir_vector.get_y() * self._move_speed)
        if event.key == pygame.K_DOWN:
            if self.walkable_down_x() and world_map[int(self._pos.get_x() - self._dir_vector.get_x() * self._move_speed)][int(self._pos.get_y())] == 0:
                self._pos.set_x(self._pos.get_x() - self._dir_vector.get_x()*self._move_speed)
            if self.walkable_down_y() and world_map[int(self._pos.get_x())][int(self._pos.get_y() - self._dir_vector.get_y() * self._move_speed)] == 0:
                self._pos.set_y(self._pos.get_y() - self._dir_vector.get_y() * self._move_speed)
        if event.key == pygame.K_RIGHT:
            old_dir_x = self._dir_vector.get_x()
            self._dir_vector.set_x(self._dir_vector.get_x() * cos(-self._rot_speed) - self._dir_vector.get_y() * sin(-self._rot_speed))
            self._dir_vector.set_y(old_dir_x * sin(-self._rot_speed) + self._dir_vector.get_y() * cos(-self._rot_speed))
            old_plane_x = self._plane_vector.get_x()
            self._plane_vector.set_x(self._plane_vector.get_x() * cos(-self._rot_speed) - self._plane_vector.get_y() * sin(-self._rot_speed))
            self._plane_vector.set_y(old_plane_x * sin(-self._rot_speed) + self._plane_vector.get_y() * cos(-self._rot_speed))
        if event.key == pygame.K_LEFT:
            old_dir_x = self._dir_vector.get_x()
            self._dir_vector.set_x(self._dir_vector.get_x() * cos(self._rot_speed) - self._dir_vector.get_y() * sin(self._rot_speed))
            self._dir_vector.set_y(old_dir_x * sin(self._rot_speed) + self._dir_vector.get_y() * cos(self._rot_speed))
            old_plane_x = self._plane_vector.get_x()
            self._plane_vector.set_x(self._plane_vector.get_x() * cos(self._rot_speed) - self._plane_vector.get_y() * sin(self._rot_speed))
            self._plane_vector.set_y(old_plane_x * sin(self._rot_speed) + self._plane_vector.get_y() * cos(self._rot_speed))


    def walkable_up_x(self):
        if int(self._pos.get_x() + self._dir_vector.get_x() * self._move_speed) < MAP_WIDTH and self._pos.get_y() < MAP_HEIGHT:
            return True
        return False

    def walkable_up_y(self):
        if int(self._pos.get_x()) < MAP_WIDTH and int(self._pos.get_y() + self._dir_vector.get_y() * self._move_speed) < MAP_HEIGHT:
            return True
        return False

    def walkable_down_x(self):
        if int(self._pos.get_x() - self._dir_vector.get_x() * self._move_speed) < MAP_WIDTH and self._pos.get_y() < MAP_HEIGHT:
            return True
        return False

    def walkable_down_y(self):
        if int(self._pos.get_x()) < MAP_WIDTH and int(self._pos.get_y() - self._dir_vector.get_y() * self._move_speed) < MAP_HEIGHT:
            return True
        return False

    def event_loop(self, running: bool, fps_t):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    self.read_keys(event=event)
                    self.clear_screen()
                    self.draw_dda()
                    self.render_FPS(fps_t)
                    pygame.display.update()
        return running

    def run(self):
        running: bool = True
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 18, bold=True)
        self.draw_dda()
        pygame.display.update()
        old_fps = 0
        fps_t = font.render("60 fps", 1, pygame.Color("RED"))
        while running:
            clock.tick(60)
            fps = int(clock.get_fps())
            if old_fps != fps:
                old_fps = fps
                self.clear_screen()
                self.draw_old_dda()
                fps_text = str(fps) + " fps"
                fps_t = font.render(fps_text, 1, pygame.Color("RED"))
                self.render_FPS(fps_t)
                pygame.display.update()
            running = self.event_loop(running, fps_t)

    def render_FPS(self, fps_t):
        self._screen.blit(fps_t, (0,0))

    def set_textures(self):
        self._textures[0] = load_image("pics/eagle.png")
        self._textures[1] = load_image("pics/redbrick.png")
        self._textures[2] = load_image("pics/purplestone.png")
        self._textures[3] = load_image("pics/greystone.png")
        self._textures[4] = load_image("pics/bluestone.png")
        self._textures[5] = load_image("pics/mossy.png")
        self._textures[6] = load_image("pics/wood.png")
        self._textures[7] = load_image("pics/colorstone.png")

