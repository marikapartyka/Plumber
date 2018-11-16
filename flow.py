import pygame

import clock
import Game

from GameObjects import PipeType

class Flow(object):
    def __init__(self, starting_x, starting_y, flowtime):

        self.starting_x = starting_x
        self.starting_y = starting_y
        self.flowtime = flowtime
        self.clock = clock.Clock()
        self.is_flowing = False
        self.x = self.starting_x
        self.y = self.starting_y


    def update(self, map, game):




        if not self.is_flowing:
            if (self.clock.elapsed() > 15000):

                self.clock.restart()
                self.is_flowing = True
        else:
            if(self.clock.elapsed() > self.flowtime):

                self.clock.restart()
                if (self.push_water(map) == False):
                    game.stance.append(Game.GAME.GAMEOVER)

                    self.gameover = True
                elif (self.x, self.y) == (map.cols -1, map.rows -1):
                    game.stance.append(Game.GAME.WIN)
                    self.change_image(map.get_pipe((map.cols -1, map.rows -1)))
                    pygame.time.delay(5000)
                    print("winner")
                    self.win = True
                    self.is_flowing = False








    def push_water(self, map):

        up = (self.x,self.y-1)
        right = (self.x + 1,self.y)
        down = (self.x,self.y+1)
        left = (self.x - 1,self.y)
        current = (self.x, self.y)


        if map.correct_index(down) and self.flow_possible(map.get_pipe(current), map.get_pipe(down), 2):
            map.get_pipe(current).sequence[2] = 2
            map.get_pipe(down).sequence[0] = 2
            self.change_image(map.get_pipe(current))
            self.y += 1


            return True
        elif map.correct_index(right) and self.flow_possible(map.get_pipe(current), map.get_pipe(right), 1):
            map.get_pipe(current).sequence[1] = 2
            map.get_pipe(right).sequence[3] = 2
            self.change_image(map.get_pipe(current))
            self.x += 1
            return True

        elif map.correct_index(left) and self.flow_possible(map.get_pipe(current), map.get_pipe(left), 3):
            map.get_pipe(current).sequence[3] = 2
            map.get_pipe(left).sequence[1] = 2
            self.change_image(map.get_pipe(current))

            self.x -= 1
            return True
        elif map.correct_index(up) and self.flow_possible(map.get_pipe(current), map.get_pipe(up),0):
            map.get_pipe(current).sequence[0] = 2
            map.get_pipe(up).sequence[2] = 2
            self.change_image(map.get_pipe(current))

            self.y -= 1
            return True
        return False

    def change_image(self,pipe):
        if pipe.type == PipeType.STRAIGHT:
            pipe.type = PipeType.STRWATER
        elif pipe.type == PipeType.CORNER:
            pipe.type = PipeType.CORWATER

    def dry_pipe(self,map):
        for pipe in map:
            if pipe.type == PipeType.STRWATER:
                pipe.type = PipeType.STRAIGHT
            elif pipe.type == PipeType.CORWATER:
                pipe.type = PipeType.CORNER



    def flow_possible(self, pipe_out, pipe_in, direction):
        if direction == 0:
            if pipe_out.sequence[0] == pipe_in.sequence[2] == 1:
                return True
            else:
                return False
        if direction == 1:
            if pipe_out.sequence[1] == pipe_in.sequence[3] == 1:
                return True
            else:
                return False
        if direction == 2:
            if pipe_out.sequence[2] == pipe_in.sequence[0] == 1:
                return True
            else:
                return False
        if direction == 3:
            if pipe_out.sequence[3] == pipe_in.sequence[1] == 1:
                return True
            else:
                return False

    def reset(self, map_):
        self.clock.restart()
        self.x = self.starting_x
        self.y = self.starting_y
        self.is_flowing = False
        for pipe in map_:
            for i in range(4):
                if pipe.sequence[i] == 2:
                    pipe.sequence[i] = 1


