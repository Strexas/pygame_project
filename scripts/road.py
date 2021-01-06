import pygame
import random


class Road:
    def __init__(self, x, y, width, height, car_sprites: list, rocket_sprite, speed=5, road_color=pygame.Color(40, 40, 40),
                 car_chance=0.01, rocket_count=5):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.speed = speed
        self.car_chance = car_chance
        self.markup_width = self.width // 80
        self.markup_height = self.height // 10
        self.generate_markup_rects()
        self.road_color = road_color

        self.car_width = self.width // 4 - 20
        self.car_height = self.height // 6
        self.car_sprites = [pygame.transform.scale(
            i, (self.car_width, self.car_height)) for i in car_sprites]
        self.cars = []
        self.lines_x = [(i * self.width // 4 - self.width // 8) -
                        self.car_width // 2 for i in range(1, 5)]

        self.person = Person(self.width // 2, self.height // 2,
                             self.width, self.height, random.choice(self.car_sprites), self.rocket_spawn)

        self.rocket_sprite = pygame.transform.scale(
            rocket_sprite, (self.height // 50, self.height // 10))
        self.rocket_max_count = rocket_count
        self.rocket_count = rocket_count
        self.rockets = []

        self.timer = pygame.time.get_ticks()
        self.spawn_timer = self.timer
        self.spawn_time = 3000
        self.GAMEOVEREVENT = pygame.event.Event(pygame.USEREVENT + 2)

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
        time = pygame.time.get_ticks() - self.spawn_timer
        chance = self.car_chance - (self.spawn_time - time) / 300000
        if random.randint(1, 1000) < chance * 1000:
            self.spawn_timer = pygame.time.get_ticks()
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
    
    def rocket_spawn(self):
        if self.rocket_count > 0:
            self.rocket_count -= 1
            rocket_x = self.person.rect.x + self.person.rect.width // 2
            rocket_y = self.person.rect.y
            self.rockets.append(Rocket(rocket_x, rocket_y, self.height, self.rocket_sprite, self.person.speed + self.width // 8))

    def move_rockets(self, time):
        for i in range(len(self.rockets)):
            if i < len(self.rockets):
                if self.rockets[i].move(time):
                    del self.rockets[i]
    
    def draw_rockets(self):
        for i in self.rockets:
            self.surface.blit(i.sprite, i.rect)

    def add_rocket(self):
        if self.rocket_count < self.rocket_max_count:
            self.rocket_count += 1

    def check_rockets(self):
        for c in range(len(self.cars)):
            if c < len(self.cars):
                for r in range(len(self.rockets)):
                    if r < len(self.rockets):
                        if self.rockets[r].rect.colliderect(self.cars[c].rect):
                            del self.cars[c]
                            del self.rockets[r]
                    else:
                        return
            else:
                return

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

    def draw_interface(self):
        margin = self.width // 50
        x, y = margin, margin
        for i in range(self.rocket_count):
            self.surface.blit(
                self.rocket_sprite, (x + (margin * i + self.rocket_sprite.get_width() * i), y))

    def check_alive(self):
        if self.check_car_collision(self.person.rect):
            print('game over')
            pygame.event.post(self.GAMEOVEREVENT)

    def cyckle(self):
        time = (pygame.time.get_ticks() - self.timer) / 100
        self.surface.fill(self.road_color)
        self.spawn_car()
        self.move_cars(time)
        self.move_markup(time)
        self.move_rockets(time)
        self.check_rockets()
        self.check_alive()

    def draw(self):
        self.cyckle()
        for i in self.markup_rects:
            pygame.draw.rect(self.surface, (210, 210, 210), i)
        self.draw_cars()
        self.surface.blit(self.person.sprite, self.person.check())
        self.draw_rockets()
        self.draw_interface()
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
    def __init__(self, x, y, width, height, sprite, rocket_spawn_function):
        self.sprite = sprite
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect(
            x, y, sprite.get_width(), sprite.get_height())
        self.speed = 3
        self.state = False
        self.rocket_spawn_function = rocket_spawn_function
        self.rocket_timer = pygame.time.get_ticks()

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
            self.rect.move_ip(-self.speed - 2, 0)
        if keys[pygame.K_d] and self.rect.x < self.width - self.rect.width:
            self.rect.move_ip(self.speed + 2, 0)
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() > self.rocket_timer + 2000:
            self.rocket_timer = pygame.time.get_ticks()
            self.rocket_spawn_function()
        if not self.state and self.rect.y < self.height - self.rect.height:
            self.rect.move_ip(0, self.speed - 1)
        return self.rect


class Rocket:
    def __init__(self, x, y, height, sprite, speed):
        self.speed = speed
        self.height = height
        self.sprite = sprite
        self.rect = pygame.Rect(x, y, sprite.get_width(), sprite.get_height())
    
    def move(self, time):
        distance = time * self.speed
        self.rect.move_ip(0, -distance)
        return self.rect.y < -self.rect.height