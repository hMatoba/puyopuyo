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
        y, x = p.falling["pos"]
        screen.blit(gem[p.falling["color"]], (x_offset + x*24, y_offset + y*24))

pygame.init()
SCREEN_SIZE = (640, 480)
screen = pygame.display.set_mode(SCREEN_SIZE)

gem = {"R":pygame.image.load("r.png").convert_alpha(),
       "G":pygame.image.load("g.png").convert_alpha(),
       "B":pygame.image.load("b.png").convert_alpha(),
       "Y":pygame.image.load("y.png").convert_alpha()}


p1 = puyo.Puyopuyo(puyo.F)
p1.controller = {"left":pygame.K_LEFT,
                 "down":pygame.K_DOWN,
                 "right":pygame.K_RIGHT}
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
        col, row = p1.falling["pos"]
        if keys[p1.controller["left"]]:
            if row > 0 and p1.puyos[col][row-1] == " ":
                p1.falling["pos"] = (col, row-1)
        if keys[p1.controller["right"]]:
            if row < p1.WIDTH-1 and p1.puyos[col][row+1] == " ":
                p1.falling["pos"] = (col, row+1)
        if keys[p1.controller["down"]]:
            if col < p1.HEIGHT-1 and p1.puyos[col+1][row] == " ":
                p1.falling["pos"] = (col+1, row)

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

