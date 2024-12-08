import sys

import pygame
from Vector import Vector, fVector
from game import Game
from constants import START_POSX,START_POSY,DIR_X,DIR_Y,PLANE_X,PLANE_Y

def main():
    args = sys.argv[1:]
    if len(args) > 1:
        raise ValueError("More then 1 arg")
    textured:bool
    if len(args) == 0:
        textured = False
    else:
        if args[0] == 'textured':
            textured = True
        elif args[0] == 'untextured':
            textured = False
        else:
            raise ValueError("Invalid argument")

    pos: Vector = Vector(START_POSX, START_POSY)
    dir_vector: fVector = fVector(DIR_X, DIR_Y)
    plane_vector: fVector = fVector(PLANE_X, PLANE_Y)
    move_speed = 0.3
    rot_speed = 0.1
    game:Game = Game(pos=pos,dir_vector=dir_vector,plane_vector=plane_vector,textured=textured)
    game.init_speeds(move_speed,rot_speed)
    game.run()
    pygame.quit()

main()