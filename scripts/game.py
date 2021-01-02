import pygame
import random
import os
from road import Road

class Game:
    def __init__(self, width, height, speed=10):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.speed = 5
        self.path = '/'.join(os.getcwd().split('/')) + '/data'
        print(self.path)
        self.car_sprites = [pygame.image.load(f'{self.path}/sprites/cars/{i}') for i in os.listdir(f'{self.path}/sprites/cars/')]
        self.road = Road(width // 4, 0, width // 2, height, self.car_sprites)
    
    def speed_up(self): 
        self.speed += 0.5
        self.road.speed_up()
    
    def render(self):
        self.surface.blit(self.road.draw(), (self.road.x, self.road.y))
        return self.surface
        