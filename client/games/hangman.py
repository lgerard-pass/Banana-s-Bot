from client.constants import words
import random

def selectWord():
    index = random.randint(0, len(words))
    return words[index]

def hang_check(message):
    if message.content.isalpha() and len(message.content)==1:
        return True
    else:
        return False


def get_revealed_word(word, found_letters):
    revealed_word = ""
    for letter in word:
        if letter in found_letters:
            revealed_word += letter
        else:
            revealed_word += "*"
    return revealed_word


def evaluate_game(word,revealedWord,remaining_tries):
    if word==revealedWord:
        lost = False
        won = True
    elif remaining_tries <= 0:
        lost = True
        won = False
    else:
        lost = False
        won = False
    return won, lost