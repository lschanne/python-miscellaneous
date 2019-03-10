"""
This module contains a class that is built for solving sudoku puzzles.
Here's a string format that I am enjoying which will be used to display output:
7 _ _ | 2 8 1 | _ _ 6
_ _ _ | 4 _ _ | _ _ 7
1 _ 5 | _ 9 _ | 8 3 _
---------------------
_ _ _ | 8 _ _ | 3 _ 5
_ _ 6 | 7 2 3 | 4 _ _
3 _ 8 | _ _ 6 | _ _ _
---------------------
_ 7 2 | _ 6 _ | 5 _ 9
8 _ _ | _ _ 2 | _ _ _
9 _ _ | 1 5 4 | _ _ 2
"""

class SudokuSolver:
    def __init__(self):
        self.fillValue  = 0
        self.fillString = '_'
        self.columnSep  = ' | '
        self.rowSep    = '-' * 21 + '\n'
        self.StringToMatrix = lambda boardString: [list(map(int, x)) for x in boardString.replace(self.fillString, str(self.fillValue)).replace(self.columnSep, '').replace(self.rowSep, '').replace(' ', '').split('\n')]
        
    def InputMatrix(self, inputBoard):
        """
        This method accepts a list of 9 lists with 9 items each to represent the board.
        Here's an example of what that looks like:
        x = 0
        inputBoard = [[3,x,6,5,x,8,4,x,x],
                      [5,2,x,x,x,x,x,x,x],
                      [x,8,7,x,x,x,x,3,1],
                      [x,x,3,x,1,x,x,8,x],
                      [9,x,x,8,6,3,x,x,5],
                      [x,5,x,x,9,x,6,x,x],
                      [1,3,x,x,x,x,2,5,x],
                      [x,x,x,x,x,x,x,7,4],
                      [x,x,5,2,x,6,3,x,x]]
        """
        self.startingBoard = inputBoard
    
    def RunSolver(self):
        startingMatrix = self.startingBoard
        startingString = self.MatrixToString(startingMatrix)
        
        print('Attempting to solve this matrix:\n{}\n'.format(startingString))
        
        unassignedLocations = self.FindUnassignedLocations(startingMatrix, self.fillValue)
        
        result, finalMatrix = self.SolveSudoku(startingMatrix, unassignedLocations[:])
        
        if result:
            finalString = self.MatrixToString(finalMatrix)
            print('Solution:\n{}\n'.format(finalString))
            
            self.SolvedBoardAsMatrix = finalMatrix
            self.SolvedBoardAsString = finalString
        else:
            print('Matrix determined to be unsolveable.\n')
            
            self.SolvedBoardAsMatrix = []
            self.SolvedBoardAsString = 'Not Possible'
        
    
    def MatrixToString(self, matrix):
        stringRepresentation = list(map(lambda x: list(map(str, x)), matrix))
        rowStrings = [self.columnSep.join([' '.join(x) for x in (row[:3], row[3:6], row[6:])]).replace(str(self.fillValue), '_') for row in stringRepresentation]
        boardString = ('\n' + self.rowSep).join(['\n'.join(x) for x in (rowStrings[:3], rowStrings[3:6], rowStrings[6:])])
        return boardString
    
    def SolveSudoku(self, grid, unassignedLocations):
        if unassignedLocations:
            row, col = unassignedLocations[0]
            availableNumbers = self.GetAvailableNumbers(grid, row, col)
            
            for num in availableNumbers:
                newGrid = [[v for v in r] for r in grid]
                newGrid[row][col] = num
                       
                result, finalGrid = self.SolveSudoku(newGrid, unassignedLocations[1:])
                
                if result:
                    return result, finalGrid
                
            result = False
        else:
            result = True
        
        return result, grid
    
    def FindUnassignedLocations(self, startingBoard, fillValue):
        unassignedLocations = []
        for rowIdx in range(9):
            for colIdx in range(9):
                if startingBoard[rowIdx][colIdx] == fillValue:
                    unassignedLocations.append((rowIdx, colIdx))
        return unassignedLocations
    
    def GetAvailableNumbers(self, grid, row, col):
        availableNumbers = set(range(1,10))
        square = 3 * (row // 3) + (col // 3)
        for rowIdx in range(9):
            for colIdx in range(9):
                squareIdx = 3 * (rowIdx // 3) + (colIdx // 3)
                if rowIdx == row or colIdx == col or squareIdx == square:
                    availableNumbers -= {grid[rowIdx][colIdx]}
        return availableNumbers
    
    def PromptMatrix(self):
        matrix = []
        infoString = 'Nine integer values must be entered for each row.\nValues don\'t have to be separated, but feel free to use a comma or space to do so.\nUse 0 to represent unassigned values.'
        print(infoString)
        for rowIdx in range(9):
            LOOP = True
            while LOOP:
                rowInput = input('Enter the 9 values for row {}:\n'.format(rowIdx))
                try:
                    rowValues = list(map(int, rowInput.replace(',','').replace(' ','')))
                    LOOP = False
                except Exception:
                    print('"{}" is an improper input!'.format(rowInput))
                    print(infoString)
            matrix.append(rowValues)
        self.startingBoard = matrix

if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='store', dest='inputBoard', default=None)
    options = parser.parse_args(sys.argv[1:])
    
    inputBoard = options.inputBoard
    Solver = SudokuSolver()
    if inputBoard:
        # Since the command line inputs get passed in as a string, you have to reformat it to a matrix
        inputMatrix = Solver.StringToMatrix(inputBoard)
        Solver.InputMatrix(inputMatrix)
    else:
        Solver.PromptMatrix()
    
    Solver.RunSolver()
