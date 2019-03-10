import os
import pandas as pd
from assets.tkImport import Tkinter

class highScoresGUI(Tkinter.Tk):
    def __init__(self, options):
        Tkinter.Tk.__init__(self)
        self.options = options
        self.initialize()

    def initialize(self):
        self.options['viewHighScores'] = False

        f = os.path.join(os.path.dirname(__file__), '{}HighScores.pkl')

        lvls = ('Beginner', 'Intermediate', 'Advanced')
        scoreDict = {level: self.GetScores(f.format(level)) for level in lvls}

        numScores = 10

        numCols = 2 * len(lvls)
        numRows = numScores + 3

        self.grid()
        self.configure(bg = 'grey')

        Tkinter.Label(self, textvariable = Tkinter.StringVar(value = 'High Scores'),
                      fg = 'black', bg = 'grey').grid(row = 0, column = 0,
                      columnspan = numCols, sticky = 'EW')

        for i, level in enumerate(lvls):
            Tkinter.Label(self, textvariable = Tkinter.StringVar(value = level),
                          fg = 'black', bg = 'grey').grid(row = 1, column = i * 2,
                          columnspan = 2, sticky = 'EW')

            for idx, row in scoreDict[level].iterrows():
                name, time = row[['Name', 'Time']]

                Tkinter.Label(self, textvariable = Tkinter.StringVar(value = name),
                              fg = 'black', bg = 'grey', anchor = 'w').grid(row = idx + 2,
                              column = i * 2, sticky = 'EW')

                Tkinter.Label(self, textvariable = Tkinter.StringVar(value = '{:.2f}'.format(time)),
                              fg = 'black', bg = 'grey', anchor = 'w').grid(row = idx + 2,
                              column = 1 + i * 2, sticky = 'EW')

        Tkinter.Button(self, textvariable =Tkinter.StringVar(value = 'Menu'),
                       command = self.GoToOptions,
                       fg = 'black', bg = 'grey').grid(row = numScores + 2,
                       column = 1)

        if self.options['level']:
            Tkinter.Button(self, textvariable = Tkinter.StringVar(value = 'Play'),
                           command = self.GoToOptions,
                           fg = 'black', bg = 'grey').grid(row = numScores + 2,
                           column = 3)

        Tkinter.Button(self, textvariable = Tkinter.StringVar(value = 'Quit'),
                       command = self.quit,
                       fg = 'black', bg = 'grey').grid(row = numScores + 2,
                       column = 5)

        for r in range(numRows):
            self.grid_rowconfigure(r, weight = 1)

        for c in range(numCols):
            self.grid_columnconfigure(c, weight = 1)

        self.resizable(True, True)
        self.update()

        self.geometry(self.geometry())

    def PlayGame(self):
        self.options['play'] = True
        self.quit()

    def GoToOptions(self):
        self.options['goToOptions'] = True
        self.quit()

    def GetScores(self, fh):
        if os.path.exists(fh):
            df = pd.read_pickle(fh)
        else:
            df = pd.DataFrame(columns = ['Name', 'Time'])

        return df.sort_values('Time', ascending = True).reset_index(drop = True)
