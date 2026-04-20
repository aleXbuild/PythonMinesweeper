import random

class Minefield():
    # @property
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

        self.player = PlayerInput()
        self.size = self.player.request_grid_size()

        self._field = Minefield(self.size, self.size)
        self._player_view = [['#' for _ in range(self.size)] for _ in range(self.size)]

        self.generator = Generator(self.size, self._field)
        self.generator.generate_mines(self.size)

        self.ui = UI(self.size, self._player_view, self._debug_mode, self._field)
        self.ui.render()

    def render(self):
        pass

class Generator(Game):
    def __init__(self, size, field):
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
        pass

    def request_grid_size(self):
        return int(input("Grid size: "))

    def render(self):
        pass

class UI(Game):
    def __init__(self, size, player_view, debug_mode, field=[]):
        self._size = size
        self._player_view = player_view
        self._debug_mode = debug_mode

        if self._debug_mode and field!=[]:
            self._field = field
        elif self._debug_mode and field==[]:
            raise AttributeError("Debug mode is enabled but minefield was not provided to the UI")
    
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
                grid = ''
                if not self._debug_mode:
                    grid = self._player_view[row][col]
                else:
                    grid = self._field.get_grid_value(row, col)
                
                st = st + "|  " + str(grid) + "  "
            print(st + "|")

            st = "     "
            for col in range(self._size):
                st = st + "|_____"
            print(st + '|')

        print()


print("MINESWEEPER\n")
game = Game(8, False)