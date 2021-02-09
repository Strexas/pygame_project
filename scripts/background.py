import pygame


class Background:
    def __init__(self, x, y,
                 width, height,
                 sprite, speed):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))
        self.sprite = pygame.transform.scale(sprite, (width, height))

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
            self.sprite,
            (0, 0),
            (0, self.height - self.sy,
             self.width, self.sy))

        self.surface.blit(
            self.sprite,
            (0, self.sy),
            (0, 0, self.width,
             self.height - self.sy))

        return self.surface
