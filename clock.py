import pygame

class Clock(object):

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks()

    def restart(self):
        self.time = pygame.time.get_ticks()

    def elapsed(self):
        return pygame.time.get_ticks()-self.time
