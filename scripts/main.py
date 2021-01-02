import pygame
import random
from menu import Game_Menu, Main_Menu

class Main:
    def __init__(self, display, fps=60):
        self.display = display
        self.resolution = display.get_size()
        self.FPS = fps
        self.status = 'main_menu'
        self.main_menu = Main_Menu(self.resolution[0], self.resolution[1], {'Новая игра': self.new_game, 'Об игре': self.game_info, 'Авторы': self.authors, 'Выход': self.exit},
                                   'racer', self.resolution[0] // 100 * 5, pygame.Color((100, 190, 85)))
        self.game_menu = Game_Menu(self.resolution[0], self.resolution[1], {'Продолжить': self.resume, 'Назад': self.back,},
                         self.resolution[0] // 100 * 5)
    
    def back(self):
        self.status = 'main_menu'

    def resume(self):
        print('продолжить')
    
    def new_game(self):
        self.status = 'game_menu'
    
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

    def draw(self):
        self.display.fill((0, 0, 0))
        if self.status == 'main_menu':
            self.display.blit(self.main_menu.render(), (0, 0))
        if self.status == 'game_menu':
            self.display.blit(self.game_menu.render(), (0, 0))
        pygame.display.update()

