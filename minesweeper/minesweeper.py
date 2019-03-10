### TODO: debug some translation errors
"""
The classic game of minesweeper.
"""

import assets

def closeGUI(gui):
    try:
        gui.destroy()
    except:
        import sys
        sys.exit()

def getOptions(prev = dict()):
    gui = assets.optionGUI(prev)
    gui.title('Main Menu')
    gui.mainloop()
    closeGUI(gui)
    return gui.options

options = getOptions()

while options['play'] or options['viewHighScores']:
    if options['play']:
        gui = assets.gameGUI(options)
        gui.title('Minesweeper')
        gui.mainloop()
        closeGUI(gui)
        options = gui.options

    if options['viewHighScores']:
        gui = assets.highScoresGUI(options)
        gui.title('High Scores')
        gui.mainloop()
        closeGUI(gui)
        options = gui.options

    if options['goToOptions']:
        options = getOptions(options)
