import pygame


class Background:
    def __init__(self, x, y, width, height, sprite, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.sprite = pygame.transform.scale(sprite, (width, height))
        self.speed = speed
        self.rects = [pygame.rect.Rect(
            0, -self.height, self.width, self.height), pygame.rect.Rect(0, 0, self.width, self.height)]
        self.timer = pygame.time.get_ticks()

    def move(self):
        distance = (pygame.time.get_ticks() - self.timer) / 100 * self.speed
        self.timer = pygame.time.get_ticks()
        for i in self.rects:
            i.move_ip(0, distance)
        if self.rects[0].y > -self.speed:
            del self.rects[-1]
            self.rects.insert(0, pygame.rect.Rect(
                0, -self.height, self.width, self.height))

    def speed_up(self, speed):
        self.speed += speed

    def render(self):
        self.move()
        for i in self.rects:
            self.surface.blit(self.sprite, i)
        return self.surface
