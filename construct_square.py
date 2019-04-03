"""
Problem:
Given a string consisting of lowercase English letters, find the largest square number which can be obtained by reordering
the string's characters and replacing them with any digits you need (leading zeros are not allowed) where the same characters
always map to the same digits and different characters always map to different digits.

If there is no solution, return -1.

Examples:
s = "ab"
constructSquare(s) = 81

s = "zzz"
constructSquare(s) = -1

s = "aba"
constructSquare(s) = 900
"""

def constructSquare(s):
    counts = getCounts(s)
    
    squareSet = getSquares(len(s) - 1)
    
    maxMatch = getMatches(counts, squareSet)
    
    return maxMatch

def getCounts(s):
    countDict = {}
    for char in s:
        if char in countDict:
            countDict[char] += 1
        else:
            countDict[char] = 1
    
    return sorted(countDict.values())

def getSquares(l):
    squareSet = []
    min_ = 10 ** l
    max_ = 10 * min_ - 1
    root = int(min_ ** .5)
    
    while 1:
        root += 1
        square = root * root
        
        if square > max_:
            return squareSet
        
        squareSet.append(square)

def getMatches(counts, squareSet):
    for square in reversed(squareSet):
        numStr = str(square)
        if getCounts(numStr) == counts:
            return square
    return -1

if __name__ == '__main__':
    for input_, answer in zip(("ab", "zzz", "aba"), (81, -1, 900)):
        assert(constructSquare(input_) == answer)
