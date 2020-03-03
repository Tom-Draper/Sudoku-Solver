import numpy as np

sudokus = np.load("data/sudokus.npy")

def apply_constraints(sudoku, row_idx, col_idx):
    # Narrows down the possible values in a given (row, column) based on 
    # the other values in the board
    # Returns a list of the possible values

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
    # Checks whether the sudoku is complete.
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0 and apply_constraints(sudoku, i, j) != 0:
                return False
    return True

def lowest_variable(sudoku):
    # Returns the variable found with lowest number of constraints.
    min_val = len(sudoku)  # Initially hold maximum number of values
    for i in range(len(sudoku)):
        for j in range(len(sudoku[0])):
            if sudoku[i][j] == 0:
                # If this variable has the fewest number of constraints save as start
                if len(apply_constraints(sudoku, i, j)) < min_val:
                    min_val = len(apply_constraints(sudoku, i, j))
                    row, col = i, j  # Save to return
                if min_val == 1:
                    return row, col

def next_variable(sudoku, row, col):
    # Returns the next empty variable by searching columns by rows.

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

        # If this location has a zero, return it
        # But if there are no available variables left return the origional
        if sudoku[new_row][new_col] == 0  or (new_row == row and new_col == col):
            return new_row, new_col
        
def random_variable(sudoku):
    while True:
        row = np.random.choice(range(9))
        col = np.random.choice(range(9))
        
        if sudoku[row][col] != 0:
            return row, col
    

def depth_first(sudoku, row, col):
    # Get constraints for this variable
    constraints = apply_constraints(sudoku, row, col)

    for val in constraints:
        sudoku[row][col] = val  # Test value
        new_row, new_col = next_variable(sudoku, row, col)

        # If row and column have not changed -> SOLVED
        if new_row == row and new_col == col:
            print("SOLVED")
            return True

        # Continue with modifed board on new row and column
        if depth_first(sudoku, new_row, new_col):
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

    solved_sudoku = sudoku
    # Choose starting variable with fewest constraints

    # Alters the values in the solved_sudoku
    # Begin depth first search from the top left square
    while not (complete(solved_sudoku)):
        row, col = random_variable(sudoku)
        depth_first(solved_sudoku, row, col)

    return solved_sudoku

    
count = -1
for sudoku in sudokus:
    count += 1
    print(count)
    print("Before:")
    print(sudoku)
    print("After:")
    print(sudoku_solver(sudoku))
    print()