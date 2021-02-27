import pygame as pg
import os
from random import randint, choice

pg.init()

display = pg.display.set_mode((1000, 700))
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
        if keys[pg.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if keys[pg.K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if keys[pg.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pg.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keydown and keys[pg.K_SPACE] and self.rocket_count:
            Rocket(self.rect.center, (0, self.speed - 70))
            self.rocket_count -= 1
        for i in range(self.rocket_count):
            display.blit(Rocket.image22, (Rocket.image22.get_width() * i, 0))


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__(cars)
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

    def draw_road(self):
        pg.draw.rect(self.surface, (90, 90, 90), (200, 0, 600, 700))
        for i in range(3):
            pg.draw.rect(display, 'white', (150 * (i + 1) + 200, 0, 7, 700))

    def draw_sprites(self, keys, keydown):
        players.update(self.surface, keys, keydown)
        cars.update()
        rockets.update()
        players.draw(self.surface)
        cars.draw(self.surface)
        rockets.draw(self.surface)

    def spawn_cars(self):
        if randint(1, 100) == 1:
            Car(randint(200, 500), -400, (0, randint(3, 7)))


players = pg.sprite.Group()
cars = pg.sprite.Group()
rockets = pg.sprite.Group()
