#! /usr/bin/env python

import pygame, sys, os

SIZE = (800, 640)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
MAXCHARS = 12
selected_nodes = set()
moving_nodes = []

class node:
    def __init__ (self, name, pos=(0, 0)):
        self.name = name
        self.pos = pos

        display = self.name
        if len (self.name) > MAXCHARS:
            display = self.name[:9] + "..."

        self.text = font.render (display, True, WHITE)
        textpos = self.text.get_rect (topleft=(pos[0] + 3, pos[1] + 3))

        self.width = textpos.width + 6
        self.height = textpos.height + 6

        self.moving = False

    def draw (self, screen):
        textpos = pygame.Rect ((self.pos[0] + 3, self.pos[1] + 3),
                               (self.width - 6, self.height - 6))
        outline = pygame.Rect (self.pos[0], self.pos[1],
                               self.width, self.height)

        pygame.draw.rect (screen, BLACK, outline)

        screen.blit (self.text, textpos)
        if self in selected_nodes:
            pygame.draw.rect (screen, YELLOW, outline, 1) 
        else:
            pygame.draw.rect (screen, WHITE, outline, 1) 

def reflow (nodes, area):
    pos = [0, 0]
    maxwidth = 0

    for n in nodes:
        if pos[1] + n.height > area[1]:
            pos[0] += maxwidth + 5
            pos[1] = 0
            maxwidth = 0

        n.pos = list (pos)

        pos[1] += n.height

        maxwidth = max (maxwidth, n.width)

def rect (p0, p1):
        left = min (p0[0], p1[0])
        top = min (p0[1], p1[1])
        width = abs (p0[0] - p1[0])
        height = abs (p0[1] - p1[1])

        return pygame.Rect (left, top, width, height)

def process_input ():
    global selstart, mousepos, moving_nodes, nodelist, selected_nodes

    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            pygame.quit ()
            sys.exit ()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit ()
                sys.exit ()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = None
            for n in nodelist:
                if pygame.Rect (n.pos, (n.width,
                                        n.height)).collidepoint (mousepos):
                    clicked = n

            if clicked:
                if clicked in selected_nodes:
                    new_order = list (nodelist)

                    for n in nodelist:
                        if n in selected_nodes:
                            new_order.remove (n)
                            new_order.append (n)
                            moving_nodes.append (n)
                            n.moving = True

                    nodelist = new_order
                else:
                    new_order = list (nodelist)

                    for n in nodelist:
                        if n == clicked:
                            new_order.remove (n)
                            new_order.append (n)
                            selected_nodes = set ([n])
                            moving_nodes.append (n)
                            n.moving = True

                    nodelist = new_order
            else:
                selstart = pygame.mouse.get_pos ()
        elif event.type == pygame.MOUSEBUTTONUP:
            for n in moving_nodes:
                n.moving = False
            moving_nodes = []

            if selstart:
                selbox = rect (mousepos, selstart)

                for n in nodelist:
                    if selbox.colliderect (pygame.Rect (n.pos,
                                                        (n.width, n.height))):
                        selected_nodes.add (n)
                    else:
                        if n in selected_nodes:
                            selected_nodes.remove (n)

                selstart = None
        elif event.type == pygame.MOUSEMOTION:
            lastpos = tuple (mousepos)
            mousepos = pygame.mouse.get_pos ()
            diff = (mousepos[0] - lastpos[0], mousepos[1] - lastpos[1])

            for n in moving_nodes:
                n.pos[0] += diff[0]
                n.pos[1] += diff[1]

def draw ():
    global selstart, mousepos

    board.fill (BLACK)

    for n in nodelist:
        n.draw (board)

    if selstart:
        pygame.draw.rect (board, YELLOW, rect (mousepos, selstart), 1)

    pygame.display.flip ()

pygame.init ()
board = pygame.display.set_mode (SIZE)
pygame.display.set_caption ("spsh")

background = pygame.Surface (SIZE)
font = pygame.font.Font ("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf",
                         20)

files = os.listdir ("/home/atw")
nodelist = [node (name) for name in files]

selstart = None
mousepos = pygame.mouse.get_pos ()

reflow (nodelist, SIZE)

while True:
    process_input ()

    draw ()
