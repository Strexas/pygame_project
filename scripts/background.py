import pygame


class Background:
    image = pygame.image.load('data/sprites/background/grass.png')

    def __init__(self, surface, x, y, width, height, speed):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.surface = surface
        self.image = pygame.transform.scale(Background.image, (width, height))

        self.speed = speed
        self.sy = 0

        self.timer = pygame.time.get_ticks()

    def move(self):
        distance = (pygame.time.get_ticks() - self.timer) / 100 * self.speed
        self.timer = pygame.time.get_ticks()
        self.sy += distance

        if self.sy > self.height:
            self.sy = 0

    def speed_up(self, speed):
        self.speed += speed

    def render(self):
        self.move()

        self.surface.blit(
            self.image,
            (0, 0),
            (0, self.height - self.sy,
             self.width, self.sy))

        self.surface.blit(
            self.image,
            (0, self.sy),
            (0, 0, int(self.width),
             int(self.height - self.sy)))

