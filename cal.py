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

import os
from time import sleep
import random
import copy
import configparser


howto = """
This game seeks to follow the rules of chutes and ladders.
Players roll a die and move spaces accordingly, spaces with a number
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

    def __init__(self, names, role, cal_board):
        # format will be symbol: [name, index]
        self.players = {
            'A': [0, names[0], role[0]],
            'B': [1, names[1], role[1]],
            'C': [2, names[2], role[2]],
            'D': [3, names[3], role[3]]
        }
        self.turn = 0
        self.board = cal_board


    def roll_die(self):
        return random.randint(1, 6)


    def use_tokens(self, amount):
        for t in range(amount):
            self.roll_die()
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
        print(f"Player: {self.players['A'][1]} {self.players['B'][1]} {self.players['C'][1]} {self.players['D'][1]}")
        print("Tokens: 0   0   0   0")
        self.board.print_board()


    def play(self):
        # first setup
        # num_players -> pick_roles -> pick_board/difficulty


        # then loop
        # cls -> print_score -> print_board -> get_coin_input -> roll_turn -> switch_to_next_player
        for i in range(3):
            os.system('clear')
            self.print_game()
            wait = input("> ")
            for player in self.board.positions:
                self.player_turn(player)



#class AI_player









# need extensive planning
g = Board(4, 3, [['@', 0, 0, -2], [0, 0, 0, 0], [0, 0, 0, "$"]], [['A', 2, 3], ['B', 2, 3]] )


# initial setup


p = Game(['Ao', 'Bafuku', 'Choku', 'Dodon'], ['a', 'b', 'c', 'd'], g)
p.play()
