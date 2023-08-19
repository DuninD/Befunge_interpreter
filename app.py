import pygame
from IDE import BefungeIDE
from logic import GameLogic
from save import SavingSystem
from savingGUI import SaveLogic
from library import PullCode


class Befunge:
    def __init__(self):
        self.start()

    def start(self):
        pygame.init()
        pygame.display.set_caption('BCharm')
        save = SavingSystem()
        bi = BefungeIDE(save)
        while True:
            if bi.write_code:
                bi.new_char = ""
                bi.code_loop()
            elif bi.read_code:
                logic = GameLogic(bi.grid, bi.screen, bi.square_fill, bi.square_fill)
                logic.translate()
                bi.answer = logic.result
                bi.read_code = False
                bi.write_code = True
            elif bi.add_new:
                add = SaveLogic(bi.screen, save, bi.grid)
                add.saving_cycle()
                bi.add_new = False
                bi.write_code = True
            elif bi.is_library:
                library = PullCode(bi.screen, save)
                library.choose_code()
                bi.write_code = True
                bi.is_library = False
                if library.grid is not None:
                    bi.grid = library.grid
