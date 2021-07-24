# print out board each move and sleep for 300 so that people can watch
# CAL is chutes and ladders
# for sake of simplicity board will wrap to the right instead of switch back and forth

"""
example board for chutes and ladders
@ 0 0 0 0 3 0
0 1 0 0 0 0 0
0 0 0 0 -9 0 0
0 0 4 0 5 0 0
0 0 0 0 0 0 start

+---+---+---+
| 0 | 9 | 0 |
+---+---+---+
"""

import random
import copy

howto = """
This game seeks to follow the rules of chutes and ladders.
players roll a die and move spaces accordingly, spaces with a number
require players to adjust their position by that number of spaces.
The main catch is that players can roll multiple times based on how
many tokens they have. Each token gives one more roll for the turn 
and each player starts with 7 tokens. At the start of their turn, each player
can grab one token from the discard pile and add it to their own. First to reach space 100 wins.
"""


class Board:
    # the matrix variable should not change after init
    cols = 0
    rows = 0
    matrix = []
    positions = []

    def __init__(self, i, j, m, p):
        """
        example input looks like
        g = Board([ [0, 0, 0, 0, 0], [1, 2, 1, -1, 0], 
        [3, 0, 0, 2, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0] ], 
        0, [ ['A', 5, 5], ['B', 5, 5], ['C', 5, 5] ])
        """
        self.rows = j
        self.cols = i
        self.matrix = m
        self.positions = p


    # positions will will determine whether to print
    # tile number or piece on tile
    def print_board(self):
        # add in the player pieces
        actual = copy.deepcopy(self.matrix)
        for guy in self.positions:
            actual[guy[1]][guy[2]] = guy[0]
        # print out the board with borders
        for i in actual:
            top = "+"
            middle = " "
            for j in i:
                top += "---+"
                middle += " " + str(j) + " |"
            print(top)
            print(middle)


    # move piece according to position stored in positions
    def update_piece(self, player, value):
        for p in range(len(self.positions)):
            if self.positions[p] == player:
                # can get new position using mod division
                ijump = (value // self.cols)
                jjump = (value % self.cols)
                self.positions[p] = [player[0], player[1] - ijump, player[2] - jjump]



    # checks value of tile and moves piece on it accordingly
    def update_bonus_tile(self, player):
        if player[1] == 0 and player[2] == 0:
            pass
        else:
            val = self.matrix[player[1]][player[2]]
            self.update_piece(player, val)


    # TODO fix this
    def get_distance_from_goal(self, player):
        for p in self.positions:
            if p[0] == player:
                # each row is worth num of cols
                return (p[1] * self.rows) + p[2]




class Game:
    # start by making this a game of only humans and then add ai later
    turn = 0
    board = 0
    players = []

    def __init__(self, cal_board) -> None:
        self.players = [['A', 0, 0], ['B', 0, 0], ['C', 0, 0], ['D', 0, 0]]
        self.turn = 0
        self.board = cal_board


    def roll_die(self):
        return random.randint(1, 6)


    def use_tokens(self):
        pass


    def player_turn(self, turnplayer):
        val = self.roll_die()
        self.board.update_piece(turnplayer, val)
        self.board.update_bonus_tile(turnplayer)

    

    def full_turn(self):
        for p in self.players:
            self.player_turn(p)
        self.turn += 1


    def print_game(self):
        print("Player A is in the lead!")
        print("Tokens: 0   0   0   0")
        self.board.print_board()


    def play(self):
        pass


#class AI_player



# need extensive planning
g = Board(4, 3, [['@', 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, "start"]], [['A', 2, 3], ['B', 1, 2]] )

g.print_board()
g.update_piece(['A', 2, 3], 5)
g.update_bonus_tile(['A', 0, 3])
print("\n \n")
g.print_board()