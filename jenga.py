import random

howto = """
This game mimics jenga by giving a 3x20 array for players to use.
You can remove one piece each turn and it goes to the top but 
some pieces are more risky based on a probability map.
Target pieces by their height and direction using 2r, 2c, 2l
for a piece on the second level on the right, center, and left
"""

class Jenga:

    def __init__(self):
        self.height = 20
        self.players = 1
        self.tower = []
        for i in range(20):
            self.tower.append([1, 1, 1])


    # val comes in the form 1c and needs to be converted
    def remove_piece(self, val):
        # needs to accept 1c  3r  40c and reject c3  ;ds'  6896985l  c  0  etc
        if not isalpha(val[0]):
            print("invalid")
        h = int(val[0])
        if h > self.height - 3:
            print("invalid")
        else:
            # remove
            pass


    # place piece at top of tower
    def add_piece(self):
        if self.tower[0][2] == 1:
            self.tower.insert(0, [1, 0, 0])
            self.height = self.height + 1
        elif self.tower[0][1] == 0:
            self.tower[0][1] = 1
        else:
            self.tower[0][2] = 1


    def get_success(self):
        pass


    def print_tower(self):
        for row in self.tower:
            print("    ", row[0], row[1], row[2])
        print("")
        print("")


    # simulate one turn of jenga with player or bot
    def play_round(self):
        pass


# playtest
print(howto)
g = Jenga()
g.print_tower()
g.add_piece()
g.print_tower()
g.add_piece()
g.print_tower()
g.add_piece()
g.print_tower()
g.add_piece()