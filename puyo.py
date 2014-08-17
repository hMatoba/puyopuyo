import copy
import random


DEBUG = False

class Puyopuyo(object):
    WIDTH = 6
    HEIGHT = 13

    def __init__(self, string=None):
        self.puyos = [[" " for x in xrange(self.WIDTH)] for y in xrange(self.HEIGHT)]
        self.pre_puyos = [[" " for x in xrange(self.WIDTH)] for y in xrange(self.HEIGHT)]
        self.rensa = 0
        self.falling = None

        row = 0
        col = 0
        if string:
            for color in string:
                if color == "\n":
                    col += 1
                    row = 0
                    continue
                else:
                    self.puyos[col][row] = color
                    row += 1

    def scan(self, col, row, chained, color):
        if row < self.WIDTH-1:
            chained = self._check_neighbor(col, row+1, chained, color)
        if col < self.HEIGHT-1:
            chained = self._check_neighbor(col+1, row, chained, color)
        if row > 0:
            chained = self._check_neighbor(col, row-1, chained, color)
        if col > 0:
            chained = self._check_neighbor(col-1, row, chained, color)

        return chained

    def _check_neighbor(self, col, row, chained, color):
        ar_color = self.puyos[col][row]
        if color == ar_color:
            if (col, row) in chained:
                return chained
            chained.append((col, row))
            chained = self.scan(col, row, chained, color)
        return chained


    def fill(self):
        prepuyos = None
        while self.puyos != prepuyos:
            prepuyos = copy.deepcopy(self.puyos)
            for col in xrange(12, 0, -1):
                for row in xrange(6):
                    if self.puyos[col][row] == ' ':
                        self.puyos[col][row] = self.puyos[col-1][row]
                        self.puyos[col-1][row] = ' '

    def remove_puyo(self, puyos):
        for x in puyos:
            self.puyos[x[0]][x[1]] = ' '


    def update(self):
        # in rensa processing
        if not self.falling:
            string=''
            puyo_to_remove = set()
            self.pre_puyos = copy.deepcopy(self.puyos)

            if DEBUG:
                for horizontal in self.puyos:
                    string += ''.join(horizontal) + '\n'
                print string, '++++++++++++++++++++++++++'

            for col in xrange(self.HEIGHT):
                for row in xrange(self.WIDTH):
                    if (col, row) in puyo_to_remove:
                        continue
                    color = self.puyos[col][row]
                    chained = [(col, row)]

                    if color != ' ':
                        chained = self.scan(col, row, chained, color)

                        if len(chained) >= 4:
                            puyo_to_remove = puyo_to_remove.union(chained)

            if len(puyo_to_remove):
                self.rensa += 1
                print self.rensa
                self.remove_puyo(puyo_to_remove)

            self.fill()

            if self.puyos == self.pre_puyos:
                self.rensa = 0

                # GAME OVER
                if self.puyos[0][2] != " ":
                    print("GAME OVER")
                    return False
                else:
                    self.falling = {"color":random.choice(("R", "G", "B", "Y")),
                                    "pos":(0, 2)}
        # drop puyo
        else:
            col, row = self.falling["pos"]
            if col == (self.HEIGHT-1) or self.puyos[col+1][row] != " ":
                self.puyos[col][row] = self.falling["color"]
                self.falling = None
            else:
                self.falling["pos"] = (col+1, row)

        return True


F = """  GYRR
RYYGYG
GYGYRR
RYGYRG
YGYRYG
GYRYRG
YGYRYR
YGYRYR
YRRGRG
RYGYGG
GRYGYR
GRYGYR
GRYGYR"""

def main():
    puyopuyo1 = Puyopuyo(F)
    loop = True
    print "PRESS ENTER KEY"
    while puyopuyo1.falling is None:
        loop = puyopuyo1.update()
        i = raw_input()

if __name__ == '__main__':
    DEBUG = True
    main()
