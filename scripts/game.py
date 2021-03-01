import pygame

from road import *


class Game:
    def __init__(self, surface, width, height, keys, keydown):
        self.width = width
        self.height = height
        self.surface = surface
        self.speed = 10

        self.gamer = Player(5)
        self.road = Road()

        self.score = 0

        self.score_font = pygame.font.SysFont('Arial', self.width // 50, True)
        self.keys = keys
        self.keydown = keydown
        self.k = 0

    def speed_up(self):
        self.speed += 1

    def cyckle(self):
        self.score += self.speed / 25
        self.k += 1
        if self.k % 200 == 0 and self.gamer.rocket_count < 4:
            self.gamer.rocket_count += 1

    def draw_score(self):
        x, y = self.width - \
               self.score_font.size(f'score: {int(self.score // 10)}')[0] \
               - 20, self.height // 20
        self.surface.blit(
            self.score_font.render(f'score: {int(self.score // 10)}',
                                   False, (255, 255, 255)), (x, y))

    def render(self, keys, keydown):
        self.road.draw_road(self.speed)
        self.road.draw_sprites(keys, keydown)
        self.draw_score()

    def check(self):
        self.cyckle()
        self.road.check()
        self.road.spawn_cars(self.score)
