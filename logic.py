import random
import pygame
import keyboard
import sys


class GameLogic:
    def __init__(self, grid, screen):
        self.stack = []
        self.signs = [">", "<", "^", "v", "_", "|", "?", "#", "@", ":", "\\", "$", "p", "g", "0", "1", "2", "3", "4",
                      "5", "6", "7", "8", "9", "\"", "+", "-", "*", "/", "%", "!", "`", ".", ","]
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

    def translate(self):
        button_rect_stop = pygame.Rect(1116, 20, 40, 24)
        while not self.ready:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_stop.collidepoint(event.pos):
                        self.ready = True
                        break
            if not self.ready:
                self.next_move(button_rect_stop)
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

    def next_move(self, button_rect_stop):
        if not button_rect_stop.collidepoint(pygame.mouse.get_pos()):
            self.screen.fill((203, 203, 203), pygame.Rect(1117, 21, 38, 22))
        else:
            self.screen.fill((255, 10, 30), pygame.Rect(1117, 21, 38, 22))
        self.screen.blit(pygame.font.Font(None, 24).render("Stop", True, (0, 0, 0)), (1118, 24))
        if self.grid[self.position[0]][self.position[1]] == "\"":
            self.add_now = not self.add_now
        elif self.add_now:
            if self.grid[self.position[0]][self.position[1]] is None:
                self.stack.append(" ")
            else:
                self.stack.append(self.grid[self.position[0]][self.position[1]])
        elif self.grid[self.position[0]][self.position[1]] is not None:
            if self.grid[self.position[0]][self.position[1]] == ">":
                self.vector = [1, 0]
            elif self.grid[self.position[0]][self.position[1]] == "<":
                self.vector = [-1, 0]
            elif self.grid[self.position[0]][self.position[1]] == "^":
                self.vector = [0, -1]
            elif self.grid[self.position[0]][self.position[1]] == "v":
                self.vector = [0, 1]
            elif self.grid[self.position[0]][self.position[1]] == "_":
                if len(self.stack) == 0:
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" В стеке нет элементов."
                    self.ready = True
                elif self.pop() == 0:
                    self.vector = [1, 0]
                else:
                    self.vector = [-1, 0]
            elif self.grid[self.position[0]][self.position[1]] == "|":
                if len(self.stack) == 0:
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" В стеке нет элементов."
                    self.ready = True
                elif self.pop() == 0:
                    self.vector = [0, 1]
                else:
                    self.vector = [0, -1]
            elif self.grid[self.position[0]][self.position[1]] == "?":
                choose = random.randint(1, 4)
                if choose == 1:
                    self.vector = [1, 0]
                elif choose == 2:
                    self.vector = [-1, 0]
                elif choose == 3:
                    self.vector = [0, 1]
                else:
                    self.vector = [0, -1]
            elif self.grid[self.position[0]][self.position[1]] == "#":
                for i in range(2):
                    self.position[i] += self.vector[i]
                self.position[0] %= 80
                self.position[1] %= 25
            elif self.grid[self.position[0]][self.position[1]] == "@":
                self.ready = True
            elif self.grid[self.position[0]][self.position[1]] == ":":
                self.stack.append(self.stack[-1])
            elif self.grid[self.position[0]][self.position[1]] == "\\":
                if len(self.stack) < 2:
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" В стеке меньше 2 элементов."
                    self.ready = True
                else:
                    self.stack.insert(len(self.stack) - 2, str(self.pop()))
            elif self.grid[self.position[0]][self.position[1]] == "$":
                self.stack.pop(-1)
            elif self.grid[self.position[0]][self.position[1]] == "p":
                if len(self.stack) < 3 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit() or \
                        not self.stack[-3].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Невозможно выполнить извлечение трёх чисел из вершины стека."
                    self.ready = True
                else:
                    last = self.pop()
                    pre_last = self.pop()
                    self.grid[pre_last][last] = chr(self.pop())
            elif self.grid[self.position[0]][self.position[1]] == "g":
                if len(self.stack) < 2 or not self.stack[-2].isdigit() or not self.stack[-1].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Некорректные входные данные."
                    self.ready = True
                else:
                    last = self.pop()
                    self.stack.append(str(ord(self.grid[self.pop()][last])))
            elif self.grid[self.position[0]][self.position[1]].isdigit():
                self.stack.append(self.grid[self.position[0]][self.position[1]])
            elif self.grid[self.position[0]][self.position[1]] == "+":
                if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Невозможно выполнить извлечение двух чисел из вершины стека."
                    self.ready = True
                else:
                    self.stack.append(str(self.pop() + self.pop()))
            elif self.grid[self.position[0]][self.position[1]] == "-":
                if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Невозможно выполнить извлечение двух чисел из вершины стека."
                    self.ready = True
                else:
                    last = self.pop()
                    self.stack.append(str(self.pop() - last))
            elif self.grid[self.position[0]][self.position[1]] == "*":
                if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Невозможно выполнить извлечение двух чисел из вершины стека."
                    self.ready = True
                else:
                    self.stack.append(str(self.pop() * self.pop()))
            elif self.grid[self.position[0]][self.position[1]] == "/":
                if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Невозможно выполнить извлечение двух чисел из вершины стека."
                    self.ready = True
                else:
                    last = self.pop()
                    self.stack.append(str(self.pop() // last))
            elif self.grid[self.position[0]][self.position[1]] == "%":
                if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Невозможно выполнить извлечение двух чисел из вершины стека."
                    self.ready = True
                else:
                    last = self.pop()
                    self.stack.append(str(self.pop() % last))
            elif self.grid[self.position[0]][self.position[1]] == "!":
                if len(self.stack) < 1 or not self.stack[-1].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" В стеке нет элементов."
                    self.ready = True
                else:
                    if self.pop() == 0:
                        self.stack.append("1")
                    else:
                        self.stack.append("0")
            elif self.grid[self.position[0]][self.position[1]] == "`":
                if len(self.stack) < 2 or not self.stack[-1].isdigit() or not self.stack[-2].isdigit():
                    self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                                  f" Невозможно выполнить извлечение двух чисел из вершины стека."
                    self.ready = True
                else:
                    if self.stack[-2] > self.stack[-1]:
                        self.stack.append("1")
                    else:
                        self.stack.append("0")
            elif self.grid[self.position[0]][self.position[1]] == "&":
                need_number = True
                write_rect = pygame.Rect(5, 170, 150, 24)
                while need_number:
                    self.screen.fill((255, 255, 255), write_rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), write_rect, 1)
                    if self.input == "":
                        self.screen.blit(pygame.font.Font(None, 24).render("Введите число", True, (0, 0, 0)),
                                         (7, 173))
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and self.can_write:
                            keyboard.hook(self.pressed_keys)
                            if self.new_char == "enter" and self.can_write:
                                self.screen.fill((85, 101, 102), write_rect)
                                self.stack.append(self.input)
                                self.input = ""
                                pygame.display.flip()
                                need_number = False
                                break
                            elif len(self.new_char) == 1 and self.can_write and self.new_char.isdigit() and \
                                    len(self.input) < 12:
                                self.input += self.new_char
                            self.can_write = False
                        elif event.type == pygame.KEYUP:
                            self.can_write = True
            elif self.grid[self.position[0]][self.position[1]] == "~":
                need_char = True
                write_rect = pygame.Rect(5, 170, 150, 24)
                while need_char:
                    self.screen.fill((255, 255, 255), write_rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), write_rect, 1)
                    if self.input == "":
                        self.screen.blit(pygame.font.Font(None, 24).render("Введите символ", True, (0, 0, 0)),
                                         (7, 173))
                    else:
                        self.screen.blit(pygame.font.Font(None, 24).render(self.input, True, (0, 0, 0)),
                                         (7, 173))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and self.can_write:
                            keyboard.hook(self.pressed_keys)
                            if self.new_char == "enter" and self.can_write:
                                self.screen.fill((85, 101, 102), write_rect)
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
            elif self.grid[self.position[0]][self.position[1]] == ".":
                if self.stack[-1].isdigit():
                    self.result += str(self.pop())
                else:
                    self.result += str(ord(self.pop()))
            elif self.grid[self.position[0]][self.position[1]] == ",":
                if self.stack[-1].isdigit():
                    self.result += chr(self.pop())
                else:
                    self.result += self.pop()
            else:
                self.result = f"Ошибка в поле по индексу {self.position[0], self.position[1]}." \
                              f" Неверный синтаксис."
                self.ready = True
        for i in range(2):
            self.position[i] += self.vector[i]
        self.position[0] %= 80
        self.position[1] %= 25
