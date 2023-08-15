import unittest
from logic import GameLogic
from unittest.mock import Mock, patch


class Tests(unittest.TestCase):
    def test_key_logic(self):
        gl = GameLogic(None, None)
        mock_event = Mock()
        mock_event.name = 'W'
        gl.pressed_keys(mock_event)
        self.assertEqual(gl.new_char, 'W')

    def test_pop_isdigit(self):
        gl = GameLogic(None, None)
        gl.stack = ["5"]
        result = gl.pop()
        self.assertEqual(result, 5)
        self.assertEqual([], gl.stack)

    def test_pop_not_isdigit(self):
        gl = GameLogic(None, None)
        gl.stack = ["x", "c", "b"]
        result = gl.pop()
        self.assertEqual(result, "b")
        self.assertEqual(["x", "c"], gl.stack)

    @patch('random.randint', side_effect=[1, 2, 3, 4])
    def test_logic_movement(self, _):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = ["1", "0", "1", "0"]
        gl.grid[0][0] = ">"
        gl.grid[1][0] = "_"
        gl.grid[1][3] = ">"
        gl.grid[1][2] = "|"
        gl.grid[2][2] = ">"
        gl.grid[2][3] = "|"
        gl.grid[1][1] = "v"
        gl.grid[2][1] = "_"
        gl.grid[3][1] = ">"
        gl.grid[3][2] = "^"
        gl.grid[6][1] = "#"
        gl.grid[7][1] = "^"
        gl.grid[8][1] = "?"
        gl.grid[8][2] = ">"
        gl.grid[2][0] = "v"
        gl.grid[5][0] = "v"
        gl.grid[5][2] = ">"
        gl.grid[10][0] = "@"
        gl.grid[10][2] = "^"
        gl.grid[10][1] = "^"
        gl.grid[7][0] = "<"
        gl.grid[8][0] = "<"
        gl.translate()
        gl.position = [8, 1]
        gl.ready = False
        gl.translate()
        gl.position = [8, 1]
        gl.ready = False
        gl.translate()
        gl.position = [8, 1]
        gl.ready = False
        gl.translate()
        self.assertEqual([], gl.stack)
        self.assertEqual(_.call_count, 4)

    def test_logic_stack(self):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = ["1", "0"]
        gl.grid[0][0] = ">"
        gl.grid[1][0] = ":"
        gl.grid[2][0] = "$"
        gl.grid[4][0] = "@"
        gl.grid[3][0] = "\\"
        gl.translate()
        self.assertEqual(["0",  "1"], gl.stack)

    def test_logic_code(self):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = ["0", "0", "100", "1", "1"]
        gl.grid[0][0] = ">"
        gl.grid[1][0] = "p"
        gl.grid[2][0] = "g"
        gl.grid[3][0] = "@"
        gl.translate()
        self.assertEqual(["62"], gl.stack)
        self.assertEqual(gl.grid[1][1], "d")

    def test_logic_const(self):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = []
        gl.grid[0][0] = ">"
        gl.grid[1][0] = "\""
        gl.grid[2][0] = "a"
        gl.grid[3][0] = "\""
        gl.grid[4][0] = "0"
        gl.grid[5][0] = "1"
        gl.grid[6][0] = "2"
        gl.grid[7][0] = "3"
        gl.grid[8][0] = "4"
        gl.grid[9][0] = "5"
        gl.grid[10][0] = "6"
        gl.grid[11][0] = "7"
        gl.grid[12][0] = "8"
        gl.grid[13][0] = "9"
        gl.grid[14][0] = "@"
        gl.translate()
        self.assertEqual(["a", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], gl.stack)

    def test_logic_bool(self):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = ["2", "1"]
        gl.grid[0][0] = ">"
        gl.grid[1][0] = "!"
        gl.grid[2][0] = "!"
        gl.grid[3][0] = "`"
        gl.grid[4][0] = "`"
        gl.grid[5][0] = "@"
        gl.translate()
        self.assertEqual(["2", "1", "1", "0"], gl.stack)

    def test_logic_operations(self):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = ["3", "51", "5", "20", "7", "8"]
        gl.grid[0][0] = ">"
        gl.grid[1][0] = "+"
        gl.grid[2][0] = "-"
        gl.grid[3][0] = "*"
        gl.grid[4][0] = "/"
        gl.grid[5][0] = "%"
        gl.grid[6][0] = "@"
        gl.translate()
        self.assertEqual(["1"], gl.stack)

    def test_logic_print(self):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = ["97", "a", "0", "a"]
        gl.grid[0][0] = ">"
        gl.grid[1][0] = "."
        gl.grid[2][0] = "."
        gl.grid[3][0] = ","
        gl.grid[4][0] = ","
        gl.grid[5][0] = "@"
        gl.translate()
        self.assertEqual("970aa", gl.result)

    def test_logic_errors(self):
        gl = GameLogic(None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.stack = []
        gl.grid[0][0] = "w"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). Неверный синтаксис.")
        gl.grid[0][0] = "|"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). В стеке нет элементов.")
        gl.grid[0][0] = "_"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). В стеке нет элементов.")
        gl.grid[0][0] = "!"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). В стеке нет элементов.")
        gl.grid[0][0] = "\\"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). В стеке меньше 2 элементов.")
        gl.grid[0][0] = "p"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). "
                                    "Невозможно выполнить извлечение трёх чисел из вершины стека.")
        gl.grid[0][0] = "g"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). Некорректные входные данные.")
        gl.grid[0][0] = "+"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). "
                                    "Невозможно выполнить извлечение двух чисел из вершины стека.")
        gl.grid[0][0] = "-"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). "
                                    "Невозможно выполнить извлечение двух чисел из вершины стека.")
        gl.grid[0][0] = "*"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). "
                                    "Невозможно выполнить извлечение двух чисел из вершины стека.")
        gl.grid[0][0] = "/"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). "
                                    "Невозможно выполнить извлечение двух чисел из вершины стека.")
        gl.grid[0][0] = "%"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). "
                                    "Невозможно выполнить извлечение двух чисел из вершины стека.")
        gl.grid[0][0] = "`"
        gl.position = [0, 0]
        gl.ready = False
        gl.translate()
        self.assertEqual(gl.result, "Ошибка в поле по индексу (0, 0). "
                                    "Невозможно выполнить извлечение двух чисел из вершины стека.")
