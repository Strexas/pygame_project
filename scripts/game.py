import pygame
import random
import os
from road import Road
from background import Background


class Game:
    def __init__(self, width, height, speed=10):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.speed = speed
        self.path = 'data'
        self.car_sprites = [pygame.image.load(
            f'{self.path}/sprites/cars/{i}') for i in os.listdir(f'{self.path}/sprites/cars/')]
        self.bg_sprite = pygame.image.load(
            f'{self.path}/sprites/background/grass.png')
        self.bullet_sprite = pygame.image.load(
            f'{self.path}/sprites/interface/bullet.jpeg')
        self.road = Road(width // 4, 0, width // 2,
                         height, self.car_sprites, self.bullet_sprite, speed=self.speed)
        self.left_bg = Background(
            0, 0, self.width // 4, self.height, self.bg_sprite, self.speed)
        self.right_bg = Background(
            self.width - self.width // 4, 0, self.width // 4, self.height, self.bg_sprite, self.speed)
        self.score = 0
        self.score_font = pygame.font.SysFont('Arial', self.width // 50, True)

    def speed_up(self):
        self.speed += 1
        print(self.speed)
        self.road.speed_up(1)
        self.left_bg.speed_up(1)
        self.right_bg.speed_up(1)
    
    def cyckle(self):
        self.score += self.speed / 20
        if int(self.score) % 250 == 0:
            print('add')
            self.road.add_rocket()

    def draw_score(self):
        x, y = self.width - \
            self.score_font.size(
                f'score: {int(self.score)}')[0] - 20, self.height // 20
        self.surface.blit(self.score_font.render(f'score: {int(self.score)}', False, (255, 255, 255)),
                          (x, y))

    def render(self):
        self.cyckle()
        self.surface.blit(self.road.draw(), (self.road.x, self.road.y))
        self.surface.blit(self.left_bg.render(),
                          (self.left_bg.x, self.left_bg.y))
        self.surface.blit(self.right_bg.render(),
                          (self.right_bg.x, self.right_bg.y))
        self.draw_score()
        return self.surface
