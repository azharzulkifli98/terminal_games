# the protoptye for our chess assignment

# if im not mistaken...

# need a game object
# need a board object
# might need player object
# need piece objects

# for king through pawn
class Piece:
    xpos = 0
    ypos = 0
    symbol = "P"
    color = "white"
    status = "alive"
    is_king = False
    is_in_check = False
    moveset = []

    def __init__(self):
        return 0
    
    def move(self):
        return 3

    def attack(self):
        return 3

    def die(self):
        return 3

class Pawn(Piece):
    # need to consider en passe, promotion, and first turn move
    def __init__(self):
        return 0

class Rook(Piece):
    # need to consider castling
    def __init__(self):
        return 0

class Bishop(Piece):
    # need to consider moves
    def __init__(self):
        return 0

class Queen(Piece):
    # need to consider moves
    def __init__(self):
        return 0

class King(Piece):
    # need to consider castling, check, and checkmate
    def __init__(self):
        return 0

class Knight(Piece):
    # need to consider moves
    def __init__(self):
        return 0


class Board:
    # fmmm

print("klksd")