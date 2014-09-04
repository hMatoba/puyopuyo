#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys

import puyo


class Game(object):
    SCREEN_SIZE = (640, 480)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        self.gem = {"R":pygame.image.load("resource/r.png").convert_alpha(),
                    "G":pygame.image.load("resource/g.png").convert_alpha(),
                    "B":pygame.image.load("resource/b.png").convert_alpha(),
                    "Y":pygame.image.load("resource/y.png").convert_alpha()}

        self.player1 = puyo.Puyopuyo(puyo.F)
        #self.player1 = puyo.Puyopuyo("")
        self.player1.controller = {"left":pygame.K_LEFT,
                         "down":pygame.K_DOWN,
                         "right":pygame.K_RIGHT,
                         "roll":pygame.K_a}
        self.player1.OFFSET = (100, 100)

        self.screen.fill((100, 100, 100),
                         (self.player1.OFFSET[0], self.player1.OFFSET[1], self.player1.WIDTH*24, self.player1.HEIGHT*24))
        self.draw(self.player1)
        pygame.display.update()

        self.clock = pygame.time.Clock()


    def draw(self, p):
        x_offset, y_offset = p.OFFSET
        for y, row in enumerate(p.puyos):
            for x, color in enumerate(row):
                if color != " ":
                    self.screen.blit(self.gem[color], (x_offset + x*24, y_offset + y*24))
        if p.falling:
            for i in xrange(2):
                y, x = p.falling[i]["pos"]
                if y >= 0 and x >= 0:
                    self.screen.blit(self.gem[p.falling[i]["color"]], (x_offset + x*24, y_offset + y*24))

    def play(self):
        counter = 0
        while True:
            counter += 1
            self.clock.tick(30)

            # exit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # control puyo
            if self.player1.falling and not (counter % 3):
                keys = pygame.key.get_pressed()
                col1, row1 = self.player1.falling[0]["pos"]
                col2, row2 = self.player1.falling[1]["pos"]
                a1 = col1 - col2
                a2 = row1 - row2

                if keys[self.player1.controller["left"]]:
                    if (row1 > 0 and self.player1.puyos[col1][row1-1] == " ") and (row2 > 0 and self.player1.puyos[col2][row2-1] == " "):
                        self.player1.falling[0]["pos"] = (col1, row1-1)
                        self.player1.falling[1]["pos"] = (col2, row2-1)
                if keys[self.player1.controller["right"]]:
                    if (row1 < self.player1.WIDTH-1 and self.player1.puyos[col1][row1+1] == " ") and (row2 < self.player1.WIDTH-1 and self.player1.puyos[col2][row2+1] == " "):
                        self.player1.falling[0]["pos"] = (col1, row1+1)
                        self.player1.falling[1]["pos"] = (col2, row2+1)
                if keys[self.player1.controller["down"]]:
                    if (col1 < self.player1.HEIGHT-1 and self.player1.puyos[col1+1][row1] == " ") and (col2 < self.player1.HEIGHT-1 and self.player1.puyos[col2+1][row2] == " "):
                        self.player1.falling[0]["pos"] = (col1+1, row1)
                        self.player1.falling[1]["pos"] = (col2+1, row2)
                if keys[self.player1.controller["roll"]]:
                    col1, row1 = self.player1.falling[0]["pos"]
                    col2, row2 = self.player1.falling[1]["pos"]
                    a1 = col1 - col2
                    a2 = row1 - row2
                    if (row1+a1 in (-1, self.player1.WIDTH)) or col1-a2 == self.player1.HEIGHT or self.player1.puyos[col1-a2][row1+a1] != " ":
                        pass
                    else:
                        self.player1.falling[1]["pos"] = (col1-a2, row1+a1)

            # update puyos' position
            if not (counter % 50):
                self.player1.update()

            # update screen
            self.screen.fill((100, 100, 100),
                             (self.player1.OFFSET[0],
                              self.player1.OFFSET[1],
                              self.player1.WIDTH*24,
                              self.player1.HEIGHT*24)
                             )
            self.draw(self.player1)
            pygame.display.update()

            if counter == 300:
                counter = 0

if __name__ == "__main__":
    Game().play()