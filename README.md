# AI-Projects
This repository includes all of the programs I have written for my Artificial Intelligence class (using Python). Below are descriptions of some of the most notable projects. 

## 15-Puzzle Slider Game Solver
This program utilizes the A* search algorithm and a Manhattan distance heuristic in order to evaluate board states during the searching process. Importantly, the Manhattan distance heuristic is both an admissible (distances are always underestimates of the true distance) and consistent (distances only get closer to the true value over time), although better heuristics may improve the efficiency of the program. Using the number of inversions within the puzzle also yields information about the solvability of the puzzle. One important takeaway from this project was that the use of lookup tables wherever possible can increase the speed greatly.

### Running
Run `15_puzzle_astar_liang_d (Optimized).py` found [here](https://github.com/derrick20/AI-Projects/tree/master/1-Searches/A*).

After inputting a puzzle, the transitions will be displayed, along with the shortest path length and the duration.

Example inputs (the numbers 10 through 15 are substituted with A through F for simplicity):
* `152349678_ABCDEF`
* `2_63514B897ACDEF`
* `8936C_24A71FDB5E`
* `E19648C5723_ABDF`

## Railroad Shortest Path Solver
This python program compares the efficiency of several search algorithms (breadth-first search, A* search, and the bidirectional variants of each of them). As expected, A* performed better than breadth-first search, and bidirectional search improved both run times by reducing the maximum depth needed for each search tree, even though there were two search trees. It uses latitudes and longitudes of cities throughout the United States and allows for testing of the shortest path between certain cities. Additionally, it displays the progression of the search algorithm's frontier and final path through a Tkinter GUI.

### Running
Run `railroad_liang_d.py` found [here](https://github.com/derrick20/AI-Projects/tree/master/1-Searches/A*).

The program will display a map and prompt you to input a start city and goal city. See `rrNodeCity.txt` for example cities that may be inputted. The map will display the progress of the search algorithm, with the explored edges colored red. Once the shortest path is found, it will be traced from the goal back to the start in green.

The program will output a summary of the search, including cost (path distance), node path (the encountered nodes, indicated by their IDs), the total number of cities explored in searching for the optimal path, the search path (a list of the major cities found in the path, which does not include all of the cities in the path), and the duration of the search.

## Sudoku Solver
A python program that solves Sudoku puzzles generalized to any size MxN. It demonstrates techniques of constraint satisfaction problem-solving such as selecting variables with minimum remaining values, least constrained variables, forward checking, and recursive backtracking. Forward checking allowed for a significant boost in speed (which is analogous to how a person would normally solve a Sudoku, that is, noting what possibilities are eliminated upon placing a number). An important concept for efficiency purposes was to avoid copying large structures by storing the *changes* in said structures, and then reverting back when backtracking. The motivation for this was that most of the structure would be unchanged before backtracking occurred. One step to improve the efficiency in the future would be to implement arc consistency (AC-3), which takes the idea of deducing possibilities to the limit.

### Running
Run `sudoku_part3_liang_d (Optimized).py` found [here](https://github.com/derrick20/AI-Projects/tree/master/2-Constraint%20Satisfaction%20Problems%20(CSP)).

The program will prompt you to input a puzzle. Examples can be found in the `puzzles.txt` or `puzzlesLarge.txt` files. The puzzles are represented as a string of length NM, where N is the width and M is the height of the puzzle. Empty tiles are represented by a period, and, for larger puzzles, letters are used instead of numbers for simplicity.

Upon inputting, the program will display the puzzle and will then display the solved puzzle along with the time taken.

## Othello AI
The aim of this project was to design an intelligent Othello-playing program. This illustrated several techniques within the topic of adversarial search, such as the minimax algorithm and alpha-beta pruning. The bulk of the code, however, was devoted to developing an accurate function to determine the value of a game state upon making a specific move. Some of the considerations included both the current and potential mobility (how many moves a player could make either now or in the future) and piece stability (notably, before a corner is taken, the only pieces that *cannot* be taken are corner pieces). These heuristics were combined with arbitrarily selected weightings, and optimizing these by training via an evolutionary neural network would be one avenue for future improvement. This program beats a player that picks moves randomly approximately 99% of the time and played at a competitive level against human players. Future improvements to the heuristic function (specifically the efficiency of piece stability calculations) would enhance the strength of the program.

### Running
Run `othello_liang_d_FINAL.py` found [here](https://github.com/derrick20/AI-Projects/tree/master/3-Adversarial%20Search).

The program will display a starting board, with '@' symbols representing black pieces and 
'o' representing white pieces. The program has many options for running. Note that the program will always move first, if it is not a human vs. human game. There are four choices for each player: A, M, R, or H (A = alphabeta, M = minimax, R = random, H = human). The input consists of two characters which denote the respective types of each player.

Example: `AR` = alphabeta vs random, with the program playing with alphabeta pruning moving first. The valid moves for each player are displayed each turn, and if there is a human player, the program will prompt you to type a move from the choices (Ex. `G6`).

## Crossword Puzzle Solver
This open-ended project consisted of two phases: creating the frame of a crossword with some given number of blocked squares (such that all words were 3 letters or more and the board was symmetric about the origin) and actually filling the board with valid words. This was another constraint-satisfaction problem and also involved the application of regular expressions. There were two basic approaches to solving: filling in one word at a time, or placing a single letter at a time. Solving with the latter method resulted in a faster (with more constraints to work with), but more complex program (since more work had to be done to update the domains of variables). Future improvements include generalizing the program to larger crossword sizes and implementing arc consistency.

### Running
Run `crossword_liang_d_FINAL.py` found [here](https://github.com/derrick20/AI-Projects/tree/master/4-Regular%20Expressions).

The program will then prompt the dimensions, number of blocked squares, and whether you want there to be words already placed in the crossword. The input format for a word to be placed in the crossword is as follows: orientation (an H or V, indicating horizontal or vertical orientation), the position (row x col, 0-indexed), followed by the word to be placed. Blocks are represented by '#' symbols, and may be included in a word.

Examples to try (large crosswords are likely to be unsolvable, but these illustrate the idea):
* `5x5`, `4`, `y`, `H1x0#best`
* `4x4`, `0`, `n`
* `5x5`, `0`, `y`, `H0x0pasta`, `y`, `v2x2all`, `n`

The program will display the progress of the search, and once the solution is found, it will output the time taken to find it.
