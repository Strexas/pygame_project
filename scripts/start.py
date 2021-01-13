import pygame
import random
import os
from main import Main
os.chdir('..')
print(os.getcwd())
pygame.init()
display = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
game = Main(display)


while True:
    game.event_handler(pygame.event.get())
    game.draw()
    clock.tick(60)
