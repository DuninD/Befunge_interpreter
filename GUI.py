import pygame
import datetime


class Draw:
    def __init__(self, IDE, fill):
        self.IDE = IDE
        self.fill = fill
        self.button_rect_blue = pygame.Rect(5, 20, 50, 24)
        self.button_rect_gray = pygame.Rect(65, 20, 50, 24)
        self.button_rect_purple = pygame.Rect(125, 20, 50, 24)
        self.button_rect_green = pygame.Rect(185, 20, 50, 24)
        self.button_rect_save = pygame.Rect(490, 20, 90, 24)
        self.button_rect_library = pygame.Rect(585, 20, 90, 24)

    def drawing(self, button_rect_start, button_rect_stop, delta_time):
        self.IDE.screen.fill((255, 255, 255), [[5, 200], [1200, 375]])
        self.IDE.draw_lines()
        pygame.draw.rect(self.IDE.screen, (21, 210, 45), button_rect_start, 1)
        pygame.draw.rect(self.IDE.screen, (255, 0, 0), button_rect_stop, 1)
        pygame.draw.rect(self.IDE.screen, (0, 0, 0), self.button_rect_blue, 1)
        pygame.draw.rect(self.IDE.screen, (0, 0, 0), self.button_rect_green, 1)
        pygame.draw.rect(self.IDE.screen, (0, 0, 0), self.button_rect_purple, 1)
        pygame.draw.rect(self.IDE.screen, (0, 0, 0), self.button_rect_gray, 1)
        pygame.draw.rect(self.IDE.screen, (0, 0, 0), self.button_rect_library, 1)
        pygame.draw.rect(self.IDE.screen, (0, 0, 0), self.button_rect_save, 1)
        if not button_rect_start.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(1067, 21, 38, 22))
        else:
            self.IDE.screen.fill((0, 210, 111), pygame.Rect(1067, 21, 38, 22))
        if not self.button_rect_save.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(491, 21, 88, 22))
        else:
            self.IDE.screen.fill((162, 162, 162), pygame.Rect(491, 21, 88, 22))
        if not button_rect_stop.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(1117, 21, 38, 22))
        else:
            self.IDE.screen.fill((255, 10, 30), pygame.Rect(1117, 21, 38, 22))
        if not self.button_rect_gray.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(66, 21, 48, 22))
        else:
            self.IDE.screen.fill((162, 162, 162), pygame.Rect(66, 21, 48, 22))
        if not self.button_rect_library.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(586, 21, 88, 22))
        else:
            self.IDE.screen.fill((162, 162, 162), pygame.Rect(586, 21, 88, 22))
        if not self.button_rect_purple.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(126, 21, 48, 22))
        else:
            self.IDE.screen.fill((162, 162, 162), pygame.Rect(126, 21, 48, 22))
        if not self.button_rect_green.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(186, 21, 48, 22))
        else:
            self.IDE.screen.fill((162, 162, 162), pygame.Rect(186, 21, 48, 22))
        if not self.button_rect_blue.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(6, 21, 48, 22))
        else:
            self.IDE.screen.fill((162, 162, 162), pygame.Rect(6, 21, 48, 22))
        if delta_time < 500000:
            self.IDE.screen.fill(self.fill, [[5 + self.IDE.position[0] * self.IDE.grid_size + 1,
                                                    200 + self.IDE.position[1] * self.IDE.grid_size + 1], [14, 14]])
        if len(self.IDE.new_char) == 1:
            self.IDE.grid[self.IDE.position[0]][self.IDE.position[1]] = self.IDE.new_char
        elif self.IDE.can_move:
            if self.IDE.new_char == "down":
                self.IDE.position[1] = (self.IDE.position[1] + 1) % 25
                self.IDE.timer = datetime.datetime.today()
            elif self.IDE.new_char == "up":
                self.IDE.position[1] = (self.IDE.position[1] - 1) % 25
                self.IDE.timer = datetime.datetime.today()
            elif self.IDE.new_char == "right":
                self.IDE.position[0] = (self.IDE.position[0] + 1) % 80
                self.IDE.timer = datetime.datetime.today()
            elif self.IDE.new_char == "left":
                self.IDE.position[0] = (self.IDE.position[0] - 1) % 80
                self.IDE.timer = datetime.datetime.today()
        for i in range(80):
            for j in range(25):
                if self.IDE.grid[i][j] is not None:
                    self.IDE.draw_text(self.IDE.screen, self.IDE.grid[i][j], (5 + i * self.IDE.grid_size + 3,
                                                                              200 + j * self.IDE.grid_size + 1))
        self.IDE.can_move = False
        self.IDE.draw_text(self.IDE.screen, "Run", (1070, 24))
        self.IDE.draw_text(self.IDE.screen, "Stop", (1118, 24))
        self.IDE.draw_text(self.IDE.screen, "Blue", (11, 24))
        self.IDE.draw_text(self.IDE.screen, "Gray", (70, 24))
        self.IDE.draw_text(self.IDE.screen, "Violet", (128, 24))
        self.IDE.draw_text(self.IDE.screen, "Green", (187, 24))
        self.IDE.draw_text(self.IDE.screen, "Сохранить", (492, 24))
        self.IDE.draw_text(self.IDE.screen, "Загрузить", (590, 24))
