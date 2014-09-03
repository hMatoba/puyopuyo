#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys

import puyo


def drow(p, screen):
    x_offset, y_offset = p.OFFSET
    for y, row in enumerate(p.puyos):
        for x, color in enumerate(row):
            if color != " ":
                screen.blit(gem[color], (x_offset + x*24, y_offset + y*24))
    if p.falling:
        for i in xrange(2):
            y, x = p.falling[i]["pos"]
            if y >= 0 and x >= 0:
                screen.blit(gem[p.falling[i]["color"]], (x_offset + x*24, y_offset + y*24))

pygame.init()
SCREEN_SIZE = (640, 480)
screen = pygame.display.set_mode(SCREEN_SIZE)

gem = {"R":pygame.image.load("r.png").convert_alpha(),
       "G":pygame.image.load("g.png").convert_alpha(),
       "B":pygame.image.load("b.png").convert_alpha(),
       "Y":pygame.image.load("y.png").convert_alpha()}


p1 = puyo.Puyopuyo("")
p1.controller = {"left":pygame.K_LEFT,
                 "down":pygame.K_DOWN,
                 "right":pygame.K_RIGHT,
                 "roll":pygame.K_a}
p1.OFFSET = (100, 100)

screen.fill((100, 100, 100),
            (p1.OFFSET[0], p1.OFFSET[1], p1.WIDTH*24, p1.HEIGHT*24))
drow(p1, screen)
pygame.display.update()

clock = pygame.time.Clock()

counter = 0
while True:
    counter += 1
    clock.tick(30)

    # exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # control puyo
    if p1.falling and not (counter % 3):
        keys = pygame.key.get_pressed()
        col1, row1 = p1.falling[0]["pos"]
        col2, row2 = p1.falling[1]["pos"]
        a1 = col1 - col2
        a2 = row1 - row2

        if keys[p1.controller["left"]]:
            if (row1 > 0 and p1.puyos[col1][row1-1] == " ") and (row2 > 0 and p1.puyos[col2][row2-1] == " "):
                p1.falling[0]["pos"] = (col1, row1-1)
                p1.falling[1]["pos"] = (col2, row2-1)
        if keys[p1.controller["right"]]:
            if (row1 < p1.WIDTH-1 and p1.puyos[col1][row1+1] == " ") and (row2 < p1.WIDTH-1 and p1.puyos[col2][row2+1] == " "):
                p1.falling[0]["pos"] = (col1, row1+1)
                p1.falling[1]["pos"] = (col2, row2+1)
        if keys[p1.controller["down"]]:
            if (col1 < p1.HEIGHT-1 and p1.puyos[col1+1][row1] == " ") and (col2 < p1.HEIGHT-1 and p1.puyos[col2+1][row2] == " "):
                p1.falling[0]["pos"] = (col1+1, row1)
                p1.falling[1]["pos"] = (col2+1, row2)
        if keys[p1.controller["roll"]]:
            col1, row1 = p1.falling[0]["pos"]
            col2, row2 = p1.falling[1]["pos"]
            a1 = col1 - col2
            a2 = row1 - row2
            if (row1+a1 in (-1, p1.WIDTH)) or col1-a2 == p1.HEIGHT or p1.puyos[col1-a2][row1+a1] != " ":
                pass
            else:
                p1.falling[1]["pos"] = (col1-a2, row1+a1)

    # update puyos' position
    if not (counter % 50):
        p1.update()

    # update screen
    screen.fill((100, 100, 100),
                (p1.OFFSET[0], p1.OFFSET[1], p1.WIDTH*24, p1.HEIGHT*24))
    drow(p1, screen)
    pygame.display.update()

    if counter == 300:
        counter = 0

