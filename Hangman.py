"""
The classic game of hangman.
"""

import argparse
import random
import sys
import time

if sys.version_info.major == 3:
    raw_input = input

class Hangman:
    def __init__(self, inputs):

        # This character is to be used to separate multiple words
        self.space = '/'

        # These are the words that will be randomly picked from if no word is specified
        self.wordBank = {'sty', 'wry', 'yew', 'oar', 'hen', 'zap', 'tin',
                         'whom', 'stew', 'knew', 'slap', 'hymn',
                         'fluke', 'crack'}

        self.parseArgs(inputs)

    def parseArgs(self, inputs):
        parser = argparse.ArgumentParser()

        parser.add_argument('-w', '-word', action='store', dest='word', default=None, help='The word to play with.')
        parser.add_argument('-l', '-lives', action='store', dest='lives', default='6', help='Number of lives to play with.')

        options = parser.parse_args(inputs)

        lives = options.lives
        while not lives.isdigit():
            lives = raw_input('Please enter a valid integer number of lives to play with.\n')

        self.lives = int(lives)

        if options.word:
            self.word = options.word.replace(' ', self.space)
            while any(not (char.islpha() or char == ' ') for char in self.word):
                print('\n{} is an invalid word to play with!'.format(self.word))
                print('Please enter a word with only letters and spaces.')
                inpt = raw_input('Enter a blank input to use the default word bank.\n')
                if inpt:
                    self.word = inpt
                else:
                    self.word = random.choice(list(self.wordBank))
                    return
        else:
            self.word = random.choice(list(self.wordBank))

    def playGame(self):

        self.startingCredits()

        self.status = []
        self.guessedLetters = set()
        self.missedLetters = []
        self.currentWord = []

        for char in self.word:
            if char == ' ':
                self.status.append(1)
                self.currentWord.append(self.space)
            else:
                self.status.append(0)
                self.currentWord.append('_')

        self.gameLoop()

        inpt = raw_input('\nWould you like to play gain? [y/n]\n')
        playAgain = inpt[:3].lower() in ('y', 'yes')

        if playAgain:
            self.wordBank -= {self.word}
            print('\nGood choice. This game is fun.')
            print('You may set the word and lives flags to new values if you want.')
            inpt = raw_input('Set flags or leave blank to use defaults.\n')
            self.parseArgs(inpt.split())
            self.playGame()
        else:
            print('\nGoodbye and good riddance.')

    @staticmethod
    def startingCredits():

        def sleep():
            time.sleep(.5)

        print('\n\n\n\n\n')
        sleep()
        print("----------------------------------------")
        sleep()
        print("----------------------------------------")
        sleep()
        print("---------------   Let's   --------------")
        sleep()
        print("---------------  play     --------------")
        sleep()
        print("--------------- hangman!  --------------")
        sleep()
        print("----------------------------------------")
        sleep()
        print("----------------------------------------")
        sleep()
        print("------------------Brought to you by-----")
        sleep()
        print("-----------------------Luke Schanne-----")
        sleep()
        print("----------------------------------------")
        sleep()
        print("----------------------------------------")
        sleep()
        print('\n\n\n\n\n')

    def gameLoop(self):
        print('Lives remaining: {}'.format(self.lives))
        print('Letters guessed: {}'.format(', '.join(self.missedLetters)))
        print('Word: {}'.format(' '.join(self.currentWord)))

        inpt = raw_input('Guess some letter(s):\n')

        for char in inpt.lower():
            if char.isalpha():
                if char in self.guessedLetters:
                    print('{} has already been guessed!\n'.format(char))
                else:
                    self.guessedLetters |= {char}
                    inWord = False
                    for idx, wordChar in enumerate(self.word):
                        if wordChar.lower() == char:
                            self.status[idx] = 1
                            self.currentWord[idx] = wordChar
                            inWord = True

                    if inWord:
                        print('Congratulations! {} is in the word.\n'.format(char))
                        if all(self.status):
                            print('\nThe word is: {}'.format(self.word))
                            self.printWin()
                            return

                    else:
                        print('You wish! {} is not in the word.\n'.format(char))
                        self.lives -= 1
                        self.missedLetters.append(char)
                        if self.lives == 0:
                            self.printLoss()
                            return

            else:
                print('{} is not a valid letter!\n'.format(char))

        self.gameLoop()

    @staticmethod
    def printWin():
        print("\n\nCongratulatioN! You won!")
        print("Luke Schanne would like to personally congratulate you for being able to win a children's game!")

    @staticmethod
    def printLoss():
        print('\n\nYou loser!\nTake your broke ass home!')

if __name__ == '__main__':
    import sys
    game = Hangman(sys.argv[1:])
    game.playGame()
