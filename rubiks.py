# 2x2 with lists

import random
import numpy


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
A = { "R":green, "U":white, "F":red }
B = { "B":magenta, "U":white, "R":green }
C = { "L":blue, "U":white, "B":magenta }
D = { "F":red, "U":white, "L":blue }
E = { "F":red, "D":yellow, "R":green }
F = { "R":green, "D":yellow, "B":magenta }
G = { "B":magenta, "D":yellow, "L":blue }
H = { "L":blue, "D":yellow, "F":red }


# all face pieces
U = []
V = []
W = []
X = []
Y = []
Z = []

# represent as a 3d array
cube = [ [[A], [B]], 
        [[C], [D]], 
        [[E], [F]], 
        [[G], [H]] ]



# 0 for faces, 1 for colors
def print_cube():
    # B
    print("   ", F[2], G[0], "         ", C[1], B[0])
    print("   ", B[0], C[2], "         ", G[0], F[2])
    print("")
    # R U L D
    print(B[2], " ", B[1], C[1], "  ", C[0], G[2], "  ", G[1], F[1], " ",  F[0])
    print(A[0], " ", A[1], D[1], "  ", D[2], H[0], "  ", H[1], E[1], " ", E[2])
    # F
    print("")
    print("   ", A[2], D[0], "         ", H[2], E[0])
    print("   ", E[0], H[2], "         ", D[0], A[2])
    print("")
    print("")



# consider clockwise vs anticlockwise
def clean_permute(t, r, b, l):
    t[0] = r[0]
    r[0] = b[0]
    b[0] = l[0]
    l[0] = holder
    holder = t[1]
    t[1] = r[1]
    r[1] = b[1]
    b[1] = l[1]
    l[1] = holder
    holder = t[2]
    t[2] = r[2]
    r[2] = b[2]
    b[2] = l[2]
    l[2] = holder


def permute(top, right, bottom, left):
    top[0] = right[0]
    return (right, bottom, left, top)



def counterpermute(top, right, bottom, left):
    return (left, top, right, bottom)


faces = { "R": [A, E, F, B],
            "r": [A, E, F, B],
            "U": [] }


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
    print_cube()
    scramble(5)
    while(True):
        print_cube()
        call = input("next move: ")
        if len(call) == 1:
            rotate(call)
        else:
            return 0





# features to consider:
# 3x3 mode, sudoku mode, solve, reset/set, undo

"""
Moving into a 3x3 cube requires more classes, one for each piece and
one for the total cube
Rotations will require a bit of matrix algebra using numpy and rotation matrices

"""

# CONSTANTS
X_CLOCKWISE = [ [1, 0, 0], [0, 0, -1], [0, 1, 0] ]
Y_CLOCKWISE = [ [0, 0, 1], [0, 1, 0], [-1, 0, 0] ]
Z_CLOCKWISE = [ [0, -1, 0], [1, 0, 0], [0, 0, 1] ]

X_REVERSE = [ [1, 0, 0], [0, 0, 1], [0, -1, 0] ]
Y_REVERSE = [ [0, 0, -1], [0, 1, 0], [1, 0, 0] ]
Z_REVERSE = [ [0, 1, 0], [-1, 0, 0], [0, 0, 1] ]


class Cube_Piece:
    # defined by x, y, and z vectors
    vectors = [0, 0, 0]
    colors = [0, 0, 0]

    def __init__(self, direction, color_set):
        self.vectors = direction
        self.colors = color_set

    def x_permute(self, ANGLE):
        self.vectors = numpy.dot(ANGLE, self.vectors)
        # swap y and z regardless of the direction of rotation
        self.colors = [self.colors[0], self.colors[2], self.colors[1]]


    def y_permute(self, ANGLE):
        self.vectors = numpy.dot(ANGLE, self.vectors)
        # swap x and z
        self.colors = [self.colors[2], self.colors[1], self.colors[0]]


    def z_permute(self, ANGLE):
        self.vectors = numpy.dot(ANGLE, self.vectors)
        # swap x and y
        self.colors = [self.colors[1], self.colors[0], self.colors[2]]


    def get_piece(self):
        print(self.vectors[0], self.vectors[1], self.vectors[2])
        print(self.colors[0], self.colors[1], self.colors[2])




test = Cube_Piece([1, 1, 1], [green, blue, red])
test.x_permute(X_CLOCKWISE)
test.get_piece()