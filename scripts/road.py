import pygame
import random


class Road:
    def __init__(self, x, y, width, height, car_sprites:list, speed=5, road_color=pygame.Color(40, 40, 40)):
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
        
        self.car_width = self.width // 4 - 10
        self.car_height = self.height // 8
        self.car_sprites = [pygame.transform.scale(i, (self.car_width, self.car_height)) for i in car_sprites]
        
        self.person = Person(self.width // 2, self.height // 2, self.width, self.height, random.choice(self.car_sprites))

    
    def generate_markup_rects(self):
        self.markup_rects = []
        x, y = self.width // 4, -self.markup_height - 30
        while True:
            for i in range(1, 4):
                self.markup_rects.append(pygame.rect.Rect(x * i, y, self.markup_width, self.markup_height))
            y += self.markup_height + 30
            if y > self.height:
                break
    
    def speed_up(self):
        self.speed += 0.5
    
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
        self.surface.blit(self.person.sprite, self.person.check())
        return self.surface    


class Car:
    def __init__(self, x, y, speed, sprite):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite = sprite

class Person:
    def __init__(self, x, y, width, height, sprite, ):
        self.sprite = sprite
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(x, y, sprite.get_width(), sprite.get_height())
        print(self.rect.width)
        self.state = False
    
    def check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:
            self.state = True
            self.rect.move_ip(0, -3)
        else:
            self.state = False
        if keys[pygame.K_s] and self.rect.y < self.height - self.rect.height:
            self.rect.move_ip(0, 3)
        if keys[pygame.K_a] and self.rect.x > 0:
            print(self.rect.x)
            self.rect.move_ip(-3, 0)
        if keys[pygame.K_d] and self.rect.x < self.width - self.rect.width:
            self.rect.move_ip(3, 0)
        if not self.state and self.rect.y < self.height - self.rect.height:
            self.rect.move_ip(0, 2)
        return self.rect
        
