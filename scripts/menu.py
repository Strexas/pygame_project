import pygame


class Menu:
    def __init__(self, width:int, height:int, objects: dict, font_size:int, menu_background_color=pygame.Color((0, 0, 0)),
                 menu_rect_color=pygame.Color((100, 190, 85)), text_color=pygame.Color((255, 255, 255)),
                 text_color_focused=pygame.Color((4, 90, 200)), margin=25):
        self.width = width
        self.height = height
        self.margin = margin
        self.menu_bg_color = menu_background_color
        self.menu_rect_color = menu_rect_color
        self.label_color = text_color
        self.label_color_focused = text_color_focused
        self.surface = pygame.Surface((self.width, self.height))
        self.texts = list(objects.keys())
        self.functions = list(objects.values())
        self.font = pygame.font.SysFont('Arial', font_size, True)
        self.font_height = self.font.get_height()
        self.menu_width = max([self.font.size(i)[0]
                              for i in self.texts]) + self.margin * 2
        self.menu_height = len(self.texts) * self.font_height + \
                               self.margin * (len(self.texts) + 2)
        self.menu_rect = pygame.rect.Rect(self.width // 2 - self.menu_width // 2,
                                          self.height // 2 - self.menu_height // 2,
                                          self.menu_width, self.menu_height)
        self.label_rects = self.generate_label_rects()
        self.rendered_labels = [self.font.render(
            i, True, self.label_color) for i in self.texts]
        self.rendered_labels_focused = [self.font.render(
            i, True, self.label_color_focused) for i in self.texts]
        self.timer = pygame.time.get_ticks()


    def generate_label_rects(self):
        y = self.menu_rect.y + self.margin
        rects = []
        for i in self.texts:
            rects.append(pygame.rect.Rect((self.width // 2 - self.font.size(i)[0] // 2, y), self.font.size(i)))
            y += self.margin + self.font_height
        return rects

    def draw_text(self):
        mx, my = pygame.mouse.get_pos()
        m1, m2, m3 = pygame.mouse.get_pressed()
        for i in range(len(self.texts)):
            if self.label_rects[i].collidepoint(mx, my):
                self.surface.blit(self.rendered_labels_focused[i], self.label_rects[i])
                if m1 and self.timer + 500 < pygame.time.get_ticks():
                    self.timer = pygame.time.get_ticks()
                    self.functions[i]()
            else:
                self.surface.blit(self.rendered_labels[i], self.label_rects[i])

    def render(self):
        self.surface.fill(self.menu_bg_color)
        pygame.draw.rect(self.surface, self.menu_rect_color,
                         self.menu_rect, border_radius=7)
        self.draw_text()
        return self.surface
