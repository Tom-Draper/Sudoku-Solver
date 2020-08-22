# Sudoku-Solver

## Sudoku
Sudoku is a Japanese puzzle where the aim is to fill a 9x9 grid with digits so that any row, column and 3x3 sub-grid are filled with only unique values (1-9). The puzzle begins with initial starting values already filled in. In 2005, Bertram Felgenhauer and Frazer Jarvis calculated number of valid Sudoku solution grids for a 9x9 grid to be 9! × 722 × 27 × 27,704,267,971 = 6,670,903,752,021,072,936,960.    
https://en.wikipedia.org/wiki/Sudoku    
https://en.wikipedia.org/wiki/Mathematics_of_Sudoku

The Sudoku solver takes a 9x9 numpy array and solves a Sudoku puzzle using a backtracking algorithm and depth first search. It makes use of constraint satisfaction to minimise down the options a particular square could take. Once run, it returns a completed puzzle. in If it finds no solution to the Sudoku, it instead returns a 9x9 array filled with -1.

## Getting Started
Run main.py

### Prerequisites
Python module numpy is required to run.

## How it Works
The soluton selects a starting variable (single Sudoku squre that can hold an integer value) by analysing each variables constraints at that time. For each variable, it looks at the other variables and reduces down the options to a list of possible values this variable can take. The variable with the lowest number of options that it can take is selected first.    
This program also includes alternative slower methods to find the next variable such as finding the next empty space moving across columns and rows from the last variable. It also includes the slowest method of taking the variable with the most constraints.
Once the variable is found, it performs a recursive depth first search, the the variable taking each possible values after taking the current constriants into consideration. For each value the square has taken it finds the next variable, which finds possible values using constraints based on the modified board. And so on until it reaches a variable that has no possible values it can take. At this point is backtracks up the tree until it reaches a previously visited variable with a possible value that hasn't been explored yet. This continues until a solution is found. If there is no solution, eventually the algorithm backs up all the way to the root node and terminates.

![depth-first-search](https://user-images.githubusercontent.com/41476809/76250443-4a761080-623d-11ea-999d-0c4ddc341572.jpg)

