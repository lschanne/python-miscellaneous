"""
This module will define a few functions that are used to permute the characters in a string.
"""

def BasicPermutation(inputString, inputList = [], currentString = ''):
    """
    This method will list all permutations of the characters in the given string.
    """
    listOfPermutations = inputList[:]
    if inputString:
        for characterIndex in range(len(inputString)):
            currentCharacter = inputString[characterIndex]
            remainingCharacters = inputString[:characterIndex] + inputString[characterIndex + 1:]
            newString = currentString + currentCharacter
            listOfPermutations = BasicPermutation(remainingCharacters, listOfPermutations, newString)
    else:
        listOfPermutations.append(currentString)
    return listOfPermutations

def IncludeSubsets(inputString, inputList = [], currentString = ''):
    """
    This method will list all permutations of the characters in the given string as well as the permutations of all subsets of the characters (that include at least one character) in the given string.
    """
    listOfPermutations = inputList[:]
    if inputString:
        for i in range(len(inputString)):
            currentCharacter = inputString[i]
            remainingCharacters = inputString[:i] + inputString[i + 1:]
            newString = currentString + currentCharacter
            listOfPermutations = IncludeSubsets(remainingCharacters, listOfPermutations, newString)
            listOfPermutations = IncludeSubsets(remainingCharacters, listOfPermutations, currentString)
    elif currentString:
        listOfPermutations.append(currentString)
    return listOfPermutations

"""
At this point the astute members of the audience will notice that there is no protection from repeat instances of permutations in the output lists of these two methods.
These repeats could be potentially very annoying and a waste of computational power if they are not desired. With that in mind, let's create some new methods.
"""

def PermutationWithoutRepeat(inputString, inputList = [], currentString = ''):
    """
    This method will list all permutations (without repeat) of the characters in the given string.
    """
    listOfPermutations = inputList[:]
    if inputString:
        characterSet = set(inputString)
        for currentCharacter in characterSet:
            characterIndex = inputString.index(currentCharacter)
            remainingCharacters = inputString[:characterIndex] + inputString[characterIndex + 1:]
            newString = currentString + currentCharacter
            listOfPermutations = PermutationWithoutRepeat(remainingCharacters, listOfPermutations, newString)
    else:
        listOfPermutations.append(currentString)
    return listOfPermutations

def IncludeSubsetsWithoutRepeat(inputString, inputSet = set(), currentString = ''):
    """
    This method will list all permutations (without repeat) of the characters in the given string as well as the permutations of all subsets of the characters (that include at least one character) in the given string.
    """
    setOfPermutations = inputSet.copy()
    if inputString:
        characterSet = set(inputString)
        for currentCharacter in characterSet:
            characterIndex = inputString.index(currentCharacter)
            remainingCharacters = inputString[:characterIndex] + inputString[characterIndex + 1:]
            newString = currentString + currentCharacter
            setOfPermutations = IncludeSubsetsWithoutRepeat(remainingCharacters, setOfPermutations, newString)
            setOfPermutations = IncludeSubsetsWithoutRepeat(remainingCharacters, setOfPermutations, currentString)
    elif currentString:
        setOfPermutations |= {currentString}
    return setOfPermutations
