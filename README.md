This is a project I made for one of my CEGEP classes. It is a simple checkers game where a user can play against an AI.  It utilizes the pygame library to make the GUI for the game. The rest of it is handled by two classes: Piece handling the piece functionalities like calculating their position, drawing them, or promoting them to kings; and Board handles the board and the game doing things like drawing the board, moving the pieces, determining the winner, etc.; and a few functions to evaluate positions and to make a computer move. It makes use of the minimax algorithm to find a move for the computer.

The controls are very simple, to move a piece, drag it to a valid square(shown by blue dots). If you are chain capturing, for each capture you will need to drag and drop the piece. Before the game start, you can set a difficulty level (1 to 4) deciding how many moves deep the computer will look into. 

To run this project, download the folder and run the main.exe file.
