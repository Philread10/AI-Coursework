import numpy as np

invalidSudoku = np.array([[-1]*9]*9)

class Sudoku:

    def __init__(self, grid):
        self.grid = grid    

    #Retrieves empty cells currently on grid
    def getEmptyCells(self):
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    #Retrieves possible moves for that empty cell, given constraints for Sudoku
    def getPossibleValues(self, cell):
        possible_values = []
        row = self.grid[cell[0]]

        if cell[0] < 3:
          rowLowerBound = 0
        elif cell[0] < 6:
          rowLowerBound = 3
        elif cell[0] < 9:
          rowLowerBound = 6
        
        rowUpperBound = rowLowerBound + 3

        col = self.grid[:, cell[1]]
        if cell[1] < 3:
          colLowerBound = 0
        elif cell[1] < 6:
          colLowerBound = 3
        elif cell[1] < 9:
          colLowerBound = 6
        colUpperBound = colLowerBound + 3

        square = self.grid[rowLowerBound:rowUpperBound, colLowerBound:colUpperBound]

        for i in range(1, 10):
            if i not in row and i not in col and i not in square:
              possible_values.append(i)

        return possible_values

    #Main constraint satisfaction implementation. If there is only one possible     value, replace the empty cell with it. It is recursive, so if anything changes it will repeat to see if there's any new possibilities.
    def constraintSatisfaction(self, empty_cells):
      change = 0 
      for cell in empty_cells:        
        possible_values = self.getPossibleValues(cell)
        if len(possible_values) == 1:
          self.grid[cell[0], cell[1]] = possible_values[0]
          change = change + 1
      if change > 0:
        self.constraintSatisfaction(self.getEmptyCells())

    #Checks that the grid conforms to the rules.
    def sudokuCheckAccurate(self):

      for i in range(0,9):
        row_list = []
        for j in range (0,9):
          row_list.append(self.grid[i,j])
        if len(row_list) != len(set(row_list)):
            return False

      for i in range(0,9):
        column_list = []
        for j in range (0,9):
          column_list.append(self.grid[j,i])
        if len(column_list) != len(set(column_list)):
            return False     

      listOfRows = np.split(self.grid, 3)
      for i in listOfRows:
        gridToCheck = np.hsplit(i,3)
        for grid in gridToCheck:
          grid_list = []
          for i in range(0,3):
            for j in range(0,3):
              grid_list.append(grid[i,j])
          if len(grid_list) != len(set(grid_list)): 
            return False
      return True     

#backtracking depth first search algorithm
def backtrack(sudoku):
    empty_cells = sudoku.getEmptyCells()
    if empty_cells == []:
        return True

    dictionary_list = []
    for cell in empty_cells:
      possible_values = sudoku.getPossibleValues(cell)
      dict = {'Cell' : cell ,'Domain Length' : len(possible_values)}
      dictionary_list.append(dict)
  
    from operator import itemgetter
  
    dictionary_list.sort(key=itemgetter('Domain Length'))

    sorted_empty_cells = []
    for dictionary in dictionary_list:
      sorted_empty_cells.append(dictionary["Cell"])

    for cell in sorted_empty_cells:
        possible_values = sudoku.getPossibleValues(cell)
        for i in possible_values:
            sudoku.grid[cell[0], cell[1]] = i
            grid_clone = np.copy(sudoku.grid)
            sudoku.constraintSatisfaction(sudoku.getEmptyCells())
            if sudoku.getEmptyCells() == []:
                return True
            else:
                sudoku.grid = grid_clone
            if backtrack(sudoku):
                return True
            else:
                sudoku.grid[cell[0], cell[1]] = 0
        return False

#Final Implementation of above functions to solve sudoku
def sudoku_solver(grid):
    s = Sudoku(grid)
    s.constraintSatisfaction(s.getEmptyCells())
    if s.getEmptyCells() == 0:
        if s.sudokuCheckAccurate() == False:
          return invalidSudoku          
        return s.grid
    else:
        if backtrack(s) == True:
          if s.sudokuCheckAccurate() == False:
            return invalidSudoku            
          return s.grid
        else:
            return invalidSudoku

SKIP_TESTS = False

def tests():
    import time
    difficulties = ['medium']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")
        
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)
            
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)
            
            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
            
            print("This sudoku took", end_time-start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break
            
if not SKIP_TESTS:
    tests()


