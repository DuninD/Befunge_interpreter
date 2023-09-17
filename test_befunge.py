import unittest
from logic import GameLogic
from unittest.mock import Mock, patch


class Tests(unittest.TestCase):
    def test_key_logic(self):
        gl = GameLogic(None, None, None)
        mock_event = Mock()
        mock_event.name = 'W'
        gl.pressed_keys(mock_event)
        self.assertEqual(gl.new_char, 'W')

    def test_pop_isdigit(self):
        gl = GameLogic(None, None, None)
        gl.stack = ["5"]
        result = gl.pop()
        self.assertEqual(result, 5)
        self.assertEqual([], gl.stack)

    def test_pop_not_isdigit(self):
        gl = GameLogic(None, None, None)
        gl.stack = ["x", "c", "b"]
        result = gl.pop()
        self.assertEqual(result, "b")
        self.assertEqual(["x", "c"], gl.stack)

    def test_move_right(self):
        gl = GameLogic(None, None, None)
        gl.move_right()
        self.assertEqual([1, 0], gl.vector)

    def test_move_left(self):
        gl = GameLogic(None, None, None)
        gl.move_left()
        self.assertEqual([-1, 0], gl.vector)

    def test_move_up(self):
        gl = GameLogic(None, None, None)
        gl.move_up()
        self.assertEqual([0, -1], gl.vector)

    def test_move_down(self):
        gl = GameLogic(None, None, None)
        gl.move_down()
        self.assertEqual([0, 1], gl.vector)

    def test_move_right_or_left(self):
        gl = GameLogic(None, None, None)
        gl.stack = ["0", "1"]
        gl.move_right_or_left()
        self.assertEqual([-1, 0], gl.vector)
        gl.move_right_or_left()
        gl.move_right_or_left()
        self.assertEqual([1, 0], gl.vector)
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке нет элементов.", gl.result)

    def test_move_down_or_up(self):
        gl = GameLogic(None, None, None)
        gl.stack = ["0", "1"]
        gl.move_down_or_up()
        self.assertEqual([0, -1], gl.vector)
        gl.move_down_or_up()
        gl.move_down_or_up()
        self.assertEqual([0, 1], gl.vector)
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке нет элементов.", gl.result)

    @patch('random.randint', side_effect=[1, 2, 3, 4])
    def test_move_random(self, _):
        gl = GameLogic(None, None, None)
        gl.move_random()
        self.assertEqual([1, 0], gl.vector)
        gl.move_random()
        self.assertEqual([-1, 0], gl.vector)
        gl.move_random()
        self.assertEqual([0, 1], gl.vector)
        gl.move_random()
        self.assertEqual([0, -1], gl.vector)
        self.assertEqual(_.call_count, 4)

    def test_jump(self):
        gl = GameLogic(None, None, None)
        gl.jump()
        self.assertEqual([1, 0], gl.position)

    def test_end(self):
        gl = GameLogic(None, None, None)
        gl.end()
        self.assertEqual(True, gl.ready)

    def test_copy(self):
        gl = GameLogic(None, None, None)
        gl.copy()
        gl.stack = ["0"]
        gl.copy()
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке нет элементов.", gl.result)
        self.assertEqual(["0", "0"], gl.stack)

    def test_change(self):
        gl = GameLogic(None, None, None)
        gl.change()
        gl.stack = ["0", "1"]
        gl.change()
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке меньше 2 элементов.", gl.result)
        self.assertEqual(["1", "0"], gl.stack)

    def test_delete(self):
        gl = GameLogic(None, None, None)
        gl.delete()
        gl.stack = ["0"]
        gl.delete()
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке нет элементов.", gl.result)
        self.assertEqual([], gl.stack)

    def test_put(self):
        gl = GameLogic(None, None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.put()
        gl.stack = ["d", "1", "0"]
        gl.put()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual("100", gl.grid[1][0])
        self.assertEqual([], gl.stack)

    def test_get(self):
        gl = GameLogic(None, None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.get()
        gl.stack = ["0", "2"]
        gl.grid[0][2] = "a"
        gl.get()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual(["97"], gl.stack)

    def test_add_number_in_stack(self):
        gl = GameLogic(None, None, None)
        gl.grid = [[None for _ in range(25)] for _ in range(80)]
        gl.grid[0][0] = "0"
        gl.add_number_in_stack()
        self.assertEqual(["0"], gl.stack)

    def test_sum(self):
        gl = GameLogic(None, None, None)
        gl.sum()
        gl.stack = ["2", "3"]
        gl.sum()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual(["5"], gl.stack)

    def test_distinct(self):
        gl = GameLogic(None, None, None)
        gl.distinct()
        gl.stack = ["7", "2"]
        gl.distinct()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual(["5"], gl.stack)

    def test_multiply(self):
        gl = GameLogic(None, None, None)
        gl.multiply()
        gl.stack = ["7", "2"]
        gl.multiply()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual(["14"], gl.stack)

    def test_division(self):
        gl = GameLogic(None, None, None)
        gl.division()
        gl.stack = ["7", "2"]
        gl.division()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual(["3"], gl.stack)

    def test_module_division(self):
        gl = GameLogic(None, None, None)
        gl.module_division()
        gl.stack = ["7", "2"]
        gl.module_division()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual(["1"], gl.stack)

    def test_change_to_one_or_zero(self):
        gl = GameLogic(None, None, None)
        gl.change_to_one_or_zero()
        gl.stack = ["0"]
        gl.change_to_one_or_zero()
        self.assertEqual(["1"], gl.stack)
        gl.change_to_one_or_zero()
        self.assertEqual(["0"], gl.stack)
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке нет элементов.", gl.result)

    def test_more_than(self):
        gl = GameLogic(None, None, None)
        gl.more_than()
        gl.stack = ["1", "0"]
        gl.more_than()
        gl.more_than()
        self.assertEqual("Ошибка в поле по индексу (0, 0). Невозможно выполнить извлечение двух чисел из вершины стека."
                         , gl.result)
        self.assertEqual(["1", "0", "1", "0"], gl.stack)

    def test_print_number(self):
        gl = GameLogic(None, None, None)
        gl.print_number()
        gl.stack = ["1", "a"]
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке нет элементов.", gl.result)
        gl.result = ""
        gl.print_number()
        gl.print_number()
        self.assertEqual([], gl.stack)
        self.assertEqual("971", gl.result)

    def test_print_char(self):
        gl = GameLogic(None, None, None)
        gl.print_char()
        gl.stack = ["100", "a"]
        self.assertEqual("Ошибка в поле по индексу (0, 0). В стеке нет элементов.", gl.result)
        gl.result = ""
        gl.print_char()
        gl.print_char()
        self.assertEqual([], gl.stack)
        self.assertEqual("ad", gl.result)
