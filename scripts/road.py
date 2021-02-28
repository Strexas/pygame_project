import pygame as pg
import os
from random import randint, choice

pg.init()

display = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()
car_sprites = [pg.image.load(f'data/sprites/cars/{i}') for i in
               os.listdir(f'data/sprites/cars/')]


class Player(pg.sprite.Sprite):
    image = choice(car_sprites)

    def __init__(self, speed):
        super().__init__(players)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = (500, 500)
        self.speed = speed
        self.rocket_count = 5

    def update(self, display, keys, keydown):
        keys = keys
        keydown = keydown
        if keys[pg.K_UP] and self.rect.y - self.speed > 0:
            self.rect.move_ip(0, -self.speed)
        if keys[pg.K_DOWN] and self.rect.y + self.rect.height + self.speed < 700:
            self.rect.move_ip(0, self.speed)
        if keys[pg.K_LEFT] and self.rect.x - self.speed > 200:
            self.rect.move_ip(-self.speed, 0)
        if keys[pg.K_RIGHT] and self.rect.x + self.rect.width + self.speed < 800:
            self.rect.move_ip(self.speed, 0)
        if keydown and keys[pg.K_SPACE] and self.rocket_count:
            Rocket(self.rect.center, (0, self.speed - 70))
            self.rocket_count -= 1
        for i in range(self.rocket_count):
            display.blit(Rocket.image22, (Rocket.image22.get_width() * i, 0))


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = choice(car_sprites)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed)  # двигаем по дороге
        if self.rect.y > 700:  # если выходит за границу удаляем
            self.kill()

    def stop(self, other):
        self.speed *= 1.25
        other.speed *= 1.25


class Rocket(pg.sprite.Sprite):
    image1 = pg.image.load('data/sprites/interface/rocket.png')
    image1.convert_alpha()
    image12 = pg.transform.scale(image1, (50, 189))
    image2 = pg.image.load('data/sprites/interface/rocket2.png')
    image2.convert_alpha()
    image22 = pg.transform.scale(image2, (40, 93))

    def __init__(self, xy, speed):
        super().__init__(rockets)
        self.image = Rocket.image12
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image12)
        self.rect.x, self.rect.y = xy
        self.rect.x -= 28
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed)
        if self.rect.y < -500:
            self.kill()


class Road:
    def __init__(self, surface):
        self.surface = surface
        self.GAMEOVEREVENT = pg.event.Event(pg.USEREVENT + 2)
        self.rects_y = -70

    def check(self):
        for i in cars:
            for j in rockets:
                if pg.sprite.collide_mask(i, j):
                    i.kill()
                    j.kill()
            for j in players:
                if pg.sprite.collide_mask(i, j):
                    pg.time.delay(1000)
                    pg.event.post(self.GAMEOVEREVENT)
                    cars.empty()
                    players.empty()

    def draw_road(self, speed):
        self.rects_y += speed / 7
        if self.rects_y >= 140:
            self.rects_y -= 140
        self.surface.fill('#3f9b0b')
        pg.draw.rect(self.surface, (90, 90, 90), (200, 0, 600, 700))
        for i in range(4):
            for j in range(-2, 10, 2):
                pg.draw.rect(self.surface, (255, 255, 255), (120 * (i + 1) + 200, self.rects_y + j * 70, 9, 70))

    def draw_sprites(self, keys, keydown):
        players.update(self.surface, keys, keydown)
        cars.update()
        rockets.update()
        players.draw(self.surface)
        cars.draw(self.surface)
        rockets.draw(self.surface)

    def spawn_cars(self, score):
        if score > 10000:
            chance = 4 + score / 1000
        elif score > 5000:
            chance = 3 + score / 1000
        elif score > 1000:
            chance = 2 + score / 1000
        else:
            chance = 1 + score / 1000

        if randint(1, 800) <= chance:
            test = Car(randint(200, 700), -400, (0, 7))
            while pg.sprite.spritecollideany(test, cars):
                test = Car(randint(200, 700), -400, (0, 10))
            cars.add(test)


players = pg.sprite.Group()
cars = pg.sprite.Group()
rockets = pg.sprite.Group()
