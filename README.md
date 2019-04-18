# AI-Projects
This repository includes all of the programs I have written for my Artificial Intelligence class (using Python). Below are descriptions of some of

## 15-Puzzle Slider Game Solver
This program utilizes the A* search algorithm and a Manhattan distance heuristic in order to evaluate board states during the searching process. Importantly, the Manhattan distance heuristic is both an admissible (distances are always underestimates of the true distance) and consistent (distances only get closer to the true value over time), although better heuristics may improve the efficiency of the program. Using the number of inversions within the puzzle also yields information about the solvability of the puzzle. One important takeaway from this project was that the use of lookup tables wherever possible can increase the speed greatly.

## Railroad Shortest Path Solver
This python program compares the efficiency of several search algorithms (breadth-first search, A* search, and the bidirectional variants of each of them). As expected, A* performed better than breadth-first search, and bidirectional search improved both run times by reducing the maximum depth needed for each search tree, even though there were two search trees. It uses latitudes and longitudes of cities throughout the United States and allows for testing of the shortest path between certain cities. Additionally, it displays the progression of the search algorithm's frontier and final path through a Tkinter GUI.

## Sudoku Solver
A python program that solves Sudoku puzzles generalized to any size MxN. It demonstrates techniques of constraint satisfaction problem-solving such as selecting variables with minimum remaining values, least constrained variables, forward checking, and recursive backtracking. Forward checking allowed for a significant boost in speed (which is analogous to how a person would normally solve a Sudoku, that is, noting what possibilities are eliminated upon placing a number). An important concept for efficiency purposes was to avoid copying large structures by storing the *changes* in said structures, and then reverting back when backtracking. The motivation for this was that most of the structure would be unchanged before backtracking occurred. One step to improve the efficiency in the future would be to implement arc consistency (AC-3), which takes the idea of deducing possibilities to the limit.

## Othello AI
The aim of this project was to design an intelligent Othello-playing program. This illustrated several techniques within the topic of adversarial search, such as the minimax algorithm and alpha-beta pruning. The bulk of the code, however, was devoted to developing an accurate function to determine the value of a game state upon making a specific move. Some of the considerations included both the current and potential mobility (how many moves a player could make either now or in the future) and piece stability (notably, before a corner is taken, the only pieces that *cannot* be taken are corner pieces). These heuristics were combined with arbitrarily selected weightings, and optimizing these by training via an evolutionary neural network would be one avenue for future improvement. This program beats a player that picks moves randomly approximately 99% of the time and played at a competitive level against human players. Future improvements to the heuristic function (specifically the efficiency of piece stability calculations) would enhance the strength of the program.

## Crossword Puzzle Solver
This open-ended project consisted of two phases: creating the frame of a crossword with some given number of blocked squares (such that all words were 3 letters or more and the board was symmetric about the origin) and actually filling the board with valid words. This was another constraint-satisfaction problem and also involved the application of regular expressions. There were two basic approaches to solving: filling in one word at a time, or placing a single letter at a time. Solving with the latter method resulted in a faster (with more constraints to work with), but more complex program (since more work had to be done to update the domains of variables). Future improvements include generalizing the program to larger crossword sizes and implementing arc consistency.
