import pygame
from enum import Enum
class GAME(Enum):
    INTRO = 0
    OPTIONS = 1
    WIN = 2
    GAMEOVER = 3
    NEWGAME = 4

import mapgenerator
import GameObjects
import flow





class Game(object):
    pygame.font.init()

    smallfont = pygame.font.SysFont(None, 20)
    medfont = pygame.font.SysFont(None, 50)
    largefont = pygame.font.SysFont(None, 80)





    def __init__(self, title, screen_width = 800, screen_height = 600, framerate = 30, size = 200):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        self.running = True
        self.english = True
        self.stance = [GAME.INTRO]


        self.intro = True
        self.option = False
        self.sound = True

        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        pygame.display.set_caption("Plumber")

        self.map = GameObjects.Map([], self.screen_height//size,self.screen_width//size, size)

        self.flow = flow.Flow(0, 0, 1000)

        print("game object has been created")
        self.size = size
        self.renderer = GameObjects.Renderer(size)
        pipe_list = mapgenerator.generate_map(self.map.rows, self.map.cols)


        self.map.full_map(pipe_list)


    def is_running(self):
        return self.running

    def game_intro(self):
        self.screen.blit(self.renderer.intro_image, (0, 0))
        new_game_b = self.screen.blit(self.renderer.button_image, (100, 430))
        options_b = self.screen.blit(self.renderer.button_image, (300, 450))
        exit_b = self.screen.blit(self.renderer.button_image, (500, 430))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    self.quit()
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_b.collidepoint(pygame.mouse.get_pos()):
                    self.stance.append(GAME.NEWGAME)
                    self.intro = False
                elif options_b.collidepoint(pygame.mouse.get_pos()):
                    self.stance.append(GAME.OPTIONS)
                    self.option = True
                    self.intro = False

                elif exit_b.collidepoint(pygame.mouse.get_pos()):
                    self.quit()
                    quit()
        if self.english == True:
            self.text_to_button("PLAY", (0,0,0), 160, 465, 0, 0)
            self.text_to_button("OPTIONS", (0, 0, 0), 350, 480, 0, 0)
            self.text_to_button("EXIT", (0, 0, 0), 570, 465, 0, 0)
            self.message_to_screen("Welcome to Plumber", (0, 0, 0), 50, "large")
        if self.english == False:
            self.text_to_button("GRAJ", (0,0,0), 160, 465, 0, 0)
            self.text_to_button("OPCJE", (0, 0, 0), 350, 480, 0, 0)
            self.text_to_button("WYJŚCIE", (0, 0, 0), 570, 465, 0, 0)
            self.message_to_screen("Witaj w grze Plumber", (0, 0, 0), 50, "large")

        pygame.display.update()
        self.clock.tick(15)

    def game_option(self):

        self.screen.blit(self.renderer.intro_image, (0, 0))
        sound_b = self.screen.blit(self.renderer.button_image, (100, 430))
        language_b = self.screen.blit(self.renderer.button_image, (300, 450))

        return_b = self.screen.blit(self.renderer.button_image, (500,430))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_b.collidepoint(pygame.mouse.get_pos()):
                    if self.sound == True:
                        pygame.mixer.music.stop()
                        self.sound = False
                    elif self.sound == False:
                        pygame.mixer.music.play(30)
                    self.intro = False
                elif language_b.collidepoint(pygame.mouse.get_pos()):
                    self.english = not self.english
                elif return_b.collidepoint(pygame.mouse.get_pos()):
                    self.stance.pop()
                    self.intro = True
                    self.option = False



        if self.english == True:
            self.text_to_button("SOUND", (0, 0, 0), 160, 465, 0, 0)
            self.text_to_button("LANGUAGE", (0, 0, 0), 350, 485, 0, 0)
            self.text_to_button("RETURN", (0,0,0),550, 465, 0, 0)
            pygame.display.update()
        if self.english == False:
            self.text_to_button("DŹWIĘK", (0, 0, 0), 155, 465, 0, 0)
            self.text_to_button("JĘZYK", (0, 0, 0), 360, 480, 0, 0)
            self.text_to_button("POWRÓT", (0, 0, 0), 550, 465, 0, 0)

            pygame.display.update()

        pygame.display.update()
        self.clock.tick(15)



    def text_to_button(self, msg, color, buttonx, buttony, buttonw, buttonh, size = "small"):
        textSurf, textRect = self.text_objects(msg,color,size)
        textRect.right = buttonx
        textRect.top = buttony
        textRect.width = buttonw
        textRect.height = buttonh
        textRect.center = ((buttonx + (buttonw/2)), buttony + (buttonh/2))
        self.screen.blit(textSurf, textRect)


    def quit(self):
        self.running = False

    def display(self):
        self.renderer.display(self.screen, self.map)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_p:
                    self.pause()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.map.get_pipe(pygame.mouse.get_pos(), global_coords=True).rotate()




    def update(self):
        self.flow.update(self.map, self)


    def text_objects(self, text, color, size):
        if size == "small":
            textSurface = self.smallfont.render(text, True, color)
        if size == "medium":
            textSurface = self.medfont.render(text, True, color)
        if size == "large":
            textSurface = self.largefont.render(text, True, color)
        return textSurface, textSurface.get_rect()


    def message_to_screen(self, msg, color, y_displace=0, size = "small"):
        textSurf, textRect = self.text_objects(msg, color, size)

        textRect.center = (self.screen_width / 2), (self.screen_height / 2) + y_displace
        self.screen.blit(textSurf, textRect)



    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_q:
                        self.quit()
                        quit()
            self.screen.fill((123,53,123))
            self.message_to_screen("Paused", (0, 0, 0), -10)
            self.message_to_screen("Press p to continue or Q to quit", (0,0,0), 10)
            pygame.display.update()
            self.clock.tick(15)


    def music(self):
        pygame.mixer.music.load("ratsrats_0.ogg")
        pygame.mixer.music.play(30)

    def win(self):
        while self.flow.win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.stance.pop()
                        self.new_level()

                        self.flow.reset(self.map)
                        self.flow.win = False

                    elif event.key == pygame.K_q:
                        self.quit()
                        quit()
            self.screen.fill((10, 100, 250))
            if self.english == True:
                self.message_to_screen("Winner", (0, 0, 0), -10, "large")
                self.message_to_screen("Press N to next level or Q to quit", (0, 0, 0), 50, "medium")
            if self.english == False:
                self.message_to_screen("Wygrana", (0, 0, 0), -10, "large")
                self.message_to_screen("Naciśnij N, aby przejść do kolejnego poziomu", (0, 0, 0), 40, "medium")
                self.message_to_screen(" lub Q, aby wyjść.", (0, 0, 0), 60, "medium")

            pygame.display.update()
            self.clock.tick(15)
    def new_level(self):

        pipe_list = mapgenerator.generate_map(self.map.rows, self.map.cols)
        self.map = GameObjects.Map([],self.screen_height//self.size,self.screen_width//self.size, self.size)
        self.map.full_map(pipe_list)




    def gameover(self):


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.quit()
                    quit()
                if event.key == pygame.K_c:
                    self.stance.pop()
                    self.flow.dry_pipe(self.map)
                    self.flow.reset(self.map)


        self.screen.fill((0, 0, 0))
        if self.english == True:
            self.message_to_screen("You Lose", (255, 255, 255), -10, "large")
            self.message_to_screen("Press C to start again or Q to quit", (255, 255, 255), 35, "medium")
        if self.english == False:
            self.message_to_screen("Przegrałeś :(", (255, 255, 255), -10, "large")
            self.message_to_screen("Naciśnij C, aby spróbować jeszcze raz ", (255, 255, 255), 40, "medium")
            self.message_to_screen("lub Q, aby wyjść.", (255, 255, 255), 75,
                                   "medium")

        pygame.display.update()
        self.clock.tick(15)