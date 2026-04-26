import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to the path so we can import minesweeper
sys.path.insert(0, os.path.dirname(__file__))

from minesweeper import Minefield, Generator, Game, Player, UI, FileManager


class TestMinefield(unittest.TestCase):
    def setUp(self):
        self.minefield = Minefield(5, 5)

    def test_initialization(self):
        self.assertEqual(self.minefield._rows, 5)
        self.assertEqual(self.minefield._cols, 5)
        self.assertEqual(len(self.minefield._field), 5)
        self.assertEqual(len(self.minefield._field[0]), 5)
        for row in self.minefield._field:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_get_tile_value(self):
        self.assertEqual(self.minefield.get_tile_value(0, 0), 0)
        self.minefield.change_tile_value(0, 0, 5)
        self.assertEqual(self.minefield.get_tile_value(0, 0), 5)

    def test_change_tile_value(self):
        self.minefield.change_tile_value(1, 1, -1)
        self.assertEqual(self.minefield.get_tile_value(1, 1), -1)
        self.minefield.change_tile_value(1, 1, 3)
        self.assertEqual(self.minefield.get_tile_value(1, 1), 3)


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.minefield = Minefield(5, 5)
        self.generator = Generator(5, self.minefield, False)

    def test_generate_mines(self):
        self.generator.generate_mines(5)
        mine_count = sum(row.count(-1) for row in self.minefield._field)
        self.assertEqual(mine_count, 5)

    def test_generate_numbers(self):
        # Place a mine at (2,2)
        self.minefield.change_tile_value(2, 2, -1)
        self.generator.generate_numbers()
        # Check adjacent cells have numbers
        self.assertEqual(self.minefield.get_tile_value(1, 1), 1)  # diagonal
        self.assertEqual(self.minefield.get_tile_value(1, 2), 1)  # above
        self.assertEqual(self.minefield.get_tile_value(1, 3), 1)  # above right
        self.assertEqual(self.minefield.get_tile_value(2, 1), 1)  # left
        self.assertEqual(self.minefield.get_tile_value(2, 3), 1)  # right
        self.assertEqual(self.minefield.get_tile_value(3, 1), 1)  # below left
        self.assertEqual(self.minefield.get_tile_value(3, 2), 1)  # below
        self.assertEqual(self.minefield.get_tile_value(3, 3), 1)  # below right
        # Corner cases
        self.assertEqual(self.minefield.get_tile_value(0, 0), 0)  # far corner


class TestGame(unittest.TestCase):
    @patch('minesweeper.UI')
    @patch('builtins.input', return_value='5')
    def setUp(self, mock_input, mock_ui):
        self.game = Game(10, debug_mode=True)

    def test_initialization(self):
        self.assertEqual(self.game.size, 5)
        self.assertEqual(self.game.size_limit, 10)
        self.assertFalse(self.game.is_over)
        self.assertEqual(self.game.flag_count, 0)

    def test_flag_tile(self):
        # Initially '#'
        self.assertEqual(self.game.player_view[0][0], '#')
        self.game.flag_tile(0, 0)
        self.assertEqual(self.game.player_view[0][0], 'F')
        self.assertEqual(self.game.flag_count, 1)
        self.game.flag_tile(0, 0)
        self.assertEqual(self.game.player_view[0][0], '#')
        self.assertEqual(self.game.flag_count, 0)

    def test_check_tile_safe(self):
        # Find a safe tile (not mine)
        safe_row, safe_col = None, None
        for r in range(self.game.size):
            for c in range(self.game.size):
                if self.game._field.get_tile_value(r, c) != -1:
                    safe_row, safe_col = r, c
                    break
            if safe_row is not None:
                break
        if safe_row is not None:
            value = self.game._field.get_tile_value(safe_row, safe_col)
            self.game.check_tile(safe_row, safe_col)
            self.assertEqual(self.game.player_view[safe_row][safe_col], value)

    @patch('minesweeper.Game.game_over')
    def test_check_tile_mine(self, mock_game_over):
        # Find a mine
        mine_row, mine_col = None, None
        for r in range(self.game.size):
            for c in range(self.game.size):
                if self.game._field.get_tile_value(r, c) == -1:
                    mine_row, mine_col = r, c
                    break
            if mine_row is not None:
                break
        if mine_row is not None:
            self.game.check_tile(mine_row, mine_col)
            mock_game_over.assert_called_once()

    def test_check_for_win(self):
        # Manually set flags on all mines
        mine_positions = []
        for r in range(self.game.size):
            for c in range(self.game.size):
                if self.game._field.get_tile_value(r, c) == -1:
                    mine_positions.append((r, c))
        for r, c in mine_positions:
            self.game.flag_tile(r, c)
        with patch('minesweeper.Game.victory') as mock_victory:
            self.game.check_for_win(len(mine_positions))
            mock_victory.assert_called_once()

    @patch('minesweeper.UI.clear')
    @patch('builtins.print')
    @patch('minesweeper.FileManager.save_game')
    @patch('builtins.input', return_value='n')
    def test_victory(self, mock_input, mock_save, mock_print, mock_clear):
        self.game.victory()
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.result, "VICTORY")

    @patch('minesweeper.UI.clear')
    @patch('builtins.print')
    @patch('minesweeper.FileManager.save_game')
    @patch('builtins.input', return_value='n')
    def test_game_over(self, mock_input, mock_save, mock_print, mock_clear):
        self.game.game_over()
        self.assertTrue(self.game.is_over)
        self.assertEqual(self.game.result, "FAIL")


class TestPlayer(unittest.TestCase):
    @patch('minesweeper.UI')
    @patch('builtins.input', return_value='5')
    def setUp(self, mock_input, mock_ui):
        self.game = Game(10, debug_mode=True)
        self.player = Player(self.game)

    @patch('builtins.input', return_value='3 4')
    @patch('minesweeper.Game.check_tile')
    def test_render_ui_check_tile(self, mock_check_tile, mock_input):
        self.player.render_ui()
        mock_check_tile.assert_called_once_with(2, 3)

    @patch('builtins.input', return_value='3 4 F')
    @patch('minesweeper.Game.flag_tile')
    def test_render_ui_flag_tile(self, mock_flag_tile, mock_input):
        self.player.render_ui()
        mock_flag_tile.assert_called_once_with(2, 3)

class TestUI(unittest.TestCase):
    def setUp(self):
        self.player_view = [['#' for _ in range(3)] for _ in range(3)]
        self.ui = UI(3, self.player_view, False)

    def test_initialization(self):
        self.assertEqual(self.ui._size, 3)
        self.assertEqual(self.ui._player_view, self.player_view)

    @patch('subprocess.run')
    @patch('builtins.print')
    def test_clear(self, mock_print, mock_subprocess):
        self.ui.clear()
        mock_subprocess.assert_called_once()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_render_ui(self, mock_print):
        self.ui.render_ui()
        # Check that print was called multiple times
        self.assertGreater(mock_print.call_count, 5)


class TestFileManager(unittest.TestCase):
    @patch('minesweeper.UI')
    @patch('builtins.input', return_value='5')
    def setUp(self, mock_input, mock_ui):
        self.game = Game(10, debug_mode=True)
        self.file_manager = FileManager("test_data.txt", self.game)

    def tearDown(self):
        if os.path.exists("test_data.txt"):
            os.remove("test_data.txt")

    @patch('builtins.print')
    def test_read_file_exists(self, mock_print):
        with open("test_data.txt", "w") as f:
            f.write("Test content")
        self.file_manager.read_file()
        mock_print.assert_called()

    @patch('builtins.print')
    def test_read_file_not_exists(self, mock_print):
        self.file_manager.read_file()
        mock_print.assert_called_with("File does not exist")

    def test_save_game_new_file(self):
        self.game.result = "VICTORY"
        self.game.elapsed_time = 10.5
        self.file_manager.save_game()
        self.assertTrue(os.path.exists("test_data.txt"))

    def test_save_game_append(self):
        with open("test_data.txt", "w") as f:
            f.write("Existing content\n")
        self.game.result = "FAIL"
        self.game.elapsed_time = 5.2
        self.file_manager.save_game()
        with open("test_data.txt", "r") as f:
            content = f.read()
            self.assertIn("Existing content", content)
            self.assertIn("FAIL", content)


if __name__ == '__main__':
    unittest.main()