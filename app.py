import pygame
from IDE import BefungeIDE
from logic import GameLogic
from save import SavingSystem


class Befunge:
    def __init__(self):
        self.start()

    def start(self):
        pygame.init()
        pygame.display.set_caption('BCharm')
        save = SavingSystem()
        bi = BefungeIDE(save)
        while True:
            bi.code_loop()
            logic = GameLogic(bi.grid, bi.screen, bi.square_fill)
            logic.translate()
            bi.answer = logic.result
