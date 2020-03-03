import numpy as np
import os

# Load sudokus
sudokus = np.load("data/sudokus.npy")

class Solver:
    def apply_constraints(self, sudoku, row_idx, col_idx):
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

    def complete(self, sudoku):
        # Checks whether the sudoku is complete.
        
        for i in range(len(sudoku)):
            for j in range(len(sudoku[0])):
                if sudoku[i][j] == 0 and self.apply_constraints(sudoku, i, j) != 0:
                    return False
        return True

    def next_along(self, sudoku, row, col):
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

    def next_variable(self, sudoku, row, col):
        # Returns the variable found with lowest number of constraints.
        min_val = len(sudoku)  # Initially hold maximum number of values
        variables = []
        for i in range(len(sudoku)):
            for j in range(len(sudoku[0])):
                if sudoku[i][j] == 0:
                    n = len(self.apply_constraints(sudoku, i, j))
                    if n == 1:
                        return i, j
                    variables.append(tuple((n, i, j)))

        if len(variables) > 0:
            variables.sort(key=lambda x: x[0])
            return variables[0][1], variables[0][2]
        
        return self.next_along(sudoku, row, col)
                
    def depth_first(self, sudoku, row, col):
        # Recursively uses depth first search to find a solution.
        
        # Get constraints for this variable
        constraints = self.apply_constraints(sudoku, row, col)
        
        for val in constraints:
            sudoku[row][col] = val  # Test value
            new_row, new_col = self.next_variable(sudoku, row, col)
            
            # If row and column have not changed -> SOLVED
            if new_row == row and new_col == col:
                print("SOLVED")
                return True
            
            # Continue with modifed board on new row and column
            if self.depth_first(sudoku, new_row, new_col):
                return True
        sudoku[row][col] = 0  # Reset this variable on backtrack
        return False
                

    def sudoku_solver(self, sudoku):
        """Solves a Sudoku puzzle and returns its unique solution.

        Input
            sudoku : 9x9 numpy array
                Empty cells are designated by 0.

        Output
            9x9 numpy array of integers
                It contains the solution, if there is one. If there is no solution, all array entries should be -1.
        """
        
        solved_sudoku = sudoku
        
        #start_row, start_col = self.lowest_variable(solved_sudoku, 0, 0) 
        start_row, start_col = self.next_variable(sudoku, 0, 0)
        # Alters the values in the solved_sudoku
        # Begin depth first search from the top left square
        self.depth_first(solved_sudoku, start_row, start_col)
        # If depth first back tracked to root, attempt again from different start point
        
        # If no change, no solution
        if not self.complete(solved_sudoku):
            print("No solution")
            solved_sudoku = np.full((9, 9), -1.)
        
        return solved_sudoku

solver = Solver()

count = 0
for sudoku in sudokus:
    print(count)
    print("Before:")
    print(sudoku)
    print("After:")
    result = solver.sudoku_solver(sudoku)
    print(result)
    print()
    count += 1