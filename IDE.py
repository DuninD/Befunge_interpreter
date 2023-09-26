import pygame
import sys
import datetime
import keyboard
from GUI import Draw


class BefungeIDE:
    def __init__(self, save):
        self.button_rect_blue = pygame.Rect(5, 20, 50, 24)
        self.button_rect_gray = pygame.Rect(65, 20, 50, 24)
        self.button_rect_purple = pygame.Rect(125, 20, 50, 24)
        self.button_rect_green = pygame.Rect(185, 20, 50, 24)
        self.screen = pygame.display.set_mode((1210, 700))
        self.write_code = True
        self.read_code = False
        self.add_new = False
        self.is_library = False
        if save.data["theme"] == [1]:
            self.screen.fill((85, 101, 102))
            self.square_fill = (203, 203, 203)
        elif save.data["theme"] == [2]:
            self.screen.fill((137, 9, 137))
            self.square_fill = (178, 102, 255)
        elif save.data["theme"] == [3]:
            self.screen.fill((0, 51, 0))
            self.square_fill = (102, 255, 102)
        else:
            self.screen.fill((152, 255, 255))
            self.square_fill = (51, 153, 203)
        self.save = save
        self.grid = [[None for _ in range(25)] for _ in range(80)]
        self.add_in_stack = False
        self.grid_size = 15
        self.position = [0, 0]
        self.new_char = ""
        self.can_write = True
        self.can_move = True
        self.timer = datetime.datetime.today()
        self.answer = ""
        self.is_delay = False

    def draw_lines(self):
        for x in range(81):
            pygame.draw.line(self.screen, (0, 0, 0), (5 + self.grid_size * x, 200),
                             (5 + self.grid_size * x, 200 + self.grid_size * 25), 1)
        for y in range(26):
            pygame.draw.line(self.screen, (0, 0, 0), (5, 200 + self.grid_size * y),
                             (5 + self.grid_size * 80, 200 + self.grid_size * y), 1)

    def code_loop(self):
        button_rect_start = pygame.Rect(1066, 20, 40, 24)
        button_rect_delay = pygame.Rect(990, 20, 66, 24)
        button_rect_stop = pygame.Rect(1116, 20, 40, 24)
        button_rect_save = pygame.Rect(490, 20, 90, 24)
        button_rect_library = pygame.Rect(585, 20, 90, 24)
        gui_tools = Draw(self, self.square_fill)
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
                        self.write_code = False
                        self.read_code = True
                        break
                    elif button_rect_save.collidepoint(event.pos):
                        ready = True
                        self.write_code = False
                        self.add_new = True
                        break
                    elif button_rect_library.collidepoint(event.pos):
                        ready = True
                        self.write_code = False
                        self.is_library = True
                        break
                    elif button_rect_delay.collidepoint(event.pos):
                        self.is_delay = not self.is_delay
                    elif self.button_rect_gray.collidepoint(event.pos):
                        self.save.data["theme"] = [1]
                        self.save.write(self.save.data, 'users.json')
                        self.screen.fill((85, 101, 102))
                        gui_tools.fill = (203, 203, 203)
                        self.square_fill = (203, 203, 203)
                        if self.answer != "":
                            self.screen.fill((255, 255, 255), [[5, 587], [1200, 100]])
                            self.screen.blit(pygame.font.Font(None, 24).render(self.answer, True, (0, 0, 0)), (7, 590))
                    elif self.button_rect_purple.collidepoint(event.pos):
                        self.save.data["theme"] = [2]
                        self.save.write(self.save.data, 'users.json')
                        self.screen.fill((137, 9, 137))
                        gui_tools.fill = (178, 102, 255)
                        self.square_fill = (178, 102, 255)
                        if self.answer != "":
                            self.screen.fill((255, 255, 255), [[5, 587], [1200, 100]])
                            self.screen.blit(pygame.font.Font(None, 24).render(self.answer, True, (0, 0, 0)), (7, 590))
                    elif self.button_rect_green.collidepoint(event.pos):
                        self.save.data["theme"] = [3]
                        self.save.write(self.save.data, 'users.json')
                        self.screen.fill((0, 51, 0))
                        gui_tools.fill = (102, 255, 102)
                        self.square_fill = (102, 255, 102)
                        if self.answer != "":
                            self.screen.fill((255, 255, 255), [[5, 587], [1200, 100]])
                            self.screen.blit(pygame.font.Font(None, 24).render(self.answer, True, (0, 0, 0)), (7, 590))
                    elif self.button_rect_blue.collidepoint(event.pos):
                        self.save.data["theme"] = [4]
                        self.save.write(self.save.data, 'users.json')
                        self.screen.fill((152, 255, 255))
                        gui_tools.fill = (51, 153, 203)
                        self.square_fill = (51, 153, 203)
                        if self.answer != "":
                            self.screen.fill((255, 255, 255), [[5, 587], [1200, 100]])
                            self.screen.blit(pygame.font.Font(None, 24).render(self.answer, True, (0, 0, 0)), (7, 590))
            gui_tools.drawing(button_rect_start, button_rect_stop, button_rect_delay, self.is_delay, delta_time)
            pygame.display.flip()

    def draw_text(self, surface, text, pos, color=(0, 0, 0)):
        font_size = 24
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    def pressed_keys(self, e):
        if len(e.name) == 1 or e.name == "down" or e.name == "up" or e.name == "right" or e.name == "left":
            self.new_char = e.name
        elif e.name == "backspace":
            self.new_char = ""
            self.grid[self.position[0]][self.position[1]] = None
