#! /usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random

def main():
    """main fuction with the use of pygame."""

    pygame.init()
    window = pygame.display.set_mode((400, 400))
    font = pygame.font.Font(None,90)
    smallFont = pygame.font.Font(None,30)

    go = 1 
    jeu = 1
    vict = 0
    end = 0

    fond = pygame.image.load("back.png").convert()

    tile = {x: pygame.image.load(str(x)+'.png').convert() for x in (2,4,8,16,32,64,128,256,512,1024,2048)}

    #On initialise le plateau de jeu 4x4
    board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
    board = add_tile(board)
    board = add_tile(board)

    while go:

        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus

            if event.type == QUIT:

                go = 0

        while jeu:

            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus

                if event.type == QUIT:

                    jeu = 0
                    end = 0
                    go = 0

                if event.type == KEYDOWN:

                    if defeat(board) == 1:

                        jeu = 0
                        end = 1

                    elif event.key == K_DOWN:

                        board = next(board,'down')

                    elif event.key == K_UP:

                        board = next(board,'up')

                    elif event.key == K_RIGHT:

                        board = next(board,'right')

                    elif event.key == K_LEFT:

                        board = next(board,'left')

                    if victory(board) == 1:

                        jeu = 0
                        vict = 1
                        end = 1


            pygame.time.Clock().tick(40)

            window.blit(fond, (0,0))

            for i,line in enumerate(board):

                for j,val in enumerate(line):

                    if val != None:

                        window.blit(tile[val], (j*100,i*100))

            pygame.display.flip()

        while end:

            for event in pygame.event.get():

                if event.type == QUIT:

                    jeu = 0
                    go = 0
                    end = 0

                if event.type == KEYDOWN:

                    if event.key == K_SPACE :

                        jeu = 1
                        end = 0
                        board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
                        board = add_tile(board)
                        board = add_tile(board)

                    if event.key == K_ESCAPE :

                        jeu = 0
                        go = 0
                        end = 0

            window.blit(fond, (0,0))

            for i,line in enumerate(board):

                for j,val in enumerate(line):

                    if val != None:

                        window.blit(tile[val], (j*100,i*100))


            if vict == 0:
                window.blit(font.render('Perdu !', 1, (255,255,255)), (100,130))

            if vict == 1:
                window.blit(font.render('Gagné !', 1, (255,255,255)), (100,130))

            window.blit(smallFont.render('Pressez espace pour rejouer', 1, (255,255,255)), (50,250))

            window.blit(smallFont.render('Pressez echap pour quitter', 1, (255,255,255)), (60,300))

            pygame.display.flip()






def move(board,direction):
    """Return the board after a movement in a direction."""

    if direction == 'left':

        for i,line in enumerate(board):

            line = fusion(line)


    elif direction == 'right':

        for i,line in enumerate(board):

            line.reverse()

            line = fusion(line)

            line.reverse()


    elif direction == 'up':

        board = transpose(move(transpose(board),'left'))

    elif direction == 'down':

        board = transpose(move(transpose(board),'right'))

    else:

        pass

    return board

def fusion(line):
    """Modify the line of the board in order to fusion the tiles"""

    fusion = 0 #Permet de ne pas tout fusionner d'un coup.

    lastFusion = None

    for j,tile in enumerate(line):

        for n in range(j):

            if tile == None:

                pass

            else:

                if  line[j-n-1] == None:

                    line[j-n-1] = line[j-n]
                    line[j-n] = None

                if line[j-n-1] != None:

                    if line[j-n-1] == line[j-n] and (lastFusion == line[j-n] or fusion == 0):

                        lastFusion = line[j-n]
                        line[j-n-1] = 2*line[j-n]
                        line[j-n] = None
                        fusion = 1

                    else:

                        pass

    return line

def transpose(board):
    """Return the transposed of the matrix board."""

    line_invert = []
    rotated = []

    for j in range(len(board[0])):

        line_invert = []

        for i,line in enumerate(board):

            line_invert.append(line.pop(0))

        rotated.append(line_invert)

    return rotated

def add_tile(board):
    """add a randomly placed tile in the board."""

    free = []

    for j in range(len(board[0])):

        for i,line in enumerate(board):

            if board[i][j] == None:

                free.append([i,j])

    if len(free) != 0:

        [i,j] = free[int(random.random()*len(free))]

        a = random.random()

        if a < 0.8:

        	board[i][j] = 2

        else:

        	board[i][j] = 4

    return board

def next(board,direction):
    """Return the board after a movement in a direction.

    If the board can be move in a direction, it is done.
    If not, nothing is done.
    """

    lastBoard = new(board)
    board = move(board,direction)

    #if newBoard != board:
    if equals(board,lastBoard) == False:
        board = add_tile(board)

    return board

def defeat(board):
    """Return 1 in case of defeat, 0 else.

    Check if the board can be moved in any direction, if not it's defeat.
    """

    i = 0
    dirList = ['right','left','up','down']

    for direction in dirList:

        newBoard = move(new(board),direction)

        if equals(board,newBoard) :

            i += 1 

    if i == 4:

        return 1

    else:

        return 0

def victory(board):
    """Return 1 in case of victory, 0 else

    Check if a tile in board have a value of 2048 then it's victory.
    """

    a = 0

    for i,line in enumerate(board):
        a += board.count(2048)

    if a == 0:

        return 0

    else:

        return 1

def new(board):
    """Return a new board with the same value as board"""  

    newBoard = []

    for l in board:

        newBoard.append(list(l))

    return newBoard

def equals(board1,board2):
    """Check if 2 boards are equals.

    if the boards have the same values at the same positions they are equals.
    """

    i = 0

    for k in range(len(board1)):

        if board1[k] == board2[k]:

            i += 1

    if i == 4:

        return True

    else:

        return False


if __name__ == "__main__":
    main()

class Board:

    new_board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]

    def __init__(self,board=self.new_board):

        self.board = []

        for l in board:

            self.board.append(line(l))

    def __eq__(self,other):

        i = 0

        for k in range(len(self)):

            if self.board[k] == other.board[k]:

                i += 1

        if i == 4:

            return True

        else:

            return False

    def __len__(self):

        return len(self.board)

    def victory(self):
        """Return 1 in case of victory, 0 else

        Check if a tile in board have a value of 2048 then it's victory.
        """

        a = 0

        for i,line in enumerate(self.board):
            a += self.board.count(2048)

        if a == 0:

            return 0

        else:

            return 1







