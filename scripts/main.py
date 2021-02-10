import pygame
from menu import Game_Menu, Main_Menu
from game import Game


class Main:
    def __init__(self, display, fps):  # передаем игровое окно и FPS
        self.display = display
        self.resolution = display.get_size()
        self.FPS = fps
        self.speed = 0
        self.status = 'main_menu'  # отслеживаем текущее положение

        # создание Главного меню
        self.main_menu = Main_Menu(
            self.resolution[0], self.resolution[1],

            {'Новая игра': self.new_game,
             'Об игре': self.game_info,
             'Авторы': self.authors,
             'Выход': self.exit},

            self.resolution[0] // 100 * 5)
        # создание Игрового меню
        self.game_menu = Game_Menu(
            self.resolution[0], self.resolution[1],

            {'Продолжить': self.resume,
             'Назад': self.back},

            self.resolution[0] // 100 * 5)

        self.SPEEDUPEVENT = pygame.USEREVENT + 1
        self.GAMEOVEREVENT = pygame.USEREVENT + 2

    def new_game(self):  # начало игры
        self.game = Game(self.resolution[0], self.resolution[1])
        pygame.time.set_timer(self.SPEEDUPEVENT, 100)
        self.status = 'game'

    def back(self):
        self.status = 'main_menu'

    def resume(self):
        self.status = 'game'

    def authors(self):
        pass

    def game_info(self):
        pass

    def exit(self):
        exit()

    def event_handler(self, events):  # перехватчик событий
        for i in events:
            if i.type == pygame.QUIT:
                self.exit()

            if i.type == pygame.KEYDOWN:
                self.keyboard_handler(pygame.key.get_pressed())

            if i.type == self.SPEEDUPEVENT and self.status == 'game':  # ускорение игры
                self.game.speed_up()
                if self.game.speed > 50:
                    self.game.speed = 50
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # перестаем ускорять игру

            if i.type == self.GAMEOVEREVENT:  # выход из игры
                self.status = 'main_menu'

    def keyboard_handler(self, keys):  # переход от игрового меню к игре и обратно
        if not (keys[pygame.K_ESCAPE] and 'game' in self.status):
            return

        self.status = 'game_menu' if self.status == 'game' else 'game'

    def draw(self):  # отрисовка в зависимости от текущего положения
        self.display.fill((0, 0, 0))
        if self.status == 'main_menu':
            self.display.blit(self.main_menu.render(), (0, 0))

        if self.status == 'game_menu':
            self.display.blit(self.game.surface, (0, 0))
            self.display.blit(self.game_menu.render(), (0, 0))

        if self.status == 'game':
            self.display.blit(self.game.render(), (0, 0))
        pygame.display.update()
