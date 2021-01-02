import pygame
import random
from menu import Menu

class Game:
    def __init__(self, display, fps=60):
        self.display = display
        self.resolution = display.get_size()
        self.FPS = fps
        self.status = 'menu'
        self.game_menu = Menu(self.resolution[0], self.resolution[1], {'Продолжить': self.resume, 'Назад': self.back,},
                         self.resolution[0] // 100 * 5)
        self.main_menu = Menu(self.resolution[0], self.resolution[1], {'Новая игра': self.new_game, 'Об игре': })
    
    def back(self):
        pass

    def resume(self):
        print('продолжить')
    
    def new_game(self):
        pass
    
    def game_info(self):
        pass

    def cickle(self):
        self.draw()
    
    def event_handler(self, events):
        for i in events:
            if i.type == pygame.QUIT:
                exit()

    def draw(self):
        self.display.fill((0, 0, 0))
        if self.status == 'menu':
            self.display.blit(self.menu.render(), (0, 0))
        pygame.display.update()

