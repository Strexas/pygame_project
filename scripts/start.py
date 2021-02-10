import pygame

import os
from main import Main  # класс отвечающий за игру
os.chdir('..')  # для удобства вернулись на папку выше
pygame.init()
display = pygame.display.set_mode((1000, 700))  # создали игровое окно
clock = pygame.time.Clock()
fps = 60  # fps игры
game = Main(display, fps)  # передали его на изменения в класс Main


while True:
    game.event_handler(pygame.event.get())  # перехватчик событий
    game.draw()  # отрисовка
    clock.tick(fps)  # FPS
