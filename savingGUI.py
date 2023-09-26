import pygame
import keyboard
import sys


class SaveLogic:
    def __init__(self, screen, save, grid):
        self.screen = screen
        self.new_char = ""
        self.name = ""
        save.data = save.read('users.json')
        self.save = save
        self.can_write = True
        self.can_add = True
        self.grid = grid
        if save.data["theme"] == [1]:
            self.fill = (85, 101, 102)
        elif save.data["theme"] == [2]:
            self.fill = (137, 9, 137)
        elif save.data["theme"] == [3]:
            self.fill = (0, 51, 0)
        else:
            self.fill = (152, 255, 255)

    def saving_cycle(self):
        ready = False
        write_rect = pygame.Rect(510, 170, 150, 24)
        button_rect_save = pygame.Rect(490, 20, 90, 24)
        while not ready:
            self.screen.fill(self.fill, [[490, 115], [300, 85]])
            self.screen.fill((255, 255, 255), write_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect_save, 1)
            if not button_rect_save.collidepoint(pygame.mouse.get_pos()):
                self.screen.fill((203, 203, 203), pygame.Rect(491, 21, 88, 22))
            else:
                self.screen.fill((162, 162, 162), pygame.Rect(491, 21, 88, 22))
            self.draw_text(self.screen, "Назад", (510, 24))
            pygame.draw.rect(self.screen, (0, 0, 0), write_rect, 1)
            if self.name == "":
                self.screen.blit(pygame.font.Font(None, 24).render("Введите название", True, (0, 0, 0)), (511, 173))
            else:
                self.screen.blit(pygame.font.Font(None, 24).render(self.name, True, (0, 0, 0)), (512, 173))
            self.can_add = True
            if self.name in self.save.data:
                self.screen.blit(pygame.font.Font(None, 24).render("недопустимое имя", True, (0, 0, 0)), (509, 150))
                self.can_add = False
            elif len(self.name) == 13:
                self.screen.blit(pygame.font.Font(None, 24).render("макс кол-во символов", True, (0, 0, 0)), (495, 150))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                        button_rect_save.collidepoint(event.pos):
                    ready = True
                    self.screen.fill(self.fill, [[490, 115], [300, 85]])
                    break
                elif event.type == pygame.KEYDOWN and self.can_write:
                    keyboard.hook(self.pressed_keys)
                    if self.new_char == "enter" and self.can_write:
                        pygame.display.flip()
                        self.save.data[self.name] = self.grid
                        self.save.write(self.save.data, 'users.json')
                        self.screen.fill(self.fill, [[490, 115], [300, 85]])
                        ready = True
                        break
                    elif self.new_char == "backspace":
                        self.name = self.name[:-1]
                    elif len(self.new_char) == 1 and self.can_write and len(self.name) < 13:
                        self.name += self.new_char
                    self.can_write = False
                elif event.type == pygame.KEYUP:
                    self.can_write = True

    def draw_text(self, surface, text, pos, color=(0, 0, 0)):
        font_size = 24
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    def pressed_keys(self, e):
        self.new_char = e.name
