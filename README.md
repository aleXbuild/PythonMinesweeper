# PythonMinesweeper

## 1. Introduction
### What is the App
The Minesweeper game is a classic puzzle game that challenges players to clear a minefield while avoiding hidden mines. The objective is to uncover all the squares without triggering any mines. This particular implementation is designed to run in Python, utilizing a console interface.

### How to Run
To run the app, ensure you have Python 3 installed. Clone the repository and navigate to the project directory. Use the command `python minesweeper.py` to start the game.

### How to Use
Once the game starts, you will be asked to select a grid size for the minefield (allowed range is given in brackets). 

    ![Grid size selection](img/1.png)

By typing -1 you will enter file read mode, which will be covered later. A freshly generated minefield will appear as well as prompt for selecting a tile you want to check.

    ![Generated minefield](img/2.png)

To check a tile, type it's row and column number separated by space.

    ![Selecting tile](img/3.png)

Selected tile revealed a number representing ammount of mines around it. If you check the tile with a mine in it, you will lose.

    ![After check](img/4.png)

In order to win the game, you have to flag all the mines in the field. In order to place a flag, select the tile as previously shown, except this time add 'F' letter. Both lowercase and uppercase work.

    ![Flagging the tile](img/5.png)

If selected tile already has a flag in it, flag will be removed.

After losing or winning, you will be asked, if you want to save results of this session in a file. After agreeing by typing 'y' (once again, both lowercase and uppercase work), the information will be written to `data.txt` file. You can access this file through game's interface by typing -1 after launching the game.

    ![File read mode](img/6.png)

## 2. Body/Analysis
The program implements all 4 OOP pillars:

### 1. Polymorphism
Polymorphism is utilized for `render_ui()` method, which is abstract in Game class. Child classes Player and UI override this method to view their elements of game's UI:

    # Method in Game class
    def render_ui(self):
        pass

    ...

    # Method in Player class
    def render_ui(self):
        try:
            msg = "Select row and column: "
            parts = input(msg).split()
            self._selected_row, self._selected_col = int(
                parts[0]), int(parts[1])
            flag = parts[2] if len(parts) > 2 else ''
        except (IndexError, ValueError):
            self._game.ui.clear()
            return

        row = self._selected_row
        col = self._selected_col
        size = self._game.size
        if row > 0 and col > 0 and row <= size and col <= size:
            if flag == 'F' or flag == 'f':
                self._game.flag_tile(row - 1, col - 1)
            elif not flag or flag == '':
                self._game.check_tile(row - 1, col - 1)

    ...

    # Method in UI class:
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

    ...

    # Execution
    game = Game(8, False)

    while not game.is_over:
        game.ui.render_ui()
        game.player.render_ui()

## 3. Results and Summary
### Results
The implementation successfully meets all functional requirements. The game operates as intended, with responsive controls and accurate mine placements.

### Conclusions
Through this project, I have deepened my understanding of game logic and user interaction in Python. The structure of the code allows for easy modifications and improvements in future iterations.

### Extension Possibilities
Future developments could include adding a graphical user interface, difficulty settings (varying grid size and mine count), and multiplayer options.