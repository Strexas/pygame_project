import pygame
import random
from main import Main

pygame.init()

display = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
game = Main(display)

SPEEDUPEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPEEDUPEVENT)

while True:
    game.event_handler(pygame.event.get())
    game.draw()
    clock.tick(60)
