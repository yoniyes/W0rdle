from english_words import english_words_lower_set
import numpy as np
import random
from termcolor import colored


GREY = 0
YELLOW = 1
GREEN = 2


def getWordList(wordLen=5):
    return [word for word in english_words_lower_set if len(word) == wordLen and "'" not in word]

def chooseWordAtRandom(wordList):
    return random.choice(wordList)

def chooseWordReductionPhaseStrategy(wordList, guessHistory):
    return chooseWordAtRandom(wordList)

def chooseWordPreciseGuessPhaseStrategy(wordList, guessHistory):
    return chooseWordAtRandom(wordList)

def isWordSpaceSmallEnough(currentSize, startSize, factor=0.1):
    return currentSize <= np.ceil(startSize * factor)

def checkGuess(guess, solution):
    result = [GREY for _ in range(len(guess))]
    for i, c in enumerate(guess):
        if c in solution:
            if solution[i] == c:
                result[i] = GREEN
            else:
                result[i] = YELLOW
    return result

def isGuessCorrect(guessEntry):
    guess = guessEntry['guess']
    result = guessEntry['result']
    # print("[DEBUG] Word: " + guess + ", Result: " + str(result))
    for i, color in enumerate(result):
        if color != GREEN:
            return False
    return True

def removeIrrelevantWords(wordList, guessEntry):
    guess = guessEntry['guess']
    result = guessEntry['result']
    for i in range(len(guess)):
        if result[i] == GREY:
            # Solution doesn't contain the letter.
            wordList = list(filter(lambda word: guess[i] not in word, wordList))
        elif result[i] == GREEN:
            # Solution contains the letter, and in a specific index.
            wordList = list(filter(lambda word: word[i] == guess[i], wordList))
        elif result[i] == YELLOW:
            # Solution contains the letter, but not in the current index.
            wordList = list(filter(lambda word: word[i] != guess[i], wordList))
        else:
            assert('how did we get here?')
    return wordList

def printResults(guessHistory):
    for turn in guessHistory:
        idx = 0
        for res in turn['result']:
            if res == GREEN:
                print(colored(turn['guess'].upper()[idx], 'green'), end=' ')
            elif res == YELLOW:
                print(colored(turn['guess'].upper()[idx], 'yellow'), end=' ')
            else:
                print(colored(turn['guess'].upper()[idx], 'white'), end=' ')
            idx += 1
        print()

wordLength = 5
maxGuesses = 6
totalGuesses = 0
maxReductionGuessesPhaseLength = 3

wordList = getWordList()
startSize = len(wordList)
solution = chooseWordAtRandom(wordList)
guessHistory = [{'guess': '', 'result': []} for _ in range(maxGuesses)]

# Solution space size reduction phase
reductionPhaseTurnCount = 0
for turn in range(maxReductionGuessesPhaseLength):
    if isWordSpaceSmallEnough(len(wordList), startSize):
        break

    reductionPhaseTurnCount += 1
    totalGuesses = reductionPhaseTurnCount
    guessHistory[turn]['guess'] = chooseWordReductionPhaseStrategy(wordList, guessHistory[:turn])
    guessHistory[turn]['result'] = checkGuess(guessHistory[turn]['guess'], solution)
    if isGuessCorrect(guessHistory[turn]):
        printResults(guessHistory)
        # print("[INFO]\t Guess #" + str(totalGuesses) + ": " + guessHistory[turn]['guess'].upper() + " correct! YOU WON!")
        exit(0)
    # print("[INFO]\t Guess #" + str(totalGuesses) + ": " + guessHistory[turn]['guess'].upper() + " incorrect...")
    wordList = removeIrrelevantWords(wordList, guessHistory[turn])

# Precise guess phase
maxPreciseGuessesPhaseLength = maxGuesses - reductionPhaseTurnCount
preciseGuessPhaseTurnCount = 0
for _ in range(maxPreciseGuessesPhaseLength):
    preciseGuessPhaseTurnCount += 1
    totalGuesses += 1

    guessHistory[totalGuesses-1]['guess'] = chooseWordPreciseGuessPhaseStrategy(wordList, guessHistory[:totalGuesses])
    guessHistory[totalGuesses-1]['result'] = checkGuess(guessHistory[totalGuesses-1]['guess'], solution)
    if isGuessCorrect(guessHistory[totalGuesses-1]):
        printResults(guessHistory)
        # print("[INFO]\t Guess #" + str(totalGuesses) + ": " + guessHistory[totalGuesses-1]['guess'].upper() + " correct! YOU WON!")
        exit(0)
    # print("[INFO]\t Guess #" + str(totalGuesses) + ": " + guessHistory[totalGuesses-1]['guess'].upper() + " incorrect...")
    wordList = removeIrrelevantWords(wordList, guessHistory[totalGuesses-1])

printResults(guessHistory)
print("[INFO]\t GAME OVER... solution is " + solution)
exit(1)

