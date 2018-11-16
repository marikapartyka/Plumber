import pygame
import Game
from Game import GAME


pygame.init()

white=(255,255,255)
game = Game.Game("Plumber", 800, 600, 30, 50)
game.music()




while game.is_running():



    if game.stance[-1] == GAME.INTRO:
        game.game_intro()


    if game.stance[-1] == GAME.OPTIONS:
        game.game_option()
    if game.stance[-1] == GAME.NEWGAME:
        game.handle_events()
        game.update()
        game.display()

    if game.stance[-1] == GAME.WIN:
        game.win()
    if game.stance[-1] == GAME.GAMEOVER:
        game.gameover()






