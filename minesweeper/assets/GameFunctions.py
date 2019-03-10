import numpy as np
from assets.GridObject import GridObject

def generateGame(options):
    levelDict = {
            'Beginner': {'nRows': 6, 'nCols': 6, 'nMines': 4},
            'Intermediate': {'nRows': 10, 'nCols': 10, 'nMines': 15},
            'Advanced': {'nRows': 16, 'nCols': 16, 'nMines': 45}
    }

    game = levelDict[options['level']]
    game['gridMatrix'] = np.matrix(
            [[GridObject(row, column) for column in range(game['nCols'])]
                for row in range(game['nRows'])]
    )
    
    return game

def populateMines(game):
    # For debugging, set the seed for reproducibility
    # np.random.seed(1)
    game['mineLocations'] = []
    for spot in np.random.choice(range(game['nRows'] * game['nCols']),
            size = game['nMines'], replace = False):
        row = spot // game['nCols']
        col = spot %  game['nCols']
        game['mineLocations'].append((row, col))
        game['gridMatrix'][row, col].makeMine(game['gridMatrix'])

    return game

def checkVictory(game):
    for row in game['gridMatrix']:
        for gridObject in row.A1:
            if not gridObject.isMine and not gridObject.isOpen:
                return False
    return True
