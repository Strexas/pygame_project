import pygame
import random
from menu import Game_Menu, Main_Menu
from game import Game


class Main:
    def __init__(self, display, fps=60):
        self.display = display
        self.resolution = display.get_size()
        self.FPS = fps
        self.speed = 10
        self.status = 'main_menu'

        self.main_menu = Main_Menu(self.resolution[0], self.resolution[1], {'Новая игра': self.new_game, 'Об игре': self.game_info, 'Авторы': self.authors, 'Выход': self.exit},
                                   'racer', self.resolution[0] // 100 * 5, pygame.Color((100, 190, 85)))
        self.game_menu = Game_Menu(self.resolution[0], self.resolution[1], {'Продолжить': self.resume, 'Назад': self.back, },
                                   self.resolution[0] // 100 * 5, alpha=225)

        self.SPEEDUPEVENT = pygame.USEREVENT + 1
        self.GAMEOVEREVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SPEEDUPEVENT, 4000)

    def back(self):
        print('main')
        self.status = 'main_menu'

    def resume(self):
        self.status = 'game'

    def new_game(self):
        self.game = Game(self.resolution[0], self.resolution[1])
        pygame.time.set_timer(self.SPEEDUPEVENT, 100)
        self.status = 'game'

    def game_info(self):
        pass

    def authors(self):
        pass

    def exit(self):
        exit()

    def cickle(self):
        self.draw()

    def event_handler(self, events):
        for i in events:
            if i.type == pygame.QUIT:
                self.exit()
            if i.type == pygame.KEYDOWN:
                self.keyboard_handler(pygame.key.get_pressed())
            if i.type == self.SPEEDUPEVENT and self.status == 'game':
                self.game.speed_up()
                if self.game.speed > 30:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            if i.type == self.GAMEOVEREVENT:
                print(self.game.score)
                self.status = 'main_menu'

    def keyboard_handler(self, keys):
        if self.status == 'game':
            if keys[pygame.K_ESCAPE]:
                self.status = 'game_menu'
            return
        if self.status == 'game_menu':
            if keys[pygame.K_ESCAPE]:
                self.status = 'game'
            return

    def draw(self):
        self.display.fill((0, 0, 0))
        if self.status == 'main_menu':
            self.display.blit(self.main_menu.render(), (0, 0))
        if self.status == 'game_menu':
            self.display.blit(self.game.surface, (0, 0))
            self.display.blit(self.game_menu.render(), (0, 0))
        if self.status == 'game':
            self.display.blit(self.game.render(), (0, 0))
        pygame.display.update()
