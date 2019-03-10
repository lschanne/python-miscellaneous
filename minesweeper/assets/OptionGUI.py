import os
from assets.tkImport import Tkinter

class optionGUI(Tkinter.Tk):
    def __init__(self, prev):
        Tkinter.Tk.__init__(self)
        self.initialize(prev)

    def initialize(self, prev):

        self.options = {
                'play': False,
                'viewHighScores': False,
                'goToOptions': False,
                'level': None,
                'highScoreFile': None
                }

        if 'username' in prev:
            self.options['username'] = Tkinter.StringVar(
                                           value = prev['username'].get()
                                       )
        else:
            self.options['username'] = Tkinter.StringVar(
                                            value = os.getlogin()
                                       )

        self.grid()
        self.configure(bg = 'grey')

        s = 'Minesweeper Main Menu'
        Tkinter.Label(self, textvariable = Tkinter.StringVar(value = s),
                      fg = 'black', bg = 'grey'
                      ).grid(column = 0, row = 0, sticky = 'EW',
                              columnspan = 2)

        s = 'username:'
        Tkinter.Label(self, textvariable = Tkinter.StringVar(value = s),
                      anchor = 'e', fg = 'black', bg = 'grey'
                      ).grid(column = 0, row = 1, sticky = 'EW')

        Tkinter.Entry(self, textvariable = self.options['username'],
                      fg = 'black', bg = 'white'
                      ).grid(column = 1, row = 1, sticky = 'EW')

        s = 'Play Game:'
        Tkinter.Label(self, textvariable = Tkinter.StringVar(value = s),
                      anchor = 'e', fg = 'black', bg = 'grey'
                      ).grid(column = 0, row = 2, sticky = 'EW')

        row = 2
        for s,c in zip(('Beginner', 'Intermediate', 'Advanced'),
                       ('green', 'blue', 'black')):
            row += 1
            Tkinter.Button(self, textvariable = Tkinter.StringVar(value = s),
                           anchor = 'w', fg = 'white', bg = c,
                           command = lambda l = s: self.startGame(l)
                           ).grid(column = 1, row = row, sticky = 'EW')

        s = 'View High Scores'
        Tkinter.Button(self, textvariable = Tkinter.StringVar(value = s),
                       anchor = 'e', fg = 'black', bg = 'grey',
                       command = self.viewHighScores
                       ).grid(column = 0, row = row + 1, sticky = 'EW')

        s = 'Quit'
        Tkinter.Button(self, textvariable = Tkinter.StringVar(value = s),
                       anchor = 'e', fg = 'black', bg = 'grey',
                       command = self.quit
                       ).grid(column = 1, row = row + 1, sticky = 'EW')

        self.resizable(False, False)
        self.update()

        for r in range(row + 2):
            self.grid_rowconfigure(r, weight = 1)

        for c in range(2):
            self.grid_columnconfigure(c, weight = 1)

        self.geometry(self.geometry())

    def startGame(self, level):
        f = os.path.join(os.path.dirname(__file__),
                         '{}HighScores.pkl'.format(level))

        self.options['highScoreFile'] = os.path.abspath(f)
        self.options['level']         = level
        self.options['play']          = True

        self.quit()

    def viewHighScores(self):
        self.options['viewHighScores'] = True
        self.quit()
