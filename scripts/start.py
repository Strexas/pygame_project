import pygame

import os

os.chdir('..')  # вернулись на папку выше

from main import Main  # класс отвечающий за игру

pygame.init()
display = pygame.display.set_mode((1000, 700))  # создали игровое окно
clock = pygame.time.Clock()
fps = 100  # fps игры
main = Main(display, fps)  # передали его на изменения в класс Main

while True:
    main.event_handler(pygame.event.get())  # перехватчик событий
    main.draw()  # отрисовка
    clock.tick(fps)  # FPS
