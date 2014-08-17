import copy


class Puyopuyo(object):
    WIDTH = 6
    HEIGHT = 13

    def __init__(self, string):
        self.puyos = [[" " for x in xrange(self.WIDTH)] for y in xrange(self.HEIGHT)]
        self.pre_puyos = [[" " for x in xrange(self.WIDTH)] for y in xrange(self.HEIGHT)]

        row = 0
        col = 0
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


    def drop(self):
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
        rensa = 0

        while self.puyos != self.pre_puyos:
            string=''
            puyo_to_remove = set()
            self.pre_puyos = copy.deepcopy(self.puyos)

            for horizontal in self.puyos:
                string += ''.join(horizontal) + '\n'
            print string, '++++++++++++++++++++++++++'

            for col in xrange(self.HEIGHT):
                for row in xrange(self.WIDTH):
                    color = self.puyos[col][row]
                    chained = [(col, row)]

                    if color != ' ':
                        chained = self.scan(col, row, chained, color)

                        if len(chained) >= 4:
                            puyo_to_remove = puyo_to_remove.union(chained)

            if len(puyo_to_remove):
                rensa += 1
                print rensa
                self.remove_puyo(puyo_to_remove)

            self.drop()
        return rensa

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
    puyopuyo1.update()

if __name__ == '__main__':
    main()
