import pygame
import datetime


class Draw:
    def __init__(self, IDE):
        self.IDE = IDE

    def drawing(self, button_rect_start, button_rect_stop, delta_time):
        self.IDE.screen.fill((255, 255, 255), [[5, 200], [1200, 375]])
        self.IDE.draw_lines()
        pygame.draw.rect(self.IDE.screen, (21, 210, 45), button_rect_start, 1)
        pygame.draw.rect(self.IDE.screen, (255, 0, 0), button_rect_stop, 1)
        if not button_rect_start.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(1067, 21, 38, 22))
        else:
            self.IDE.screen.fill((0, 210, 111), pygame.Rect(1067, 21, 38, 22))
        if not button_rect_stop.collidepoint(pygame.mouse.get_pos()):
            self.IDE.screen.fill((203, 203, 203), pygame.Rect(1117, 21, 38, 22))
        else:
            self.IDE.screen.fill((255, 10, 30), pygame.Rect(1117, 21, 38, 22))
        if delta_time < 500000:
            self.IDE.screen.fill((203, 203, 203), [[5 + self.IDE.position[0] * self.IDE.grid_size + 1,
                                                    200 + self.IDE.position[1] * self.IDE.grid_size + 1], [14, 14]])
        if len(self.IDE.new_char) == 1:
            self.IDE.grid[self.IDE.position[0]][self.IDE.position[1]] = self.IDE.new_char
        elif self.IDE.can_move:
            if self.IDE.new_char == "down":
                self.IDE.position[1] += 1
                self.IDE.timer = datetime.datetime.today()
            elif self.IDE.new_char == "up":
                self.IDE.position[1] -= 1
                self.IDE.timer = datetime.datetime.today()
            elif self.IDE.new_char == "right":
                self.IDE.position[0] += 1
                self.IDE.timer = datetime.datetime.today()
            elif self.IDE.new_char == "left":
                self.IDE.position[0] -= 1
                self.IDE.timer = datetime.datetime.today()
        for i in range(80):
            for j in range(25):
                if self.IDE.grid[i][j] is not None:
                    self.IDE.draw_text(self.IDE.screen, self.IDE.grid[i][j], (5 + i * self.IDE.grid_size + 3,
                                                                              200 + j * self.IDE.grid_size + 1))
        self.IDE.can_move = False
        self.IDE.draw_text(self.IDE.screen, "Run", (1070, 24))
        self.IDE.draw_text(self.IDE.screen, "Stop", (1118, 24))
