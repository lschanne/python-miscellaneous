import assets.GameFunctions as GF
import numpy as np
import os
import pandas as pd
import time
from assets.tkImport import Tkinter

class gameGUI(Tkinter.Tk):
    def __init__(self, options):
        Tkinter.Tk.__init__(self)

        self.options = options
        self.options['play'] = False

        self.game = GF.generateGame(self.options)
        self.formatHeaderFooter()

        self.initialize()

    def formatHeaderFooter(self):
        """
        Create a dictionary with settings for how Tkinter should format
        the header and footer sections of the game GUI.
        """

        # Build the header and footer settings to surround the game grid
        self.headerKeys = []
        self.footerKeys = []
        self.formatDict = {}

        key = 'TimeWord'
        self.headerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Label',
                'Label': {
                    'textvariable': Tkinter.StringVar(value = 'Time'),
                    'anchor': 'w',
                    'fg': 'black',
                    'bg': 'grey'
                },
                'Grid': {
                    'columnspan': 2
                }
        }

        key = 'TimeVariant'
        self.time = Tkinter.StringVar(value = '0000')
        self.headerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Label',
                'Label': {
                    'textvariable': self.time,
                    'anchor': 'w',
                    'fg': 'red',
                    'bg': 'black'
                },
                'Grid': {
                    'columnspan': 3
                }
        }

        key = 'GameStatus'
        self.gameStatus = Tkinter.StringVar(value = 'XXXXXXXX')
        self.headerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Label',
                'Label': {
                    'textvariable': self.gameStatus,
                    'fg': 'white',
                    'bg': 'black'
                },
                'Grid': {
                    'columnspan': 3
                }
        }

        key = 'MineVariant'
        self.activeMines = Tkinter.StringVar(value = '0000')
        self.headerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Label',
                'Label': {
                    'textvariable': self.activeMines,
                    'anchor': 'e',
                    'fg': 'red',
                    'bg': 'black'
                },
                'Grid': {
                    'columnspan': 3
                }
        }

        key = 'MineWord'
        self.headerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Label',
                'Label': {
                    'textvariable': Tkinter.StringVar(value = 'Mines'),
                    'anchor': 'e',
                    'fg': 'black',
                    'bg': 'grey'
                },
                'Grid': {
                    'columnspan': 2
                }
        }

        for idx, key in enumerate(self.headerKeys):
            # all the header is on one row
            self.formatDict[key]['Grid']['row'] = 0
            self.formatDict[key]['Grid']['sticky'] = 'EW'
            if idx:
                # space out each header component based on the size and
                # location of the last one
                prevGrid = self.formatDict[self.headerKeys[idx - 1]]['Grid']
                self.formatDict[key]['Grid']['column'] = (
                        prevGrid['column'] + prevGrid['columnspan']
                )
            else:
                # of course the first one will just start on the left
                self.formatDict[key]['Grid']['column'] = 0

        # Determine the number of columns occupied by the header and decide
        # if the header or the game grid need to be centered
        finalGrid = self.formatDict[self.headerKeys[-1]]['Grid']
        headerCols = finalGrid['column'] + finalGrid['columnspan']
        if self.game['nCols'] > headerCols:
            headerOffset = (self.game['nCols'] - headerCols) // 2
            self.colOffset = 0
        else:
            headerOffset = 0
            self.colOffset = (headerCols - self.game['nCols']) // 2
        if headerOffset:
            for key in self.headerKeys:
                self.formatDict[key]['Grid']['column'] += headerOffset

        # The header only consists of 1 row, so just hardcode that bad boy
        self.rowOffset = 1
        self.totCols = self.colOffset + self.game['nCols']
        self.totRows = self.rowOffset + self.game['nRows']

        key = 'HighScore'
        self.highScoreText = Tkinter.StringVar()
        self.footerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Label',
                'Label': {
                    'textvariable': self.highScoreText,
                    'anchor': 'w',
                    'fg': 'blue',
                    'bg': 'grey'
                }
        }

        key = 'BootText'
        self.bootText = Tkinter.StringVar()
        self.footerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Label',
                'Label': {
                    'textvariable': self.bootText,
                    'anchor': 'w',
                    'fg': 'blue',
                    'bg': 'grey'
                }
        }

        key = 'StartGame'
        self.footerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Button',
                'Label': {
                    'textvariable': Tkinter.StringVar(value = 'Restart Game'),
                    'command': self.StartGame,
                    'fg': 'black',
                    'bg': 'grey'
                }
        }

        key = 'HighScores'
        self.footerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Button',
                'Label': {
                    'textvariable': Tkinter.StringVar(value = 'High Scores'),
                    'command': self.ViewHighScores,
                    'fg': 'black',
                    'bg': 'grey'
                }
        }

        key = 'MainMenu'
        self.footerKeys.append(key)
        self.formatDict[key] = {
                'Type': 'Button',
                'Label': {
                    'textvariable': Tkinter.StringVar(value = 'Main Menu'),
                    'command': self.GoToOptions,
                    'fg': 'black',
                    'bg': 'grey'
                }
        }

        for key in self.footerKeys:
            self.formatDict[key]['Grid'] = {
                    'columnspan': self.totCols,
                    'sticky': 'EW',
                    'column': 0,
                    'row': self.totRows
            }
            self.totRows += 1

    def makeHeaderFooter(self, keys):
        for key in keys:
            tkType = self.formatDict[key]['Type']
            gridKwargs = self.formatDict[key]['Grid']
            labelKwargs = self.formatDict[key]['Label']

            if tkType == "Label":
                construct = Tkinter.Label
            elif tkType == "Button":
                construct = Tkinter.Button
            else:
                raise ValueError("Unknown type {type} for {key}".format(
                    type = tkType, key = key))

            construct(self, **labelKwargs).grid(**gridKwargs)


    def initialize(self):
        # Make the header and footer
        self.grid()
        self.configure(bg = 'grey')
        self.makeHeaderFooter(self.headerKeys)
        self.makeHeaderFooter(self.footerKeys)

        
        # Make the minefield
        for row in self.game['gridMatrix']:
            for gridObject in row.A1:
                gridObject.makeButton(self)

        # Assign left-click and right-click commands
        self.bind_all('<Button-1>', self.MakeMove)
        self.bind_all('<Button-2>', self.ToggleFlag)
        # These two for laptop support
        self.bind_all('<Command-Button-1>', self.ToggleFlag)
        self.bind_all('<Control-Button-1>', self.ToggleFlag)

        # Some GUI formatting
        self.resizable(True, True)
        for c in range(self.totCols):
            self.grid_columnconfigure(c, weight = 1)
        for r in range(self.totRows):
            self.grid_rowconfigure(r, weight = 1)
        self.update()
        self.geometry(self.geometry())

        # Start the game already
        self.StartGame()

    def StartGame(self):
        self.play = True
        self.loss = False
        for row in self.game['gridMatrix']:
            for gridObject in row.A1:
                gridObject.reset()

        self.game = GF.populateMines(self.game)

        self.activeMines.set(str(self.game['nMines']))
        self.highScoreText.set('')
        self.bootText.set('')

        self.startTime = time.time()
        self.PlayGame()

    def PlayGame(self):
        if self.play:
            t = time.time() - self.startTime
            self.time.set('{:3.0f}'.format(min([999, int(t)])))
            if self.loss:
                self.play = False
                self.GameOver()
            elif GF.checkVictory(self.game):
                self.play = False
                self.Victory(t)
            else:
                self.after(50, self.PlayGame)

    def GetGridSpace(self, event):
        info = event.widget.grid_info()
        row = int(info['row']) - self.rowOffset
        col = int(info['column']) - self.colOffset

        # Make sure it's a tile on the minefield
        isIn = not (row < 0 or row - 1 > self.game['nRows'] or
                    col < 0 or col - 1 > self.game['nCols'])

        return (row, col, isIn)

    def ToggleFlag(self, event):
        row, col, isIn = self.GetGridSpace(event)
        if not isIn:
            return

        mines = int(self.activeMines.get())
        mines = self.game['gridMatrix'][row, col].toggleFlag(mines)
        self.activeMines.set(str(mines))

    def MakeMove(self, event):
        if self.play:
            row, col, isIn = self.GetGridSpace(event)
            if not isIn:
                return

            self.loss = self.game['gridMatrix'][row, col].open(
                    self.game['gridMatrix'])
            
    def GameOver(self):
        self.highScoreText.set('You can\'t set any high scores by losing!')
        self.bootText.set('Next time try using your brain!')
        self.gameStatus.set('You Lose!')
        for r, c in self.game['mineLocations']:
            self.game['gridMatrix'][r, c].revealMine()

    def Victory(self, time):
        self.gameStatus.set('You win!')

        # Number of high scores to maintain
        numScores = 10
        f = ['1st', '2nd', '3rd'] + ['{}th'.format(x) for x in range(4, numScores + 1)]

        if os.path.exists(self.options['highScoreFile']):
            df = pd.read_pickle(self.options['highScoreFile'])
        else:
            df = pd.DataFrame(columns = ['Name', 'Time'])

        place = (df['Time'] <= time).sum()
        if place < numScores:
            df = df.append(pd.DataFrame({'Name': [self.options['username'].get()],
                                         'Time': [time]}), ignore_index = True)
            df = df.sort_values('Time', ascending = True).reset_index(drop = True)

            self.highScoreText.set('Congrats! You got the {} place score!'.format(f[place]))

            if len(df) > place + 1:
                n,t = df.loc[place + 1][['Name', 'Time']]
                self.bootText.set('You beat {} with a time of {:.2f}'.format(n,t))
            else:
                self.bootText.set('But you didn\'t actually beat anyone.')

            df.iloc[:numScores].to_pickle(self.options['highScoreFile'])
            os.system('chmod 666 {}'.format(self.options['highScoreFile']))

        else:
            self.highScoreText.set('If you thought that time would set a high score')
            self.bootText.set('then you were not right.')

    def ViewHighScores(self):
        self.options['viewHighScores'] = True
        self.quit()

    def GoToOptions(self):
        self.options['goToOptions'] = True
        self.quit()

