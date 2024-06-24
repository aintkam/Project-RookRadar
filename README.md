# Project-RookRadar

The project's goal was to create a program that takes a physical chessboard, runs it through stockfish API, and outputs the best move to play

The project uses Roboflow with YOLO v9 for object detection in order to detect the 4 corners of the chessboard and each piece
- Using numpy, we convert the corners found to an array and order the points as a rectangle
- We transform the matrix into a bird's eye view using a perspectiveMatrix
- Using the image manipulation, we set squares around each square on the chessboard and gets its position in an array
- The chess piece model then makes a prediction and compares each (X,Y) coordinate found to its corresponding square

We also created a working version of Stockfish chess that the user can play against
- Without using multi threading, the stockfish is understandably slow

We made a working version of a normal chess game as a template to build upon

We created GUI for a starting menu and black/white winning
- The GUI's are implimented with Stockfish API chess, but not the normal version of chess

The project does not fully work as this is the extent the project has been made

To fully complete the project, we would need to connect the AI model to the stockfish API - most likely by making the model find and return the FIN notation that stockfish can use

As of right now, we do not plan on completing this project, but we will be using it as a base for a similar project later.
