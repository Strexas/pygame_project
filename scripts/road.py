import pygame
import random


class Road:
    def __init__(self, x, y, width, height, car_sprites:list, speed=10, road_color=pygame.Color(40, 40, 40)):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.speed = 1
        self.markup_width = self.width // 100
        self.markup_height = self.height // 20
        self.generate_markup_rects()
        self.road_color = road_color
    
    def generate_markup_rects(self):
        self.markup_rects = []
        x, y = self.width // 4, -self.markup_height - 30
        while True:
            for i in range(1, 4):
                self.markup_rects.append(pygame.rect.Rect(x * i, y, self.markup_width, self.markup_height))
            y += self.markup_height + 30
            if y > self.height:
                break
    
    def move_markup(self):
        for i in self.markup_rects:
            i.move_ip(0, self.speed)
        if self.markup_rects[0].y > 0:
            del self.markup_rects[-1]
            x, y = self.width // 4, -self.markup_height - 30
            for i in range(1, 4):
                self.markup_rects.insert(0, pygame.rect.Rect(x * i, y, self.markup_width, self.markup_height))
    
    def draw(self):
        self.surface.fill(self.road_color)
        self.move_markup()
        for i in self.markup_rects:
            pygame.draw.rect(self.surface, (210, 210, 210), i)
        return self.surface    
        