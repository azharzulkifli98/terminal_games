# print out board each move and sleep for 300 so that people can watch
# CAL is chutes and ladders

"""
example board for chutes and ladders
@ 0 0 0 0 3 0
0 1 0 0 0 0 0
0 0 0 0 -9 0 0
0 0 4 0 5 0 0
0 0 0 0 0 0 start
"""

import random


class Board:
    # the matrix variable should not change after init
    cols = 0
    rows = 0
    matrix = [[]]
    turn = 0
    positions = []

    def __init__(self, i, j, m, t, p):
        """
        example input looks like
        g = Board([ [0, 0, 0, 0, 0], [1, 2, 1, -1, 0], 
        [3, 0, 0, 2, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0] ], 
        0, [ ['A', 5, 5], ['B', 5, 5], ['C', 5, 5] ])
        """
        self.rows = j
        self.cols = i
        self.matrix = m
        self.turn = t
        self.positions = p


    # positions will will determine whether to print
    # tile number or piece on tile
    def print_board(self):
        for i in self.matrix:
            for j in i:
                occupy = False
                for k in self.positions:
                    if i in k and j in k:
                        print(k[0])
                        occupy = True
                # only print number when no player is there
                if not occupy:
                    print(self.matrix[i][j])


    # move piece according to position stored in positions
    def update_piece(self, i, j, player, value):
        for p in self.positions:
            if p == [player, i, j]:
                # TODO: fix this and test vals
                newi = 
                p = [player, newi, newj]



    # checks value of tile and moves piece on it accordingly
    def update_bonus_tile(self, i, j):
        val = self.matrix[i][j]
        self.update_piece(i, j, val)


    def get_distance_from_goal(self, player):
        for p in self.positions:
            if p[0] == player:
                # each row is worth num of cols
                return (p[1] * self.rows) + p[2]




class Game:

    def __init__(self) -> None:
        players = []
        num_players = 0

    def roll_die(self):
        pass

    def use_tokens(self):
        pass

    def player_turn(self):
        pass
    
    def print_game(self):
        pass


    def play(self):
        pass


#class AI_player



# need extensive planning