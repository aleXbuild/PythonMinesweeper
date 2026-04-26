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
### Functional Requirements Implementation
- **Grid Generation:** The game generates a grid of specified dimensions and places a set number of mines within it. This is done using random placement algorithms to ensure that the mines are distributed evenly.
- **User Input Handling:** The application takes input from users in the form of grid coordinates, validating these inputs to prevent errors.
- **Game Logic:** The core logic checks for mines and counts adjacent mines for each square. It uses depth-first search to reveal squares until all safe squares are uncovered.

## 3. Results and Summary
### Results
The implementation successfully meets all functional requirements. The game operates as intended, with responsive controls and accurate mine placements.

### Conclusions
Through this project, I have deepened my understanding of game logic and user interaction in Python. The structure of the code allows for easy modifications and improvements in future iterations.

### Extension Possibilities
Future developments could include adding a graphical user interface, difficulty settings (varying grid size and mine count), and multiplayer options.