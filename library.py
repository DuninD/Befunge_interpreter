import pygame
import sys


class PullCode:
    def __init__(self, screen, save):
        self.grid = None
        self.screen = screen
        self.save = save
        if save.data["theme"] == [1]:
            self.fill = (85, 101, 102)
        elif save.data["theme"] == [2]:
            self.fill = (137, 9, 137)
        elif save.data["theme"] == [3]:
            self.fill = (0, 51, 0)
        else:
            self.fill = (152, 255, 255)

    def choose_code(self):
        ready = False
        button_rect_save = pygame.Rect(585, 20, 90, 24)
        while not ready:
            self.screen.fill(self.fill, [[0, 45], [2000, 100]])
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect_save, 1)
            if not button_rect_save.collidepoint(pygame.mouse.get_pos()):
                self.screen.fill((203, 203, 203), pygame.Rect(586, 21, 88, 22))
            else:
                self.screen.fill((162, 162, 162), pygame.Rect(586, 21, 88, 22))
            self.draw_text(self.screen, "Назад", (605, 24))
            for i in range(0, len(self.save.data) - 1):
                option_rect = pygame.Rect(5 + (i % 7) * 175, 50 + (i // 7) * 29, 150, 24)
                if not option_rect.collidepoint(pygame.mouse.get_pos()):
                    self.screen.fill((203, 203, 203), pygame.Rect(6 + (i % 7) * 175, 51 + (i // 7) * 29, 148, 22))
                else:
                    self.screen.fill((162, 162, 162), pygame.Rect(6 + (i % 7) * 175, 51 + (i // 7) * 29, 148, 22))
                pygame.draw.rect(self.screen, (0, 0, 0), option_rect, 1)
                self.draw_text(self.screen, list(self.save.data.keys())[i + 1], (7 + (i % 7) * 175,
                                                                                 53 + (i // 7) * 29, 150, 24))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_save.collidepoint(event.pos):
                        ready = True
                        self.screen.fill(self.fill, [[0, 45], [2000, 100]])
                        break
                    else:
                        for i in range(0, len(self.save.data) - 1):
                            option_rect = pygame.Rect(5 + (i % 7) * 175, 50 + (i // 7) * 29, 150, 24)
                            if option_rect.collidepoint(event.pos):
                                self.save.data = self.save.read('users.json')
                                self.grid = list(self.save.data.values())[i + 1]
                                self.screen.fill(self.fill, [[0, 45], [2000, 100]])
                                ready = True
                                break

    def draw_text(self, surface, text, pos, color=(0, 0, 0)):
        font_size = 24
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)
