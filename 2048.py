#! /usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random

def main():

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

                    if defeat(board) == 1: #board_full(board)==1 and

                        jeu = 0
                        end = 1

                    elif event.key == K_DOWN:

                        board = next(board,'down')

                        # newBoard = move(board,'down')
                        # if newBoard != board:
                        #     board = add_tile(newBoard)

                    elif event.key == K_UP:

                        board = next(board,'up')

                        # newBoard = move(board,'up')
                        # if newBoard != board:
                        #     board = add_tile(newBoard)

                    elif event.key == K_RIGHT:

                        board = next(board,'right')

                        # newBoard = move(board,'right')
                        # if newBoard != board:
                        #     board = add_tile(newBoard)

                    elif event.key == K_LEFT:

                        board = next(board,'left')

                        # newBoard = move(board,'left')
                        # if newBoard != board:
                        #     board = add_tile(newBoard)

                    if victory(board) == 1:

                        jeu = 0
                        vict = 1
                        end = 1




            window.blit(fond, (0,0))

            for i,line in enumerate(board):

                for j,val in enumerate(line):

                    if val != None:

                        window.blit(tile[val], (j*100,i*100))

            pygame.display.flip()

        while end:

            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus

                if event.type == QUIT:

                    jeu = 0
                    go = 0
                    end = 0

                if event.type == KEYDOWN:

                    jeu = 1
                    end = 0
                    board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
                    board = add_tile(board)
                    board = add_tile(board)

            window.blit(fond, (0,0))

            for i,line in enumerate(board):

                for j,val in enumerate(line):

                    if val != None:

                        window.blit(tile[val], (j*100,i*100))


            if vict == 0:
                window.blit(font.render('Perdu !', 1, (255,255,255)), (100,130))

            if vict == 1:
                window.blit(font.render('Gagné !', 1, (255,255,255)), (100,130))

            window.blit(smallFont.render('Pressez une touche pour rejouer', 1, (255,255,255)), (0,0))

            pygame.display.flip()






def move(board,direction): #Fonction principale pour faire bouger les pieces.

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

        print 'merdouille'

    return board

def fusion(line): #Fonction qui permet de fusionner les pieces.

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

                    else: # board[i][j-1] != tile

                        pass

    return line

def transpose(board): #Transpose la matrice "board" pour simplifier les mouvements.

    line_invert = []
    rotated = []

    for j in range(len(board[0])):

        line_invert = []

        for i,line in enumerate(board):

            line_invert.append(line.pop(0))

        rotated.append(line_invert)
        #line_invert = []

    return rotated

def add_tile(board): #Ajoute une piece de façon random.

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

def board_full(board): #Fonction qui parametre le remplissage du board.

    compteur = 0

    for j in range(len(board[0])):

        for i,line in enumerate(board):

            if board[i][j] != None:

                compteur += 1

    if compteur == (len(board[0]) * len(board)):

        return 1

    else:

        return 0

def next(board,direction):

    lastBoard = new(board)
    board = move(board,direction)

    #if newBoard != board:
    if equals(board,lastBoard) == False:
        board = add_tile(board)

    return board

def defeat(board):

    i = 0
    dirList = ['right','left','up','down']

    for direction in dirList:

        newBoard = move(new(board),direction)

        if equals(board,newBoard) :

            i += 1 


    #if board == newBoard:
    if i == 4:

        return 1

    else:

        return 0

def victory(board):

    a = 0

    for i,line in enumerate(board):
        a += board.count(2048)

    if a == 0:

        return 0

    else:

        return 1

def new(board):

    newBoard = []

    for l in board:

        newBoard.append(list(l))

    return newBoard

def equals(board1,board2):

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
    board = [[1,2,None,None],[None,1,None,None],[None,None,1,None],[None,None,None,1]]
    board = transpose(move(transpose(board),'left'))
    print board
