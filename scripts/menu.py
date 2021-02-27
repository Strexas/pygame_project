import pygame
from music import Menu_music, Game_music1, Game_music2, channel, pressing, moving
from random import choice


class Menu:
    def __init__(self, width: int, height: int, objects: dict, font_size: int):
        self.width = width
        self.height = height
        self.margin = 0

        self.functions = list(objects.values())
        self.texts = list(objects.keys())

        self.label_color = pygame.Color((255, 255, 255))
        self.label_color_focused = pygame.Color((4, 90, 200))
        self.bg_color = pygame.Color((100, 190, 85))
        self.font = pygame.font.Font('data/fonts/19255.ttf', font_size)

        self.surface = pygame.Surface((self.width, self.height))

        self.rendered_labels = []
        self.rendered_labels_focused = []

        for i in self.texts:
            self.rendered_labels.append(self.font.render(i, True, self.label_color))
            self.rendered_labels_focused.append(self.font.render(i, True, self.label_color_focused))

        self.label_rects = []

        self.moving_cursor = (False, -1)

    def generate_label_rects(self, y):
        y = y

        text_rects = []

        for i in self.texts:
            rect = pygame.rect.Rect(
                ((self.width - self.font.size(i)[0]) // 2, y),
                self.font.size(i))

            text_rects.append(rect)

            y += self.margin + self.font.size(i)[1]

        return text_rects

    def draw_text(self):
        mx, my = pygame.mouse.get_pos()

        m1, m2, m3 = pygame.mouse.get_pressed()

        for i in range(len(self.texts)):
            if self.label_rects[i].collidepoint(mx, my):
                if self.moving_cursor[1] != i:
                    self.moving_cursor = (True, i)

                self.surface.blit(self.rendered_labels_focused[i], self.label_rects[i])

                if m1:
                    if type(self) == type(Main_Menu):
                        pressing.play()
                        pygame.time.delay(4000)
                        channel.play(choice((Game_music1, Game_music2)))
                    self.functions[i]()
            else:
                self.surface.blit(self.rendered_labels[i], self.label_rects[i])


class Game_Menu(Menu):
    def __init__(self, width: int, height: int, objects: dict, font_size: int):
        super().__init__(width, height, objects, font_size)

        self.margin = 25

        self.surface_alpha = 225
        self.surface.set_alpha(self.surface_alpha)

        self.font_height = font_size

        self.menu_width = self.font.size(max(self.texts))[0] + self.margin * 2

        self.menu_height = len(self.texts) * (self.font_height + self.margin) + self.margin

        self.menu_rect = pygame.rect.Rect((self.width - self.menu_width) // 2,
                                          (self.height - self.menu_height) // 2,
                                          self.menu_width, self.menu_height)

        self.label_rects = self.generate_label_rects(self.menu_rect.y + self.margin)

        for x, y in zip(self.rendered_labels, self.rendered_labels_focused):
            x.set_alpha(self.surface_alpha)
            y.set_alpha(self.surface_alpha)

    def render(self):
        if self.moving_cursor[0]:
            moving.stop()
            moving.play()
            self.moving_cursor = (False, self.moving_cursor[1])
        pygame.draw.rect(self.surface,
                         self.bg_color,
                         self.menu_rect, border_radius=7)

        self.draw_text()

        return self.surface


class Main_Menu(Menu):
    def __init__(self, width, height, objects: dict, font_size: int):
        super().__init__(width, height, objects, font_size)

        channel.play(Menu_music)

        self.name_font = pygame.font.SysFont('Arial', int(font_size * 2), True)

        self.name_fs = int(font_size * 1.25)
        self.margin = 35
        self.bottom_margin = 150

        self.game_name = 'Racer'

        self.rendered_name = self.name_font.render(self.game_name, True, self.label_color)

        self.label_rects = self.generate_label_rects(
            self.margin * 4 + self.rendered_name.get_height())

        self.draw_text = self.draw_name(self.draw_text)

    def draw_name(self, func):
        def decorated_draw():
            func()
            self.name_rect = pygame.rect.Rect(
                (self.width - self.rendered_name.get_width()) // 2,
                self.margin * 2, self.rendered_name.get_width(),
                self.rendered_name.get_height())
            self.surface.blit(self.rendered_name, self.name_rect)

        return decorated_draw

    def render(self):
        if self.moving_cursor[0]:
            moving.stop()
            moving.play()
            self.moving_cursor = (False, self.moving_cursor[1])
        self.surface.fill(self.bg_color)
        self.draw_text()
        return self.surface
