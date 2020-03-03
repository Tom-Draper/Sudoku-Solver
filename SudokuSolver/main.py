import numpy as np

# Load sudokus
sudokus = np.load("data/sudokus.npy")
print("Shape of one sudoku array:", sudokus[0].shape, ". Type of array values:", sudokus.dtype)

# Load solutions
solutions = np.load("data/sudoku_solutions.npy")
print("Shape of one sudoku solution array:", solutions[0].shape, ". Type of array values:", solutions.dtype, "\n")

# Print the first sudoku...
print("Sudoku #1:")
print(sudokus[0], "\n")

# ...and its solution
print("Solution of Sudoku #1:")
print(solutions[0])


def apply_constraints(sudoku, row_idx, col_idx):
    possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Remove row duplicates
    for val in sudoku[row_idx]:
        if val != 0 and val in possible:
            possible.remove(val)
            
    # Remove col duplicates
    for row in sudoku:
        val = row[col_idx]
        if val != 0 and val in possible:
            possible.remove(val)
            
    # Remove duplicates from square
    # Get top left location of sudoku square the variable is in
    square_row = (row_idx // 3) * 3
    square_col = (col_idx // 3) * 3
    
    # Loop through square and remove duplicates
    for i in range(square_row, square_row + 3):
        for j in range(square_col, square_col + 3):
            val = sudoku[i][j]
            if val != 0 and val in possible:
                possible.remove(val)
    
    return possible

def complete(sudoku):
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if apply_constraints(sudoku, i, j) != 0:
                return False
    return True

def nextVariable(sudoku):
    min_val = len(sudoku)  # Initially hold maximum number of values
    start_var = tuple()
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                # If this variable has the fewest number of constraints save as start
                if len(apply_constraints(sudoku, i, j)) < min_val:
                    min_val = len(apply_constraints(sudoku, i, j))
                    start_var = tuple((i, j))
            if min_val == 1: break
        if min_val == 1: break
    return start_var

def traverse(sudoku, var, constraints):
    if complete(sudoku):
        return
    
    row, col = var[0], var[1]
    for value in constraints:
        new_sudoku = sudoku[:]
        new_sudoku[row][col] = value
        new_constraints = apply_constraints(sudoku, row, col)
        new_var = nextVariable(sudoku)
        
        if len(new_constraints) != 0:
            traverse(new_sudoku, new_var, new_constraints)
            

def sudoku_solver(sudoku):
    """Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    solved_sudoku = sudoku    
        
    # Choose starting variable with fewest constraints
    start_var = nextVariable(solved_sudoku)
        
    constraints = apply_constraints(solved_sudoku, start_var[0], start_var[1])
    print(start_var)
    print(constraints)
    
    solved_sudoku = traverse(sudoku, start_var, constraints)
        
    print(solved_sudoku)
    return solved_sudoku


sudoku_solver(sudokus[0])