import pygame
import random


class Road:
    def __init__(self, x, y, width, height, car_sprites: list, speed=5, road_color=pygame.Color(40, 40, 40),
                 car_chance=0.01):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.speed = speed
        self.car_chance = car_chance
        self.markup_width = self.width // 100
        self.markup_height = self.height // 20
        self.generate_markup_rects()
        self.road_color = road_color

        self.car_width = self.width // 4 - 10
        self.car_height = self.height // 6
        self.car_sprites = [pygame.transform.scale(
            i, (self.car_width, self.car_height)) for i in car_sprites]
        self.cars = []
        self.lines_x = [(i * self.width // 4 - self.width // 8) -
                        self.car_width // 2 for i in range(1, 5)]

        self.person = Person(self.width // 2, self.height // 2,
                             self.width, self.height, random.choice(self.car_sprites))

        self.timer = pygame.time.get_ticks()

    def generate_markup_rects(self):
        self.markup_rects = []
        x, y = self.width // 4, -self.markup_height - 30
        while True:
            for i in range(1, 4):
                self.markup_rects.append(pygame.rect.Rect(
                    x * i, y, self.markup_width, self.markup_height))
            y += self.markup_height + 30
            if y > self.height:
                break

    def check_car_collision(self, rect):
        for i in self.cars:
            if rect.colliderect(i.rect):
                return True
        return False

    def spawn_car(self):
        lines = list(range(4))
        y = -self.car_height
        if random.randint(1, 1000) < self.car_chance * 1000:
            print('spawn')
            if len(self.cars) == 0:
                line = lines.pop(random.randint(0, len(lines) - 1))
                self.cars.append(Car(
                    self.lines_x[line], y, self.height, self.speed, random.choice(self.car_sprites)))
                return
            while True:
                line = lines.pop(random.randint(0, len(lines) - 1))
                if len(lines) == 0:
                    return
                if not self.check_car_collision(
                        pygame.rect.Rect(self.lines_x[line], y, self.car_width, self.car_height + self.car_height // 2)):
                    self.cars.append(Car(
                        self.lines_x[line], y, self.height, self.speed, random.choice(self.car_sprites)))
                    break

    def move_cars(self, time):
        for i in range(len(self.cars)):
            if i < len(self.cars):
                if self.cars[i].move(time):
                    del self.cars[i]

    def draw_cars(self):
        for i in self.cars:
            self.surface.blit(i.sprite, i.rect)

    def speed_up(self, speed):
        self.speed += speed
        self.car_chance += 0.002
        for i in self.cars:
            i.set_speed(self.speed)
        self.person.speed_up(speed / 4)

    def move_markup(self, time):
        distance = time * self.speed
        self.timer = pygame.time.get_ticks()
        for i in self.markup_rects:
            i.move_ip(0, distance)
        if self.markup_rects[0].y > 0:
            del self.markup_rects[-1]
            x, y = self.width // 4, -self.markup_height - 30
            for i in range(1, 4):
                self.markup_rects.insert(0, pygame.rect.Rect(
                    x * i, y, self.markup_width, self.markup_height))

    def draw(self):
        time = (pygame.time.get_ticks() - self.timer) / 100
        self.surface.fill(self.road_color)
        self.spawn_car()
        self.move_cars(time)
        self.move_markup(time)
        for i in self.markup_rects:
            pygame.draw.rect(self.surface, (210, 210, 210), i)
        self.draw_cars()
        self.surface.blit(self.person.sprite, self.person.check())
        return self.surface


class Car:
    def __init__(self, x, y, height, speed, sprite: pygame.Surface):
        self.height = height
        self.speed = speed
        self.sprite = sprite
        self.height = height
        self.rect = pygame.rect.Rect(
            x, y, self.sprite.get_width(), self.sprite.get_width())

    def set_speed(self, speed):
        self.speed = speed

    def move(self, time):
        self.rect.move_ip(0, time * self.speed)
        return self.rect.y > self.height


class Person:
    def __init__(self, x, y, width, height, sprite, ):
        self.sprite = sprite
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(
            x, y, sprite.get_width(), sprite.get_height())
        self.speed = 3
        self.state = False

    def speed_up(self, speed):
        self.speed += speed

    def check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:
            self.state = True
            self.rect.move_ip(0, -self.speed)
        else:
            self.state = False
        if keys[pygame.K_s] and self.rect.y < self.height - self.rect.height:
            self.rect.move_ip(0, self.speed)
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_d] and self.rect.x < self.width - self.rect.width:
            self.rect.move_ip(self.speed, 0)
        if not self.state and self.rect.y < self.height - self.rect.height:
            self.rect.move_ip(0, self.speed - 1)
        return self.rect
