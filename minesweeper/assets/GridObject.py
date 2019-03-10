from assets.tkImport import Tkinter

IS_MINE, IS_OPEN, ADD_TO_QUEUE = range(3)
MINE_VALUE = 9

# Define the color and string representation for displaying
# each possible number on the game grid
numberFormat = {i: {'color': c, 'string': str(i)} for i, c in enumerate((
                      'white', 'blue', 'green',
                      'red', 'purple', 'brown',
                      'aqua', 'black', 'grey'
                ))}
numberFormat[0]['string'] = ' '
blankStr = ' '
flagStr  = '?'
mineStr  = 'X'

class GridObject:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.string = Tkinter.StringVar()
        self.button = False
        self.reset()

    def reset(self):
        self.value = 0
        self.isMine = False
        self.isOpen = False
        self.isFlag = False
        
        self.string.set(blankStr)
        if self.button:
            self.button.configure(bg = 'grey', fg = 'black')

    def makeButton(self, gameGUI):
        self.button = Tkinter.Button(
                gameGUI,
                textvariable = self.string,
                fg = 'black',
                bg = 'grey'
        )

        self.button.grid(
                row = self.row + gameGUI.rowOffset,
                column = self.column + gameGUI.colOffset,
                sticky = 'EW'
        )

    def makeMine(self, gridMatrix):
        self.value = MINE_VALUE
        self.isMine = True

        nRows, nCols = gridMatrix.shape
        for i in (-1, 0, 1):
            r = self.row + i
            if r < 0 or r >= nRows:
                continue
            for j in (-1, 0, 1):
                c = self.column + j
                if c < 0 or c >= nCols:
                    continue
                if not (i or j):
                    continue
                gridMatrix[r, c].incrementValue()

    def incrementValue(self):
        if not self.isMine:
            self.value += 1

    def open(self, gridMatrix):
        """
        Return True if the game is lost and False otherwise.
        """
        if self.isMine:
            return True
        if self.isOpen:
            return False

        self.string.set(numberFormat[self.value]['string'])
        self.button.configure(
                bg = 'white',
                fg = numberFormat[self.value]['color']
        )
        self.isOpen = True

        if self.value:
            return False

        # If self.value is 0, no mines surround this cell, so we can safely
        # open all surrounding cells
        nRows, nCols = gridMatrix.shape
        for i in (-1, 0, 1):
            r = self.row + i
            if r < 0 or r >= nRows:
                continue
            for j in (-1, 0, 1):
                c = self.column + j
                if c < 0 or c >= nCols:
                    continue
                if not (i or j):
                    continue
                gridMatrix[r, c].open(gridMatrix)

        return False

    def toggleFlag(self, mines):
        if not self.isOpen:
            # toggle the flag state
            self.isFlag = not self.isFlag

            # if the flag has been set, decrement mines
            if self.isFlag:
                mines -= 1
                self.string.set(flagStr)
            # otherwise, increment mines
            else:
                mines += 1
                self.string.set(blankStr)

        return mines

    def revealMine(self):
        assert(self.isMine)
        self.string.set(mineStr)
        self.button.configure(fg = 'black', bg = 'red')
