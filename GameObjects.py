import pygame
import Game
import random
from enum import Enum
import mapgenerator

class D(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    TOTAL = 4

class PipeType(Enum):
    STRAIGHT = 0
    CORNER = 1

    EMPTY = 2
    TOTAL = 3
    STRWATER = 4
    CORWATER = 5

class Pipe(object):

    def __init__(self, type, start_angle = 0, fixed = False):
        self.type = type
        self.fixed = fixed
        self.sequence = list(self.create(type))
        self.start_angle = start_angle
        self.rotate_angle = 0

        self.how_many_rotate()


    def how_many_rotate(self):
        rotate_number = self.start_angle/90
        while rotate_number > 0:
            self.rotate()
            rotate_number -=1

    def create(self, pipetype):
        if pipetype is PipeType.EMPTY:
            return [0,0,0,0]

        if pipetype is PipeType.CORNER:
            return [1, 1, 0, 0]
        if pipetype is PipeType.STRAIGHT:
            return [1, 0, 1, 0]



    def rotate(self):
        if not self.fixed:
            self.increase_angle()

        tmp = self.sequence[0]
        self.sequence[0] = self.sequence[1]
        self.sequence[1] = self.sequence[2]
        self.sequence[2] = self.sequence[3]
        self.sequence[3] = tmp

    def increase_angle(self):
        self.rotate_angle +=90
        self.start_angle += 90
        if(self.start_angle == 360 ):
            self.start_angle = 0
        if (self.rotate_angle == 360):
            self.rotate_angle = 0




class Map(object):
    def __init__(self, map_, rows, cols, size):
        self.rows = rows
        self.cols = cols
        self.size = size


        if type(map_) == list:
            self.map_ = map_

    def __getitem__(self, item):
        return self.map_[item]

    def __setitem__(self, key, value):
        self.map_[key] = value

    def fill(self, pipe):
        self.map_.append(pipe)

    def full_map(self, pipe_list):
        for pipe in pipe_list:
            self.fill(pipe)

    def get_pipe(self, x, y):
        return self.map_[y * self.cols + x]

    def get_pipe(self, coords, global_coords = False):
        if global_coords == True:
            return self.get_pipe((coords[0]//self.size, coords[1]//self.size))
        return self.map_[coords[1] * self.cols + coords[0]]

    def correct_index(self, x, y):
        if self.x < 0 or self.x > self.cols or self.y < 0 or self.y > self.rows:
            return False
        else:
            return True

    def correct_index(self, coords):
        if coords[0] < 0 or coords[0] >= self.cols or coords[1]< 0 or coords[1] >= self.rows:
            return False
        else:
            return True

    def from_i_to_xy(self, i):
        return (i % self.cols, i // self.cols)





class Renderer(object):
    def __init__(self, size):
        self.textures = {PipeType.STRAIGHT : pygame.image.load("STR.bmp").convert(),
                         PipeType.CORNER : pygame.image.load("COR.bmp").convert(),
                         PipeType.EMPTY : pygame.image.load("EMPTY.bmp").convert(),
                         PipeType.STRWATER : pygame.image.load("STRW.bmp").convert(),
                         PipeType.CORWATER: pygame.image.load("CORW.bmp").convert()}
        self.intro_image = pygame.image.load("INTRO.bmp").convert()
        self.button_image = pygame.image.load("BUTTON.bmp").convert()
        self.size = size
        for key in self.textures.keys():
            self.textures[key] = pygame.transform.scale(self.textures[key], (self.size, self.size))






    def display(self, window, map):
        window.fill((0,0,0))

        for i in range(len(map.map_)):
            x,y = map.from_i_to_xy(i)
            x *= map.size
            y *= map.size
            window.blit(self.get_texture(map[i]), (x,y))
        pygame.display.flip()






    def get_texture(self, pipe):
        return pygame.transform.rotate(self.textures[pipe.type],pipe.rotate_angle)





