import numpy as np
import time


class Solver:
    def apply_constraints(self, sudoku, row_idx, col_idx):
        """Narrows down the possible values in a given (row, column) based on 
        the other values in the board. Returns a list of the possible values."""
        
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
        """Checks whether the input sudoku is complete."""
        
        for i in range(len(sudoku)):
            for j in range(len(sudoku[0])):
                if sudoku[i][j] == 0 and self.apply_constraints(sudoku, i, j) != 0:
                    return False
        return True
    
    def next_variable3(self, sudoku, row, col):
        """The much slower alternatvie to next_variable function.
        This function will produce the longest time to find a the solution as
        the branching factor is a maximum during depth-first search.
        Returns the variable found with highest number of constraints."""
        
        var_info = []  # Holds tuples of number of constraints, and position
        for i in range(len(sudoku)):
            for j in range(len(sudoku[0])):
                if sudoku[i][j] == 0:
                    n = len(self.apply_constraints(sudoku, i, j))
                    if n == 9:  # If maximum constraints found, cannot find better
                        return i, j
                    var_info.append(tuple((n, i, j)))

        # Sort list and take variable with most constraints
        if len(var_info) > 0:
            var_info.sort(key=lambda x: x[0], reverse=True)
            return var_info[0][1], var_info[0][2]
        
        # If no constraints found, return input row and column
        return row, col
    
    def next_variable2(self, sudoku, row, col):
        """A longer alternative to the next_variable function.
        Returns the next empty variable by searching along columns by rows."""

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
        """Returns the variable found with lowest number of constraints."""
        
        var_info = []  # Holds tuples of number of constraints, and position
        for i in range(len(sudoku)):
            for j in range(len(sudoku[0])):
                if sudoku[i][j] == 0:
                    n = len(self.apply_constraints(sudoku, i, j))
                    if n == 1:  # If only one constraint, cannot find better
                        return i, j
                    var_info.append(tuple((n, i, j)))

        # Sort list and take variable with least constraints
        if len(var_info) > 0:
            var_info.sort(key=lambda x: x[0])
            return var_info[0][1], var_info[0][2]
        
        # If no constraints found, return original input row and column
        return row, col

    def depth_first(self, sudoku, row, col):
        """Recursively uses depth first search to find a solution."""
        
        # Get constraints for this variable
        constraints = self.apply_constraints(sudoku, row, col)
        
        for val in constraints:
            sudoku[row][col] = val  # Test value
            new_row, new_col = self.next_variable(sudoku, row, col)
            
            # If row and column are unchanged -> all placed filled
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
        start_row, start_col = self.next_variable(sudoku, 0, 0)
        # Alters the values in the solved_sudoku
        # Begin depth first search from the top left square
        self.depth_first(solved_sudoku, start_row, start_col)
        
        if not self.complete(solved_sudoku):
            print("No solution")
            solved_sudoku = np.full((9, 9), -1.)
        
        return solved_sudoku


def run(sudokus, solutions):
    for i in range(len(sudokus)):
        print(i+1)
        print("Before:")
        print(sudokus[i])
        print("After:")
        start = time.time()
        result = solver.sudoku_solver(sudokus[i])
        time_taken = time.time() - start
        print(result)
        print("Solution:")
        print(solutions[i])
        print("Correct:", np.array_equal(solutions[i], result))
        print("Time taken:", time_taken, "seconds")
        print("-" * 40)


# Load sudokus
sudokus = np.load("data/sudokus.npy")
# Load solutions to sample sudokus
solutions = np.load("data/sudoku_solutions.npy")

solver = Solver()
run(sudokus, solutions)