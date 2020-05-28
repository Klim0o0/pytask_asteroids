import sys


class Menu:
    def __init__(self, pygame, win, window_width, window_height):
        self.pygame = pygame
        self.selected_item = 0
        self.win = win
        self.window_width = window_width
        self.window_height = window_height
        self.items = [(
            window_width / 2 - 20, window_height / 2 - 15, "Start",
            (250, 250, 250), (250, 0, 0), 0),
            (window_width / 2 - 20, window_height / 2 + 15, "Exit",
             (250, 250, 250), (250, 0, 0), 1)]

    def start_menu(self, font_menu):
        selected_item = 0
        while True:
            self.menu_render(font_menu, selected_item)
            for e in self.pygame.event.get():
                if e.type == self.pygame.QUIT:
                    sys.exit()
                if e.type == self.pygame.KEYUP:
                    if e.key == self.pygame.K_ESCAPE:
                        return

                if e.type == self.pygame.KEYDOWN:
                    if e.key == self.pygame.K_DOWN:
                        selected_item = (selected_item + 1) % len(
                            self.items)
                    if e.key == self.pygame.K_UP:
                        selected_item = (selected_item - 1) % len(
                            self.items)
                    if e.key == self.pygame.K_RSHIFT:
                        if selected_item == 0:
                            return
                        if selected_item == 1:
                            sys.exit()
            self.pygame.display.update()

    def start_game_over_screen(self, font):
        while True:
            if self.check_game_over_events():
                return
            self.win.fill((0, 0, 0))
            self.win.blit(
                font.render("To restart press right shift", 1,
                            (250, 250, 250)),
                (self.window_height / 2 - 150, self.window_width / 2))
            self.pygame.display.update()

    def check_game_over_events(self):
        for e in self.pygame.event.get():
            if e.type == self.pygame.QUIT:
                sys.exit()
            if e.type == self.pygame.KEYUP:
                if e.key == self.pygame.K_RSHIFT:
                    return True

    def check_next_level_events(self):
        for e in self.pygame.event.get():
            if e.type == self.pygame.QUIT:
                sys.exit()
            if e.type == self.pygame.KEYUP:
                if e.key == self.pygame.K_RSHIFT:
                    return True
        return False

    def start_next_lvl_screen(self, font):
        while True:
            if self.check_next_level_events():
                return
            self.win.fill((0, 0, 0))
            self.win.blit(
                font.render("Press right shift to next lvl", 1,
                            (250, 250, 250)),
                (self.window_height / 2 - 150, self.window_width / 2))
            self.pygame.display.update()

    def menu_render(self, font, selected_punkt):
        for i in self.items:
            if selected_punkt == i[5]:
                self.win.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                self.win.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
            self.win.blit(
                font.render("To select press right shift", 1, (250, 250, 250)),
                (2, self.window_height - 30))
