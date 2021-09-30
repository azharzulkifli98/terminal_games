
"""
Moving into a 3x3 cube requires more classes, one for each piece and
one for the total cube
Rotations will require a bit of matrix algebra using numpy and rotation matrices
features to consider:
3x3 mode, sudoku mode, solve, reset/set, undo
"""
import random
import numpy

#                                           CONSTANTS

""" faces are 
# -x green
# +z white
# -z yellow
# +y red 
# -y magenta
# +x blue
"""
GREEN = u"\u001b[32m#\u001b[0m"
BLUE = u"\u001b[34m#\u001b[0m"

RED = u"\u001b[31m#\u001b[0m"
MAGENTA = u"\u001b[35m#\u001b[0m"

YELLOW = u"\u001b[33m#\u001b[0m"
WHITE = u"\u001b[37m#\u001b[0m"

# consider clockwise vs anticlockwise

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




class Cube:
    """
    Here we need to consider what we want to do with all the pieces of the cube
    rotate pieces around an axis
    view the whole cube in an easy format
    take commands through the terminal
    reset the cube when the player is done
    """
    main_bag = []
    faces = []
    edges = []
    corners = []


    def __init__(self) -> None:
        self.faces = [ 
            Cube_Piece([-1, 0, 0], [GREEN, 0, 0]),
            Cube_Piece([1, 0, 0], [BLUE, 0, 0]),
            Cube_Piece([0, -1, 0], [0, MAGENTA, 0]),
            Cube_Piece([0, 1, 0], [0, RED, 0]),
            Cube_Piece([0, 0, -1], [0, 0, YELLOW]),
            Cube_Piece([0, 0, 1], [0, 0, WHITE])
        ]

        self.corners = [ 
            Cube_Piece([-1, -1, -1], [GREEN, MAGENTA, YELLOW]),
            Cube_Piece([1, -1, -1], [BLUE, MAGENTA, YELLOW]),
            Cube_Piece([-1, 1, -1], [GREEN, RED, YELLOW]),
            Cube_Piece([-1, -1, 1], [GREEN, MAGENTA, WHITE]),
            Cube_Piece([1, 1, -1], [BLUE, RED, YELLOW]),
            Cube_Piece([1, -1, 1], [BLUE, MAGENTA, WHITE]),
            Cube_Piece([1, -1, -1], [BLUE, MAGENTA, YELLOW]),
            Cube_Piece([1, 1, 1], [BLUE, RED, WHITE])
        ]

        self.edges = [ 
            Cube_Piece([0, -1, -1], [0, MAGENTA, YELLOW]),
            Cube_Piece([0, 1, -1], [0, RED, YELLOW]),
            Cube_Piece([0, -1, 1], [0, MAGENTA, WHITE]),
            Cube_Piece([0, 1, 1], [0, RED, WHITE]),
            Cube_Piece([1, 0, -1], [BLUE, 0, YELLOW]),
            Cube_Piece([1, 0, 1], [BLUE, 0, WHITE]),
            Cube_Piece([-1, 0, 1], [GREEN, 0, WHITE]),
            Cube_Piece([-1, 0, -1], [GREEN, 0, YELLOW]),
            Cube_Piece([1, -1, 0], [BLUE, MAGENTA, 0]),
            Cube_Piece([-1, 1, 0], [GREEN, RED, 0]),
            Cube_Piece([1, 1, 0], [BLUE, RED, 0]),
            Cube_Piece([-1, -1, 0], [GREEN, MAGENTA, 0])
        ]

        self.main_bag.append(self.faces)
        self.main_bag.append(self.edges)
        self.main_bag.append(self.corners)
    

    def rotate(self, angle, axis):
        return 0
    

    def print_cube(self):
        print(self.faces)
    

    def read_user_input(self, string):
        if len(string) > 1:
            return "Sorry that wont do..."
        else:
            return "Hi"


    def play(self):
        # clear screen
        # print cube
        # get input
        # perform rotation or help or reset or undo
        # repeat
        return 0



test = Cube_Piece([1, 1, 1], [GREEN, BLUE, RED])
test.x_permute(X_CLOCKWISE)
test.get_piece()
game = Cube()
game.print_cube()