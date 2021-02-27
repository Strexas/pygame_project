import pygame

from road import *
from background import Background


class Game:
    def __init__(self, surface, width, height, keys, keydown):
        self.width = width
        self.height = height
        self.surface = surface
        self.speed = 10

        self.gamer = Player(5)
        self.road = Road(surface)

        self.bg = Background(surface, 0, 0, self.width, self.height, self.speed)

        self.score = 0

        self.score_font = pygame.font.SysFont('Arial', self.width // 50, True)
        self.keys = keys
        self.keydown = keydown

    def speed_up(self):
        self.speed += 1
        self.bg.speed_up(1)

    def cyckle(self):
        self.score += 1
        if int(self.score) % 200 == 0 and self.gamer.rocket_count < 4:
            self.gamer.rocket_count += 1

    def draw_score(self):
        x, y = self.width - \
               self.score_font.size(f'score: {int(self.score)}')[0] \
               - 20, self.height // 20
        self.surface.blit(
            self.score_font.render(f'score: {int(self.score)}',
                                   False, (255, 255, 255)), (x, y))

    def render(self, keys, keydown):
        self.bg.render()
        self.road.draw_road()
        self.road.draw_sprites(keys, keydown)
        self.draw_score()

    def check(self):
        self.cyckle()
        self.road.check()
        self.road.spawn_cars()
