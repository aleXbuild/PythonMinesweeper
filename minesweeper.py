import random

class Minefield():
    @property
    # def field(self):
    #     return self._field
    
    # @field.setter
    # def field(self, value):
    #     if not (isinstance(value, list) and all(isinstance(self._rows, list) for self._rows in value)):
    #         raise TypeError("Minefield must be a two-dimentional list!")
    #     else:
    #         self._field = value

    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._field = [[0 for _ in range(cols)] for _ in range(rows)]

    def get_grid_value(self, row, col):
        return self._field[row][col]
    
    def change_grid_value(self, row, col, value :int):
        self._field[row][col] = value

class Game:
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value :int):
        if value < 2:
            return 0
        else:
            return value

    @property
    def size_limit(self):
        return self._size_limit

    def __init__(self, size_limit, is_debug_mode=False):
        self.size_limit = size_limit
        self._field = Minefield(self._size, self._size)
        if is_debug_mode:
            self._player_view = self._field
        else:
            self._player_view = [[['#' for _ in range(self._size)] for _ in range(self._size)]]

        self.ui = UI(self._player_view)
        self.generator = Generator(self.size, self._field, self.size)

    def render(self):
        pass

class Generator(Game):
    def __init__(self, size, field, mine_count):
        self._size = size
        self._field = field
    
    def generate_mines(self, mine_count):
        k = 0
        while k < mine_count:
            row = random.randint(0, self._size-1)
            col = random.randint(0, self._size-1)

            if (self._field.get_grid_value(row, col) != -1):
                self._field.change_grid_value(row, col, -1)
                k += 1



class PlayerInput(Game):
    def __init__(self):
        super.size = int(input("Grid size: "))

class UI(Game):
    def __init__(self, player_view):
        self._player_view = player_view
    
    def render(self):
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
                st = st + "|  " + str(self._player_view[row][col]) + "  "
            print(st + "|")

            st = "     "
            for col in range(self._size):
                st = st + "|_____"
            print(st + '|')

        print()


print("MINESWEEPER\n")
game = Game()