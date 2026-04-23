import random
import os
import subprocess

class Minefield():
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._field = [[0 for _ in range(cols)] for _ in range(rows)]

    def get_tile_value(self, row, col):
        return self._field[row][col]
    
    def change_tile_value(self, row, col, value :int):
        self._field[row][col] = value

class Game:
    @property
    def size_limit(self):
        return self._size_limit
    
    @size_limit.setter
    def size_limit(self, value):
        if value < 3:
            raise ValueError("Size limit was set too low")
        else:
            self._size_limit = value

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value :int):
        if value < 3:
            self._size = 0
        elif value > self.size_limit:
            self._size = 0
        else:
            self._size = value

    def __init__(self, size_limit, debug_mode=False):
        self.size_limit = size_limit
        self._debug_mode = debug_mode

        self.flag_count = 0
        self.is_over = False

        self.player = Player(self)
        self.size = self.player.request_grid_size()

        self._field = Minefield(self.size, self.size)
        self._player_view = [['#' for _ in range(self.size)] for _ in range(self.size)]

        self._generator = Generator(self.size, self._field, self._debug_mode)
        self._generator.generate_mines(self.size)
        self._generator.generate_numbers()

        self.ui = UI(self.size, self._player_view, self._debug_mode, self._field)
        self.render_ui

    def render_ui(self):
        pass

    def flag_tile(self, row, col):
        if self._player_view[row][col] == 'F':
            self._player_view[row][col] = '#'
            self.flag_count -= 1
        elif self._player_view[row][col] == '#':
            self._player_view[row][col] = 'F'
            self.flag_count += 1

        self.ui.clear()
    
    def check_tile(self, row, col):
        if self._field.get_tile_value(row, col) == -1:
            self.game_over()
        else:
            self._player_view[row][col] = self._field.get_tile_value(row, col)
            self.ui.clear()

    def check_for_win(self, mine_count):
        match_count = 0
        for row in range(self._size):
            for col in range(self._size):
                if self._field.get_tile_value(row, col) == -1 and self._player_view[row][col] == 'F':
                    match_count += 1

        if match_count == mine_count:
            self.victory()

    def victory(self):
        self.is_over = True
        self.ui.clear()
        print("VICTORY")

        for row in range(self._size):
            for col in range(self._size):
                if self._field.get_tile_value(row, col) != -1:
                    self._player_view[row][col] = self._field.get_tile_value(row, col)
        
        self.ui.render_ui()

    def game_over(self):
        self.is_over = True
        self.ui.clear()
        print("GAME OVER")

        for row in range(self._size):
            for col in range(self._size):
                if self._field.get_tile_value(row, col) == -1 and self._player_view[row][col] != 'F':
                    self._player_view[row][col] = 'M'
        
        self.ui.render_ui()

class Generator(Game):
    def __init__(self, size, field, debug_mode):
        self._size = size
        self._field = field
        self._debug_mode = debug_mode
    
    def generate_mines(self, mine_count):
        k = 0
        while k < mine_count:
            row = random.randint(0, self._size-1)
            col = random.randint(0, self._size-1)

            if self._field.get_tile_value(row, col) != -1:
                self._field.change_tile_value(row, col, -1)
                k += 1

    def __add_number(self, row, col):
        if self._field.get_tile_value(row, col) != -1:
            grid_num = self._field.get_tile_value(row, col) + 1  
            self._field.change_tile_value(row, col, grid_num)
            if self._debug_mode:
                print(f"Incremented ({row}, {col}) to {grid_num}")

    def generate_numbers(self):
        for row in range(self._size):
            for col in range(self._size):
                if self._field.get_tile_value(row, col) == -1:
                    gen_row = row
                    gen_col = col

                    if gen_row - 1 >= 0:
                        gen_row -= 1
                        self.__add_number(gen_row, gen_col)

                        if gen_col -1 >= 0:
                            gen_col -= 1
                            self.__add_number(gen_row, gen_col)

                        gen_col = col
                        if gen_col + 1 < self._size:
                            gen_col += 1
                            self.__add_number(gen_row, gen_col)

                    gen_row = row
                    if gen_row + 1 < self._size:
                        gen_row += 1
                        self.__add_number(gen_row, gen_col)

                        if gen_col - 1 >= 0:
                            gen_col -= 1
                            self.__add_number(gen_row, gen_col)

                        gen_col = col
                        if gen_col + 1 < self._size:
                            gen_col += 1
                            self.__add_number(gen_row, gen_col)

                    gen_row = row
                    gen_col = col
                    if gen_col - 1 >= 0:
                        gen_col -= 1
                        self.__add_number(gen_row, gen_col)

                    gen_col = col
                    if gen_col + 1 < self._size:
                        gen_col += 1
                        self.__add_number(gen_row, gen_col)


class Player(Game):
    def __init__(self, game):
        self._game = game
        self._selected_row = 0
        self._selected_col = 0

    def request_grid_size(self):
        return int(input("Grid size: "))

    def render_ui(self):
        parts = input("Select row and column (space-separated): ").split()
        self._selected_row, self._selected_col = int(parts[0]), int(parts[1])
        flag = parts[2] if len(parts) > 2 else ''
        
        if flag == 'F':
            self._game.flag_tile(self._selected_row-1, self._selected_col-1)
        else:
            self._game.check_tile(self._selected_row-1, self._selected_col-1)



class UI(Game):
    def __init__(self, size, player_view, debug_mode, field=[]):
        self._size = size
        self._player_view = player_view
        self._debug_mode = debug_mode

        if self._debug_mode and field!=[]:
            self._field = field
        elif self._debug_mode and field==[]:
            raise AttributeError("Debug mode is enabled but minefield was not provided to the UI")
    
    def clear(self):
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print("\nMINESWEEPER\n")

    def render_ui(self):
        print()
        st = "   "
        for i in range(self._size):
            st = st + "     " + str(i + 1)
        print(st)

        for row in range(self._size):
            st = "     "
            if row == 0:
                for col in range(self._size):
                    st = st + "______" 
                print(st)

            st = "     "
            for col in range(self._size):
                st = st + "|     "
            print(st + "|")

            st = "  " + str(row + 1) + "  "
            for col in range(self._size):
                grid = ''
                if not self._debug_mode:
                    grid = self._player_view[row][col]
                else:
                    grid = self._field.get_tile_value(row, col)
                
                st = st + "|  " + str(grid) + "  "
            print(st + "|")

            st = "     "
            for col in range(self._size):
                st = st + "|_____"
            print(st + '|')

        print()


print("\nMINESWEEPER\n")

game = Game(8, False)

while not game.is_over:
    game.ui.render_ui()
    game.player.render_ui()
    if game.flag_count == game.size:
        game.check_for_win(game.size)