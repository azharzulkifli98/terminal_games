"""
Moving into a 3x3 cube requires more classes, one for each piece and
one for the total cube
Rotations will require a bit of matrix algebra using numpy and rotation matrices
features to consider:
3x3 mode, sudoku mode, solve, reset/set, undo
"""
import random
import numpy
import os

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


    # for actual use with cube functions for given arguments
    def permute(self, angle):
        self.vectors = numpy.dot(angle, self.vectors)

    def color_swap(self, axis):
        if axis == 0:
            self.colors = [self.colors[0], self.colors[2], self.colors[1]]
        elif axis == 1:
            self.colors = [self.colors[2], self.colors[1], self.colors[0]]
        elif axis == 2:
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
    last_move = ""


    def __init__(self) -> None:

        self.main_bag = [ 
            Cube_Piece([-1, 0, 0], [GREEN, 0, 0]),
            Cube_Piece([1, 0, 0], [BLUE, 0, 0]),
            Cube_Piece([0, -1, 0], [0, MAGENTA, 0]),
            Cube_Piece([0, 1, 0], [0, RED, 0]),
            Cube_Piece([0, 0, -1], [0, 0, YELLOW]),
            Cube_Piece([0, 0, 1], [0, 0, WHITE]),

            Cube_Piece([-1, -1, -1], [GREEN, MAGENTA, YELLOW]),
            Cube_Piece([-1, 1, 1], [GREEN, RED, WHITE]),
            Cube_Piece([-1, 1, -1], [GREEN, RED, YELLOW]),
            Cube_Piece([-1, -1, 1], [GREEN, MAGENTA, WHITE]),
            Cube_Piece([1, 1, -1], [BLUE, RED, YELLOW]),
            Cube_Piece([1, -1, 1], [BLUE, MAGENTA, WHITE]),
            Cube_Piece([1, -1, -1], [BLUE, MAGENTA, YELLOW]),
            Cube_Piece([1, 1, 1], [BLUE, RED, WHITE]),

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


    def print_cube(self):
        gs = [piece for piece in self.main_bag if piece.vectors[0] == -1]
        bs = [piece for piece in self.main_bag if piece.vectors[0] == 1]
        m = [piece for piece in self.main_bag if piece.vectors[0] == 0]

        gs.sort(key=lambda x : (x.vectors[2], x.vectors[1]))
        bs.sort(key=lambda x : (x.vectors[2], x.vectors[1]))
        m.sort(key=lambda x: (x.vectors[2], x.vectors[1]))

        layer1 = "    " + gs[0].colors[2] + " " + gs[1].colors[2] + " " + gs[2].colors[2]
        layer1 = layer1 + "\t    " + bs[0].colors[2] + " " + bs[1].colors[2] + " " + bs[2].colors[2]

        layer2 = "  " + gs[0].colors[1]  + " " + gs[0].colors[0]  + " " + gs[1].colors[0]  + " " + gs[2].colors[0] + " " + gs[2].colors[1]
        layer2 = layer2 + "\t  " + bs[0].colors[1] + " " + bs[0].colors[0] + " " + bs[1].colors[0] + " " + bs[2].colors[0] + " " + bs[2].colors[1]

        layer3 = "  " + gs[3].colors[1] + " " + gs[3].colors[0] + " " + gs[4].colors[0] + " " + gs[5].colors[0] + " " + gs[5].colors[1]
        layer3 = layer3 + "\t  " + bs[3].colors[1] + " " + bs[3].colors[0] + " " + bs[4].colors[0] + " " + bs[5].colors[0] + " " + bs[5].colors[1]

        layer4 = "  " + gs[6].colors[1] + " " + gs[6].colors[0] + " " + gs[7].colors[0] + " " + gs[8].colors[0] + " " + gs[8].colors[1]
        layer4 = layer4 + "\t  " + bs[6].colors[1] + " " + bs[6].colors[0] + " " + bs[7].colors[0] + " " + bs[8].colors[0] + " " + bs[8].colors[1]

        layer5 = "    " + gs[6].colors[2] + " " + gs[7].colors[2] + " " + gs[8].colors[2]
        layer5 = layer5 + "\t    " + bs[6].colors[2] + " " + bs[7].colors[2] + " " + bs[8].colors[2]


        print("\n")
        print(layer1)
        print(layer2)
        print(layer3)
        print(layer4)
        print(layer5)
        print("\n")




    def rotate(self, angle, axis, slice):
        # here slice helps to index the x or y or z axis that will rotate
        # so X_REVERSE, 0, -1 will rotate the green face counter clockwise ^_^
        for piece in self.main_bag:
            if piece.vectors[axis] == slice:
                piece.permute(angle)
                piece.color_swap(axis)
    

    def execute_user_input(self, string):
        if len(string) > 1:
            return "Sorry that wont do..."
        else:
            # should be 12 types of rotations in total
            if string == "l":
                self.rotate(X_REVERSE, 0, -1)
            elif string == "L":
                self.rotate(X_CLOCKWISE, 0, -1)
            elif string == "r":
                self.rotate(X_REVERSE, 0, 1)
            elif string == "R":
                self.rotate(X_CLOCKWISE, 0, 1)

            # Z AXIS STUFF
            elif string == "u":
                self.rotate(Z_REVERSE, 2, -1)
            elif string == "U":
                self.rotate(Z_CLOCKWISE, 2, 1)
            elif string == "d":
                self.rotate(Z_REVERSE, 2, -1)
            elif string == "D":
                self.rotate(Z_CLOCKWISE, 2, 1)

            # Y AXIS STUFF
            elif string == "f":
                self.rotate(Y_REVERSE, 1, 1)
            elif string == "F":
                self.rotate(Y_CLOCKWISE, 1, 1)
            elif string == "b":
                self.rotate(Y_REVERSE, 1, -1)
            elif string == "B":
                self.rotate(Y_CLOCKWISE, 1, -1)


    def undo_move(self):
        # undo moves by reversing string and calling reverse rotations
        backwards = self.last_move[::-1]
        backwards = backwards.swapcase()
        print(backwards)
        for char in backwards:
            self.execute_user_input(char)
        self.last_move = ""


    def scramble(self):
        # perform 10 random rotations to get a scrambled cube to solve
        total = ""
        for n in range(10):
            flip = random.choice(['l', 'L', 'r', 'R', 'u', 'U', 'd', 'D', 'f', 'F', 'b', 'B'])
            total = total + flip
            self.execute_user_input(flip)
        self.last_move = total


    def play(self):
        # main function of Cube class that lets users play with a rubiks cube using char input
        help = """
        This program lets you play with a 3x3 rubiks cube model
        the front and back face are printed out to keep track of piece locations
        you can rotate the cube sides using the following notation:
        r - right face clockwise  R - right face counterclockwise
        l - left face clockwise   L - left face counterclockwise
        u - top face clockwise    U - top face counterclockwise
        d - bottom face clockwise D - bottom face counterclockwise
        f - front face clockwise  F - front face counterclockwise
        b - rear face clockwise   B - rear face counterclockwise
        You can perform multiple rotations at once by giving a string as input
        for example rrll will rotate both faces twice which is equivalent to 
        rotating the center slice counterclockwise twice
        The program also comes with the following keywords:
        help - print this message again
        quit - end the program
        scramble - perform random rotations on the cube
        undo - undo the rotations performed in the previous move
        """
        message = help
        while True:
            # clear screen
            os.system('clear')

            # print cube
            self.print_cube()

            # get input
            next = input(message + "\n > ")

            if next == "help":
                message = help
            elif next == "quit":
                break
            elif next == "scramble":
                self.scramble()
            elif next == "undo":
                self.undo_move()

            # perform rotations on cube
            else:
                for char in next:
                    if char not in "lrudfbLRUDFB":
                        message = "bad input, try again"
                        continue
                message = ""
                for char in next:
                    self.execute_user_input(char)
                    self.print_cube()
                
                # save this action for undo function
                self.last_move = next

        # repeat



game = Cube()
game.play()