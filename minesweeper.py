import random
import os

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
        if value < 2:
            raise ValueError("Size limit was set too low")
        else:
            self._size_limit = value

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value :int):
        if value < 2:
            self._size = 0
        elif value > self.size_limit:
            self._size = 0
        else:
            self._size = value

    def __init__(self, size_limit, debug_mode=False):
        self.size_limit = size_limit
        self._debug_mode = debug_mode

        self.player = Player()
        self.size = self.player.request_grid_size()

        self._field = Minefield(self.size, self.size)
        self._player_view = [['#' for _ in range(self.size)] for _ in range(self.size)]

        self.generator = Generator(self.size, self._field)
        self.generator.generate_mines(self.size)
        self.generator.generate_numbers()

        self.ui = UI(self.size, self._player_view, self._debug_mode, self._field)

        while not self.player.is_dead:
            self.ui.render_ui()
            self.player.render_ui()

    def render_ui(self):
        pass

    def update(self):
        if self._field.get_tile_value(self.player.get_row_selection(), self.player.get_col_selection) == -1:


class Generator(Game):
    def __init__(self, size, field):
        self._size = size
        self._field = field
    
    def generate_mines(self, mine_count):
        k = 0
        while k < mine_count:
            row = random.randint(0, self._size-1)
            col = random.randint(0, self._size-1)

            if (self._field.get_tile_value(row, col) != -1):
                self._field.change_tile_value(row, col, -1)
                k += 1

    def __add_number(self, row, col):
        if (self._field.get_tile_value(row, col) != -1):
            grid_num = self._field.get_tile_value(row, col) + 1  
            self._field.change_tile_value(row, col, grid_num)

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

                        if gen_col -1 >= 0:
                            gen_col -= 1
                            self.__add_number(gen_row, gen_col)

                        gen_col = col
                        if gen_col + 1 < self._size:
                            gen_col += 1
                            self.__add_number(gen_row, gen_col)

                    gen_row = row
                    if gen_col -1 >= 0:
                        gen_col -= 1
                        self.__add_number(gen_row, gen_col)

                    gen_col = col
                    if gen_col + 1 < self._size:
                        gen_col += 1
                        self.__add_number(gen_row, gen_col)


class Player(Game):
    def __init__(self, field):
        self._field = field

        self._selected_row = 0
        self._selected_col = 0
        self._is_flag = False
        self.is_dead = False

    def request_grid_size(self):
        return int(input("Grid size: "))

    def render_ui(self):
        self._selected_row, self._selected_row = map(int, input("Select row and column (space-separated): ").split())

    def get_row_selection(self):
        return self._selected_row
    
    def get_col_selection(self):
        return self._selected_col


class UI(Game):
    def __init__(self, size, player_view, debug_mode, field=[]):
        self._size = size
        self._player_view = player_view
        self._debug_mode = debug_mode

        if self._debug_mode and field!=[]:
            self._field = field
        elif self._debug_mode and field==[]:
            raise AttributeError("Debug mode is enabled but minefield was not provided to the UI")
    
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


print("MINESWEEPER\n")
game = Game(8, False)