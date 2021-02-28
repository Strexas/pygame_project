import pygame
from menu import Game_Menu, Main_Menu, Authors, GameInfo
from game import Game
from music import channel, menu_music, game_music
from road import players, cars, rockets


class Main:
    def __init__(self, display, fps):  # передаем игровое окно и FPS
        self.display = display
        self.resolution = display.get_size()
        self.FPS = fps
        self.speed = 0
        self.status = 'main_menu'  # отслеживаем текущее положение

        # загружаем очки
        self.key = 'qwerty1029'
        with open('data/score.txt') as f:
            self.scores = int(f.readline())

        # создание Главного меню
        self.main_menu = Main_Menu(
            self.resolution[0], self.resolution[1],

            {'Новая игра': self.new_game,
             'Об игре': self.game_info,
             'Авторы': self.authors,
             'Выход': self.exit},

            self.resolution[0] // 100 * 5, self.scores)
        # создание Игрового меню
        self.game_menu = Game_Menu(
            self.resolution[0], self.resolution[1],

            {'Продолжить': self.resume,
             'Назад': self.back},

            self.resolution[0] // 100 * 5)

        # создание меню авторов
        self.authors_menu = Authors(self.resolution[0], self.resolution[1])
        # создание меню об игре
        self.game_info_menu = GameInfo(self.resolution[0], self.resolution[1])

        self.SPEEDUPEVENT = pygame.USEREVENT + 1
        self.GAMEOVEREVENT = pygame.USEREVENT + 2
        self.keys = 0
        self.keydown = 0

    def new_game(self):  # начало игры
        self.game = Game(self.display, self.resolution[0], self.resolution[1], self.keys, self.keydown)
        channel.play(game_music[0])
        channel.queue(game_music[1])
        pygame.time.set_timer(self.SPEEDUPEVENT, 100)
        self.status = 'game'

    def back(self):
        self.status = 'main_menu'

    def resume(self):
        self.status = 'game'

    def authors(self):
        self.status = 'authors'

    def game_info(self):
        self.status = 'game_info'

    def exit(self):
        exit()

    def event_handler(self, events):  # перехватчик событий
        self.keys = pygame.key.get_pressed()
        for i in events:
            if i.type == pygame.QUIT:
                self.exit()

            if i.type == pygame.KEYDOWN:
                self.keyboard_handler(self.keys)
                self.keydown = True

            if i.type == self.SPEEDUPEVENT and self.status == 'game':  # ускорение игры
                self.game.speed_up()
                if self.game.speed > 70:
                    self.game.speed = 70
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # перестаем ускорять игру

            if i.type == self.GAMEOVEREVENT:  # выход из игры
                self.status = 'main_menu'
                channel.play(menu_music[0])
                channel.queue(menu_music[1])
                if self.game.score // 10 > self.scores:
                    with open('data/score.txt', 'w') as w:
                        w.write(str(int(self.game.score // 10)))
                    self.scores = int(self.game.score // 10)
                    self.main_menu.update_scores(self.scores)

    def keyboard_handler(self, keys):  # переход от игрового меню к игре и обратно
        if keys[pygame.K_h]:
            channel.set_volume(channel.get_volume() + 0.01)

        if keys[pygame.K_l]:
            channel.set_volume(channel.get_volume() - 0.01)

        if keys[pygame.K_ESCAPE] and (self.status == 'authors' or self.status == 'game_info'):
            self.status = 'main_menu'

        if not (keys[pygame.K_ESCAPE] and 'game' in self.status):
            return

        self.status = 'game_menu' if self.status == 'game' else 'game'

    def draw(self):  # отрисовка в зависимости от текущего положения
        self.display.fill((0, 0, 0))
        if self.status == 'main_menu':
            self.display.blit(self.main_menu.render(), (0, 0))
            pygame.display.update()

        if self.status == 'game_menu':
            self.game.road.draw_road(self.speed)
            players.draw(self.display)
            cars.draw(self.display)
            rockets.draw(self.display)
            self.display.blit(self.game_menu.render(), (0, 0))
            pygame.display.update()

        if self.status == 'authors':
            self.display.blit(self.authors_menu.render(), (0,0))
            pygame.display.update()

        if self.status == 'game_info':
            self.display.blit(self.game_info_menu.render(), (0, 0))
            pygame.display.update()

        if self.status == 'game':
            self.game.render(self.keys, self.keydown)
            pygame.display.update()
            self.game.check()
            self.keydown = 0


