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


HOWTO = """
This game seeks to follow the rules of chutes and ladders.
Players roll a die and move spaces accordingly, spaces with a number
require players to adjust their position by that number of spaces.
The main catch is that players can roll multiple times based on how
many tokens they have. Each token gives one more roll for the turn 
and each player starts with 7 tokens. At the start of their turn, each player
can grab one token from the discard pile and add it to their own. First to reach space 100 wins.
"""

SPARSEBOARD = [
    ['@', 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, '$']
]





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
            middle = "|"
            for j in i:
                top += "---+"
                middle += str(j).rjust(3) + "|"
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




class Player:
    position = []
    name = ""
    role = ""
    token_count = 0
    # player doenst need to know turn order


    # name has to shortened for formatting
    def __init__(self, pos, na, ro):
        self.position = pos
        if len(na) > 10:
            self.name = na[:9]
        else:
            self.name = na
        self.role = ro
        self.token_count = 7


    # for keeping track with the board
    def update_position(self, x, y):
        self.position = [self.position[0], x, y]


    #
    def use_tokens(self, amount):
        self.token_count = self.token_count - amount


    # three methods for deciding how to spend players tokens on their turn
    def decide_turn(self):
        # human -> input
        if self.role == "human":
            val = ""
            while not val.isdigit():
                val = input("how many coins will you spend: ")

        # greedy -> all tokens if > 1
        if self.role == "greedy":
            return self.token_count

        # binge -> all if pos > 50% spend all else spend 1
        if self.role == "binge":
            if self.distance_from_goal() > 50:
                return self.token_count
            else:
                return 0




class Game:
    turn = 0
    board = 0
    players = []

    def __init__(self):
        # for now we will go with 2 humans and 2 ai
        self.players = []
        self.players.append(Player(['A', 9, 9], input("enter player 1 name: "), "human"))
        self.players.append(Player(['B', 9, 9], input("enter player 2 name: "), "human"))
        self.players.append(Player(['C', 9, 9], "Bot1", "greedy"))
        self.players.append(Player(['D', 9, 9], "Fred", "binge"))
        self.turn = 0
        initials = [['A', 9, 9], ['B', 9, 9], ['C', 9, 9], ['D', 9, 9]]
        self.board = Board(10, 10, SPARSEBOARD, initials)




    def player_turn(self, turn):
        amount = self.players[turn].decide_turn()
        self.players[turn].use_tokens(amount)

        # automatically performs die roll in for loop
        for i in range(amount):
            self.board.update_piece(self.players[turn].position, random.randint(1, 6))
            self.board.update_bonus_tile(self.players[turn].position)
        
        # update player info
        self.players[turn].position = self.board.positions[turn]


    def print_game(self):
        row1 = ""
        row2 = ""
        for i in range(len(self.players)):
            row1 += str(self.players[i].name).ljust(10)
            row2 += str(self.players[i].token_count).ljust(10)
        print(row1)
        print(row2)
        self.board.print_board()


    def play(self):
        # cls -> print_score -> print_board -> get_coin_input -> roll_turn -> switch_to_next_player
        for i in range(3):
            os.system('clear')
            self.print_game()
            wait = input("> ")
            for i in range(len(self.players)):
                self.player_turn(i)
            self.turn += 1




# need extensive planning
#g = Board(4, 3, [['@', 0, 0, -2], [0, 0, 0, 0], [0, 0, 0, "$"]], [['A', 2, 3], ['B', 2, 3]] )


# initial setup


#p = Game(['Ao', 'Bafuku', 'Choku', 'Dodon'], ['a', 'b', 'c', 'd'], g)
#p.play()
p = Game()
p.play()