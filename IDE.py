import pygame
import sys
import datetime
import keyboard
from GUI import Draw


class BefungeIDE:
    def __init__(self):
        self.grid = [[None for _ in range(25)] for _ in range(80)]
        self.add_in_stack = False
        self.screen = pygame.display.set_mode((1210, 700))
        self.grid_size = 15
        self.position = [0, 0]
        self.new_char = ""
        self.can_write = True
        self.can_move = True
        self.timer = datetime.datetime.today()
        self.screen.fill((85, 101, 102))

    def draw_lines(self):
        for x in range(81):
            pygame.draw.line(self.screen, (0, 0, 0), (5 + self.grid_size * x, 200),
                             (5 + self.grid_size * x, 200 + self.grid_size * 25), 1)
        for y in range(26):
            pygame.draw.line(self.screen, (0, 0, 0), (5, 200 + self.grid_size * y),
                             (5 + self.grid_size * 80, 200 + self.grid_size * y), 1)

    def code_loop(self):
        button_rect_start = pygame.Rect(1066, 20, 40, 24)
        button_rect_stop = pygame.Rect(1116, 20, 40, 24)
        gui_tools = Draw(self)
        ready = False
        while not ready:
            current_time = datetime.datetime.today()
            delta_time = (current_time - self.timer).microseconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and self.can_write:
                    keyboard.hook(self.pressed_keys)
                    if len(self.new_char) != 1 and self.can_write:
                        self.new_char = ""
                    self.can_write = False
                elif event.type == pygame.KEYUP:
                    self.can_write = True
                    self.can_move = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_start.collidepoint(event.pos):
                        ready = True
                        break
            gui_tools.drawing(button_rect_start, button_rect_stop, delta_time)
            pygame.display.flip()

    def draw_text(self, surface, text, pos, color=(0, 0, 0)):
        font_size = 24
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    def pressed_keys(self, e):
        if len(e.name) == 1 or e.name == "down" or e.name == "up" or e.name == "right" or e.name == "left":
            self.new_char = e.name
        elif e.name == "space":
            self.new_char = " "
