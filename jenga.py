# 2x2 with lists

import random


""" faces are 
# R green
# U white
# D yellow
# F red 
# B magenta
# L blue
"""
green = u"\u001b[32m#\u001b[0m"
blue = u"\u001b[34m#\u001b[0m"

red = u"\u001b[31m#\u001b[0m"
magenta = u"\u001b[35m#\u001b[0m"

yellow = u"\u001b[33m#\u001b[0m"
white = u"\u001b[37m#\u001b[0m"


# all corners
A = ["RUF", [green, white, red] ]
B = ["BUR", [magenta, white, green] ]
C = ["LUB", [blue, white, magenta] ]
D = ["FUL", [red, white, blue] ]
E = ["FDR", [red, yellow, green] ]
F = ["RDB", [green, yellow, magenta] ]
G = ["BDL", [magenta, yellow, blue] ]
H = ["LDF", [blue, yellow, red] ]

# all face pieces
U = []
V = []
W = []
X = []
Y = []
Z = []

# 0 for faces, 1 for colors
def print_cube(i):
    # B
    print("   ", F[i][2], G[i][0], "         ", C[i][2], B[i][0])
    print("   ", B[i][0], C[i][2], "         ", G[i][0], F[i][2])
    print("")
    # R U L D
    print(B[i][2], " ", B[i][1], C[i][1], "  ", C[i][0], G[i][2], "  ", G[i][1], F[i][1], " ",  F[i][0])
    print(A[i][0], " ", A[i][1], D[i][1], "  ", D[i][2], H[i][0], "  ", H[i][1], E[i][1], " ", E[i][2])
    # F
    print("")
    print("   ", A[i][2], D[i][0], "         ", H[i][2], E[i][0])
    print("   ", E[i][0], H[i][2], "         ", D[i][0], A[i][2])
    print("")
    print("")



# consider clockwise vs anticlockwise
def permute(top, right, bottom, left):
    return (right, bottom, left, top)



def counterpermute(top, right, bottom, left):
    return (left, top, right, bottom)


refer = { "R": [A[1][0], E[1][2], F[1][0], B[1][2]] }


# a copypasta mess but it works...
def rotate(char):
    # A E F B
    if char == "R":
        (A[1][0], E[1][2], F[1][0], B[1][2]) = permute(A[1][0], E[1][2], F[1][0], B[1][2])
        (A[1][1], E[1][0], F[1][1], B[1][0]) = permute(A[1][1], E[1][0], F[1][1], B[1][0])
        (A[1][2], E[1][1], F[1][2], B[1][1]) = permute(A[1][2], E[1][1], F[1][2], B[1][1])
    elif char == "r":
        (A[1][0], E[1][2], F[1][0], B[1][2]) = counterpermute(A[1][0], E[1][2], F[1][0], B[1][2])
        (A[1][1], E[1][0], F[1][1], B[1][0]) = counterpermute(A[1][1], E[1][0], F[1][1], B[1][0])
        (A[1][2], E[1][1], F[1][2], B[1][1]) = counterpermute(A[1][2], E[1][1], F[1][2], B[1][1])

    # A B C D
    elif char == "U":
        (A[1][1], B[1][1], C[1][1], D[1][1]) = permute(A[1][1], B[1][1], C[1][1], D[1][1])
        (A[1][0], B[1][0], C[1][0], D[1][0]) = permute(A[1][0], B[1][0], C[1][0], D[1][0])
        (A[1][2], B[1][2], C[1][2], D[1][2]) = permute(A[1][2], B[1][2], C[1][2], D[1][2])
    elif char == "u":
        (A[1][1], B[1][1], C[1][1], D[1][1]) = counterpermute(A[1][1], B[1][1], C[1][1], D[1][1])
        (A[1][0], B[1][0], C[1][0], D[1][0]) = counterpermute(A[1][0], B[1][0], C[1][0], D[1][0])
        (A[1][2], B[1][2], C[1][2], D[1][2]) = counterpermute(A[1][2], B[1][2], C[1][2], D[1][2])

    # A D H E
    elif char == "F":
        (A[1][2], D[1][0], H[1][2], E[1][0]) = permute(A[1][2], D[1][0], H[1][2], E[1][0])
        (A[1][1], D[1][2], H[1][1], E[1][2]) = permute(A[1][1], D[1][2], H[1][1], E[1][2])
        (A[1][0], D[1][1], H[1][0], E[1][1]) = permute(A[1][0], D[1][1], H[1][0], E[1][1])
    elif char == "f":
        (A[1][2], D[1][0], H[1][2], E[1][0]) = counterpermute(A[1][2], D[1][0], H[1][2], E[1][0])
        (A[1][1], D[1][2], H[1][1], E[1][2]) = counterpermute(A[1][1], D[1][2], H[1][1], E[1][2])
        (A[1][0], D[1][1], H[1][0], E[1][1]) = counterpermute(A[1][0], D[1][1], H[1][0], E[1][1])

    # D C G H
    elif char == "L":
        (D[1][1], C[1][2], G[1][1], H[1][2]) = permute(D[1][1], C[1][2], G[1][1], H[1][2])
        (D[1][2], C[1][0], G[1][2], H[1][0]) = permute(D[1][2], C[1][0], G[1][2], H[1][0])
        (D[1][0], C[1][1], G[1][0], H[1][1]) = permute(D[1][0], C[1][1], G[1][0], H[1][1])
    elif char == "l":
        (D[1][1], C[1][2], G[1][1], H[1][2]) = counterpermute(D[1][1], C[1][2], G[1][1], H[1][2])
        (D[1][2], C[1][0], G[1][2], H[1][0]) = counterpermute(D[1][2], C[1][0], G[1][2], H[1][0])
        (D[1][0], C[1][1], G[1][0], H[1][1]) = counterpermute(D[1][0], C[1][1], G[1][0], H[1][1])

    # E F G H
    elif char == "D":
        (E[1][0], F[1][0], G[1][0], H[1][0]) = permute(E[1][0], F[1][0], G[1][0], H[1][0])
        (E[1][1], F[1][1], G[1][1], H[1][1]) = permute(E[1][1], F[1][1], G[1][1], H[1][1])
        (E[1][2], F[1][2], G[1][2], H[1][2]) = permute(E[1][2], F[1][2], G[1][2], H[1][2])
    elif char == "d":
        (E[1][0], F[1][0], G[1][0], H[1][0]) = counterpermute(E[1][0], F[1][0], G[1][0], H[1][0])
        (E[1][1], F[1][1], G[1][1], H[1][1]) = counterpermute(E[1][1], F[1][1], G[1][1], H[1][1])
        (E[1][2], F[1][2], G[1][2], H[1][2]) = counterpermute(E[1][2], F[1][2], G[1][2], H[1][2])

    # B F G C
    elif char == "B":
        (B[1][0], F[1][2], G[1][0], C[1][2]) = permute(B[1][0], F[1][2], G[1][0], C[1][2])
        (B[1][1], F[1][0], G[1][1], C[1][0]) = permute(B[1][1], F[1][0], G[1][1], C[1][0])
        (B[1][2], F[1][1], G[1][2], C[1][1]) = permute(B[1][2], F[1][1], G[1][2], C[1][1])
    elif char == "b":
        (B[1][0], F[1][2], G[1][0], C[1][2]) = counterpermute(B[1][0], F[1][2], G[1][0], C[1][2])
        (B[1][1], F[1][0], G[1][1], C[1][0]) = counterpermute(B[1][1], F[1][0], G[1][1], C[1][0])
        (B[1][2], F[1][1], G[1][2], C[1][1]) = counterpermute(B[1][2], F[1][1], G[1][2], C[1][1])




def scramble(num = 10):
    for i in range(num):
        possible = ["U", "u", "R", "r", "F", "f", "D", "d", "L", "l", "B", "b"]
        turn = random.choice(possible)
        rotate(turn)



def play():
    print_cube(1)
    scramble(5)
    while(True):
        print_cube(1)
        call = input("next move: ")
        if len(call) == 1:
            rotate(call)
        else:
            return 0


def change(er):
    er[0] = "hello my beutiful world"

p = [1, 2, 3]

print(p)
change(p)
print(p)
play()

# features to consider:
# 3x3 mode, sudoku mode, solve, reset/set, undo