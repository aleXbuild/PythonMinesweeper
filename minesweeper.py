class Minefield:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._field = [[0 for _ in range(cols)] for _ in range(rows)]

    def get_grid_value(self, row, col):
        return self._field[row][col]

class Game:
    def __init__(self):
        self._rows = input("Rows: ")
        self._cols = input("Columns: ")
        self._field = Minefield(int(self._rows), int(self._cols))
    
    def draw_grid(self):
        print()
        print(self._field.get_grid_value(0, 0))

    


print("MINESWEEPER\n")
game = Game()
game.draw_grid()