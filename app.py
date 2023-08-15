import pygame
from IDE import BefungeIDE
from logic import GameLogic


class Befunge:
    def __init__(self):
        self.start()

    def start(self):
        pygame.init()
        pygame.display.set_caption('BCharm')
        bi = BefungeIDE()
        while True:
            bi.code_loop()
            logic = GameLogic(bi.grid, bi.screen)
            logic.translate()
