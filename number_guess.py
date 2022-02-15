# the goal of this game is to guess a number in a set of turns
# each guess will tell the correct digits and whether they are in the right place

import random

answer = str(random.randint(1000000000, 9999999999))
instructions = """
Play a number guesing game!
try to guess a specific 10 digit number using random number guesses
each randomized roll will tell whether the answer contains a digit and
whether that digit is in the correct position
try to guess the answer with as few rolls as possible
x - not in answer
o - in answer but incorrect location
* - in answer and in correct location
"""
ready = False
rolls = 0

# start game
print(instructions)

# mid game
while not ready:
    rolls += 1
    roll = str(random.randint(1000000000, 9999999999))
    print(roll)
    matches = ""
    for i in range(10):
        if roll[i] == answer[i]:
            matches += "*"
        elif roll[i] in answer:
            matches += "o"
        else:
            matches += "x"
    print(matches)
    ready = input("Ready to answer? text=yes blank=no:")

# end game
guess = input("your exact guess: ")
if answer == guess:
    print("You win!, number of guesses needed:", rolls)
else:
    print("Nice try, actual number:", answer)