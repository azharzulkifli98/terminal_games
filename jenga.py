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


    # needs to accept 1c  3r  40c and reject c3  ;ds'  6896985l  c  0  etc
    def pick_piece(self):
        while True:
            val = input("pick a piece from the tower: ")
            if len(val) < 2:
                print("invalid format, try again")
            else:
                num = val[:-1]
                char = val[-1]
            
            if char not in "rcl" or not num.isdigit():
                print("invalid format, try again")
            elif int(num) > self.height - 3:
                print("not within tower range, try again")
            else:
                i = self.height - int(num)
                if i > self.height - 4:
                    print("cannot pick from top 3 layers, try again")
                if char == "l":
                    j = 0
                elif char == "c":
                    j = 1
                else:
                    j = 2
                # cannot pick from empty spaces
                if self.tower[i][j] == 0:
                    print("no piece to remove, try again")
                else:
                    return i, j


    # use this for bots turn, make it pick a random piece blindly
    def auto_piece(self):
        val = 0
        print("Bot's turn...")
        # cannot pick location with no piece
        while val == 0:
            i = random.randint(4, self.height - 1)
            j = random.randint(0, 2)
            val = self.tower[i][j]
        return i, j


    # input validation is done with pick_piece()
    def remove_piece(self, i, j):
        self.tower[i][j] = 0


    # place piece at top of tower
    def add_piece(self):
        if self.tower[0][2] == 1:
            self.tower.insert(0, [1, 0, 0])
            self.height = self.height + 1
        elif self.tower[0][1] == 0:
            self.tower[0][1] = 1
        else:
            self.tower[0][2] = 1


    # each time a piece is removed we need to check
    # whether the tower will collapse or not
    def get_success(self, h):
        prob = random.randint(0, 99)
        slice = self.tower[h]
        if slice == [1, 1, 1]:
            return 100 > prob
        elif slice == [1, 0, 1]:
            return 90 > prob
        elif slice == [1, 1, 0] or slice == [0, 1, 1]:
            return 80 > prob
        elif slice == [0, 1, 0]:
            return 50 > prob
        elif slice == [0, 0, 1] or slice == [1, 0, 0] or slice == [0, 0, 0]:
            return 0 > prob


    def print_tower(self):
        for row in self.tower:
            print("    ", row[0], row[1], row[2])
        print("")
        print("")


    # simulate one turn of jenga with player or bot
    # TODO add the bot simulating piece removal
    def play_round(self):
        myturn = True
        while True:
            self.print_tower()

            if myturn:
                valid = self.pick_piece()
            else:
                valid = self.auto_piece()

            self.remove_piece(valid[0], valid[1])
            myturn = not myturn

            if self.get_success(valid[0]):
                self.add_piece()
            else:
                print("tower collapse! ! !")
                self.print_tower()
                break
        if not myturn:
            print("Better luck next time!")
        else:
            print("Nice, you win!")


# playtest
print(howto)
g = Jenga()
g.play_round()
