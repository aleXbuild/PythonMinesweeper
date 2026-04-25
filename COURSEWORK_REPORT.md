# COURSEWORK REPORT

## 1. Introduction
### What is the App
The Minesweeper game is a classic puzzle game that challenges players to clear a minefield while avoiding hidden mines. The objective is to uncover all the squares without triggering any mines. This particular implementation is designed to run in Python, utilizing a console interface.

### How to Run
To run the app, ensure you have Python 3 installed. Clone the repository and navigate to the project directory. Use the command `python main.py` to start the game.

### How to Use
Once the game starts, you will see a grid represented in the console. You can uncover a square by inputting its coordinates (e.g., `A1`). If you uncover a mine, the game ends. The goal is to uncover all squares that do not contain mines.

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