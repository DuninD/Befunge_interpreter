import random
import pygame
import keyboard
import sys


class GameLogic:
    def __init__(self, grid, screen, fill, save):
        self.stack = []
        self.add_now = False
        self.vector = [1, 0]
        self.position = [0, 0]
        self.grid = grid
        self.result = ""
        self.can_write = True
        self.input = ""
        self.new_char = ""
        self.screen = screen
        self.ready = False
        self.fill = fill
        self.action_dict = {">": self.move_right, "<": self.move_left, "^": self.move_up, "v": self.move_down, "_":
                            self.move_right_or_left, "|": self.move_down_or_up, "?": self.move_random, "#": self.jump,
                            "@": self.end, ":": self.copy, "\\": self.change, "$": self.delete, "p": self.put, "g":
                            self.get, "0": self.add_number_in_stack, "1": self.add_number_in_stack, "2":
                            self.add_number_in_stack, "3": self.add_number_in_stack, "4": self.add_number_in_stack, "5":
                            self.add_number_in_stack, "6": self.add_number_in_stack, "7": self.add_number_in_stack, "8":
                            self.add_number_in_stack, "9": self.add_number_in_stack, "+": self.sum, "-": self.distinct,
                            "*": self.multiply, "/": self.division, "%": self.module_division, "!":
                            self.change_to_one_or_zero, "`": self.more_than, "&": self.write_number, "~":
                            self.write_char, ".": self.print_number, ",": self.print_char}
        if save.data["theme"] == [1]:
            self.fill_screen = (85, 101, 102)
        elif save.data["theme"] == [2]:
            self.fill_screen = (137, 9, 137)
        elif save.data["theme"] == [3]:
            self.fill_screen = (0, 51, 0)
        else:
            self.fill_screen = (152, 255, 255)

    def translate(self, is_delay):
        button_rect_stop = pygame.Rect(1116, 20, 40, 24)
        while not self.ready:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and self.can_write:
                    keyboard.hook(self.pressed_keys)
                    self.can_write = False
                elif event.type == pygame.KEYUP:
                    self.can_write = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_stop.collidepoint(event.pos):
                        self.ready = True
                        break
            if not self.ready:
                if not button_rect_stop.collidepoint(pygame.mouse.get_pos()):
                    self.screen.fill((203, 203, 203), pygame.Rect(1117, 21, 38, 22))
                else:
                    self.screen.fill((255, 10, 30), pygame.Rect(1117, 21, 38, 22))
                self.screen.blit(pygame.font.Font(None, 24).render("Stop", True, (0, 0, 0)), (1118, 24))
                if (is_delay and self.new_char == "space" and self.can_write) or not is_delay:
                    self.can_write = False
                    self.new_char = ""
                    self.next_move()
                    self.screen.fill((255, 255, 255), [[5, 587], [1200, 100]])
                    self.screen.blit(pygame.font.Font(None, 24).render(self.result, True, (0, 0, 0)), (7, 590))
            pygame.display.flip()

    def pop(self):
        result = self.stack[-1]
        self.stack.pop(-1)
        if result.isdigit():
            return int(result)
        else:
            return result

    def pressed_keys(self, e):
        self.new_char = e.name

    def next_move(self):
        if self.grid[self.position[0]][self.position[1]] == "\"":
            self.add_now = not self.add_now
        elif self.add_now:
            if self.grid[self.position[0]][self.position[1]] is None:
                self.stack.append(" ")
            else:
                self.stack.append(self.grid[self.position[0]][self.position[1]])
        elif self.grid[self.position[0]][self.position[1]] is not None:
            try:
                self.action_dict[self.grid[self.position[0]][self.position[1]]]()
            except KeyError:
                self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                              f" Неверный синтаксис."
                self.ready = True
        self.screen.fill((255, 255, 255), [[5 + self.position[0] * 15 + 1, 200 + self.position[1] * 15 + 1], [14, 14]])
        self.draw_text(self.screen, self.grid[self.position[0]][self.position[1]], (5 + self.position[0] * 15 + 3,
                                                                                    200 + self.position[1] * 15 + 1))
        for i in range(2):
            self.position[i] += self.vector[i]
        self.position[0] %= 80
        self.position[1] %= 25
        self.screen.fill(self.fill, [[5 + self.position[0] * 15 + 1, 200 + self.position[1] * 15 + 1], [14, 14]])
        self.draw_text(self.screen, self.grid[self.position[0]][self.position[1]], (5 + self.position[0] * 15 + 3,
                                                                                    200 + self.position[1] * 15 + 1))

    def draw_text(self, surface, text, pos, color=(0, 0, 0)):
        font_size = 24
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    def move_right(self):
        self.vector = [1, 0]

    def move_left(self):
        self.vector = [-1, 0]

    def move_up(self):
        self.vector = [0, -1]

    def move_down(self):
        self.vector = [0, 1]

    def move_right_or_left(self):
        if len(self.stack) == 0:
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" В стеке нет элементов."
            self.ready = True
        elif str(self.pop()) == "0":
            self.vector = [1, 0]
        else:
            self.vector = [-1, 0]

    def move_down_or_up(self):
        if len(self.stack) == 0:
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" В стеке нет элементов."
            self.ready = True
        elif self.pop() == 0:
            self.vector = [0, 1]
        else:
            self.vector = [0, -1]

    def move_random(self):
        choose = random.randint(1, 4)
        if choose == 1:
            self.vector = [1, 0]
        elif choose == 2:
            self.vector = [-1, 0]
        elif choose == 3:
            self.vector = [0, 1]
        else:
            self.vector = [0, -1]

    def jump(self):
        for i in range(2):
            self.position[i] += self.vector[i]
        self.position[0] %= 80
        self.position[1] %= 25

    def end(self):
        self.ready = True

    def copy(self):
        if len(self.stack) == 0:
            self.stack = ["0", "0"]
        else:
            self.stack.append(self.stack[-1])

    def change(self):
        if len(self.stack) < 2:
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" В стеке меньше 2 элементов."
            self.ready = True
        else:
            self.stack.insert(len(self.stack) - 2, str(self.pop()))

    def delete(self):
        if len(self.stack) == 0:
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" В стеке нет элементов."
            self.ready = True
        else:
            self.stack.pop(-1)

    def put(self):
        if len(self.stack) < 3 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            last = self.pop()
            pre_last = self.pop()
            self.grid[pre_last][last] = str(ord(self.pop()))

    def get(self):
        if len(self.stack) < 2 or not self.stack[-2].isdigit() or not self.stack[-1].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            last = self.pop()
            pre_last = self.pop()
            if self.grid[pre_last][last] is None:
                self.stack.append("32")
            else:
                self.stack.append(str(ord(self.grid[pre_last][last])))

    def add_number_in_stack(self):
        self.stack.append(self.grid[self.position[0]][self.position[1]])

    def sum(self):
        if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            self.stack.append(str(self.pop() + self.pop()))

    def distinct(self):
        if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            last = self.pop()
            self.stack.append(str(self.pop() - last))

    def multiply(self):
        if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            self.stack.append(str(self.pop() * self.pop()))

    def division(self):
        if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            last = self.pop()
            self.stack.append(str(self.pop() // last))

    def module_division(self):
        if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            last = self.pop()
            self.stack.append(str(self.pop() % last))

    def change_to_one_or_zero(self):
        if len(self.stack) < 1:
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" В стеке нет элементов."
            self.ready = True
        else:
            if self.pop() == 0:
                self.stack.append("1")
            else:
                self.stack.append("0")

    def more_than(self):
        if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" Невозможно выполнить извлечение двух чисел из вершины стека."
            self.ready = True
        else:
            if self.stack[-2] > self.stack[-1]:
                self.stack.append("1")
            else:
                self.stack.append("0")

    def write_number(self):
        need_number = True
        write_rect = pygame.Rect(5, 170, 150, 24)
        while need_number:
            self.screen.fill((255, 255, 255), write_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), write_rect, 1)
            if self.input == "":
                self.screen.blit(pygame.font.Font(None, 24).render("Введите число", True, (0, 0, 0)), (7, 173))
            else:
                self.screen.blit(pygame.font.Font(None, 24).render(self.input, True, (0, 0, 0)), (7, 173))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and self.can_write:
                    keyboard.hook(self.pressed_keys)
                    if self.new_char == "enter" and self.can_write:
                        self.screen.fill(self.fill_screen, write_rect)
                        self.stack.append(self.input)
                        self.input = ""
                        pygame.display.flip()
                        need_number = False
                        break
                    elif len(self.new_char) == 1 and self.can_write and self.new_char.isdigit() and \
                            len(self.input) < 12:
                        self.input += self.new_char
                    elif self.new_char == "backspace":
                        self.input = self.input[:-1]
                    self.can_write = False
                elif event.type == pygame.KEYUP:
                    self.can_write = True

    def write_char(self):
        need_char = True
        write_rect = pygame.Rect(5, 170, 150, 24)
        while need_char:
            self.screen.fill((255, 255, 255), write_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), write_rect, 1)
            if self.input == "":
                self.screen.blit(pygame.font.Font(None, 24).render("Введите символ", True, (0, 0, 0)), (7, 173))
            else:
                self.screen.blit(pygame.font.Font(None, 24).render(self.input, True, (0, 0, 0)), (7, 173))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and self.can_write:
                    keyboard.hook(self.pressed_keys)
                    if self.new_char == "enter" and self.can_write:
                        self.screen.fill(self.fill_screen, write_rect)
                        self.stack.append(self.input)
                        self.input = ""
                        pygame.display.flip()
                        need_char = False
                        break
                    elif len(self.new_char) == 1 and self.can_write:
                        self.input = self.new_char
                    self.can_write = False
                elif event.type == pygame.KEYUP:
                    self.can_write = True

    def print_number(self):
        if len(self.stack) == 0:
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" В стеке нет элементов."
            self.ready = True
        elif self.stack[-1].isdigit():
            self.result += str(self.pop())
        else:
            self.result += str(ord(self.pop()))

    def print_char(self):
        if len(self.stack) == 0:
            self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                          f" В стеке нет элементов."
            self.ready = True
        elif self.stack[-1].isdigit():
            self.result += str(chr(self.pop()))
        else:
            self.result += self.pop()
