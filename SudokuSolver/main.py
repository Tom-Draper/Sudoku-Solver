import numpy as np

# Load sudokus
sudokus = np.load("data/sudokus.npy")

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

def lowest_variable(sudoku):
    """Returns the variable found with lowest number of constraints"""
    min_val = len(sudoku)  # Initially hold maximum number of values
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                # If this variable has the fewest number of constraints save as start
                if len(apply_constraints(sudoku, i, j)) < min_val:
                    min_val = len(apply_constraints(sudoku, i, j))
                    row, col = i, j  # Save to return
            if min_val == 1: break
        if min_val == 1: break
    return row, col

def next_variable(sudoku, row, col):
    """Returns the next empty variable by searching columns by rows."""
    
    new_row, new_col = row, col
    while True:
        if new_col + 1 == len(sudoku):
            new_col = 0
            if new_row + 1 == len(sudoku):
                new_row = 0
            else:
                new_row += 1
        else:
            new_col += 1
            
        if sudoku[new_row][new_col] == 0:
            return new_row, new_col
        
        # No available variables
        if new_row == row and new_col == col:
            return new_row, new_col

def traverse(sudoku, row, col, constraints):
    if complete(sudoku):
        return
    
    for value in constraints:
        new_sudoku = sudoku[:]
        new_sudoku[row][col] = value
        new_row, new_col = next_variable(sudoku, row, col)
        new_constraints = apply_constraints(sudoku, new_row, new_col)
        
        if len(new_constraints) != 0:
            traverse(new_sudoku, new_row, new_col, new_constraints)
            
def traverse_(sudoku, row, col, complete):
    constraints = apply_constraints(sudoku, row, col)
    for val in constraints:
        sudoku[row][col] = val
        new_row, new_col = next_variable(sudoku, row, col)
        if traverse_(sudoku, new_row, new_col, complete):
            return True
    sudoku[row][col] = 0  # Reset this variable on backtrack
    return False
            

def sudoku_solver(sudoku):
    """Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    print(sudoku)
    solved_sudoku = sudoku
        
    # Choose starting variable with fewest constraints
    start_row, start_col = lowest_variable(solved_sudoku)  
    constraints = apply_constraints(solved_sudoku, start_row, start_col)
    solved_sudoku = traverse_(solved_sudoku, 0, 0, False)
        
    print(solved_sudoku)
    return solved_sudoku


sudoku_solver(sudokus[0])