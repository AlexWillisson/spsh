#! /usr/bin/env python

import pygame, sys, os

SIZE = (800, 640)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class node:
    def __init__ (self, name, pos=(0, 0)):
        self.name = name
        self.pos = pos

        self.text = font.render (self.name, True, WHITE)
        textpos = self.text.get_rect (topleft=(pos[0] + 3, pos[1] + 3))

        self.textwidth = textpos.width
        self.textheight = textpos.height

    def draw (self, screen):
        textpos = pygame.Rect ((self.pos[0] + 3, self.pos[1] + 3),
                               (self.textwidth, self.textheight))
        outline = pygame.Rect (self.pos[0], self.pos[1],
                               self.textwidth + 6, self.textheight + 6)

        screen.blit (self.text, textpos)
        pygame.draw.rect (screen, WHITE, outline, 1) 

def reflow (nodes, area):
    pos = [0, 0]
    maxwidth = 0

    for n in nodes:
        if pos[1] + n.textheight + 6 > area[1]:
            pos[0] += maxwidth
            pos[1] = 0
            maxwidth = 0

        n.pos = list (pos)

        pos[1] += n.textheight + 6

        maxwidth = max (maxwidth, n.textwidth + 6)

        print pos

def process_input ():
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit ()
            sys.exit ()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit ()
                sys.exit ()

def draw ():
    board.fill (BLACK)

    for n in nodelist:
        n.draw (board)

    pygame.display.flip ()

pygame.init ()
board = pygame.display.set_mode (SIZE)
pygame.display.set_caption ("spsh")

background = pygame.Surface (SIZE)
font = pygame.font.Font (None, 30)

#files = os.listdir ("/home/atw/springspin")
files = os.listdir ("/home/atw")
nodelist = [node (name) for name in files]

reflow (nodelist, SIZE)

while True:
    process_input ()

    draw ()
