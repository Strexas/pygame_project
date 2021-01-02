import pygame
import random
from main import Game

pygame.init()

display = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
game = Game(display)

while True:
    game.event_handler(pygame.event.get())
    game.draw()
    clock.tick(60)