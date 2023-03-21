This is a project I made for one of my CEGEP classes. It is a simple checkers game where a user can play against an AI.  It utilizes the pygame library to make the GUI for the game. The rest of it is handled by two classes: Piece handling the piece functionalities like calculating their position, drawing them, or promoting them to kings; and Board handles the board and the game doing things like drawing the board, moving the pieces, determining the winner, etc.; and a few functions to evaluate positions and to make a computer move. It makes use of the minimax algorithm to find a move for the computer.

The controls are very simple, to move a piece, drag it to a valid square(shown by blue dots). If you are chain capturing, for each capture you will need to drag and drop the piece. Before the game start, you can set a difficulty level (1 to 4) deciding how many moves deep the computer will look into. 

To run this project, open the command prompt 
1. Make sure python is installed (run the command : python -V). Install python if it is not installed.
2. Then run the command: py -m ensurepip --upgrade on Windows and python -m ensurepip --upgrade on MacOS to install the pip tool.
3. Finally, install the pygame library using the command py -m pip install -U pygame --user on Windows and python3 -m pip install -U pygame --user on MacOs.
4. Run the main file and enjoy!
