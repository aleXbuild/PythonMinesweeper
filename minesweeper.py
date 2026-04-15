import random

class Minefield:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._field = [['#' for _ in range(cols)] for _ in range(rows)]

    def get_grid_value(self, row, col):
        return self._field[row][col]

class Game:
    def __init__(self):
        self.__size_input = input("Grid size: ")
        self._size = int(self.__size_input)
        self._field = Minefield(self._size, self._size)
    
    def draw_grid(self):
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
                st = st + "|  " + str(self._field.get_grid_value(row, col)) + "  "
            print(st + "|")

            st = "     "
            for col in range(self._size):
                st = st + "|_____"
            print(st + '|')

        print()
    
    def generate_mines(self, mine_count):
        k = 0
        while k < mine_count:
            val = random.randint(0, self._size*self._size-1)

            row = val // self._size
            col = val % self._size
    


print("MINESWEEPER\n")
game = Game()
game.draw_grid()