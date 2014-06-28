#! /usr/bin/python2
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random

def main():
    pygame.init()
    window = pygame.display.set_mode((400, 400))
    font = pygame.font.Font(None,90)
    jeu = 1

    fond = pygame.image.load("background.jpg").convert()

    #On initialise le plateau de jeu 4x4
    board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
    board = addTile(board)
    board = addTile(board)


    while jeu:
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                jeu = 0      #On arrête la boucle

            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    board = move(board,'down')
                if event.key == K_UP:
                    board = move(board,'up')
                if event.key == K_RIGHT:
                    board = move(board,'right')
                if event.key == K_LEFT:
                    board = move(board,'left')
                if defeat(board) == 1:
                    jeu = 0
                else:
                    board = addTile(board)


        window.blit(fond, (0,0))
        for i,line in enumerate(board):
            for j,val in enumerate(line):
                if val != None:
                    window.blit(font.render(str(val), 1, (255,0,0)), (j*100,i*100))

        pygame.display.flip()







def move(board,direction):

    if direction == 'left':
        
        for i,line in enumerate(board):

            fusion(line)

    elif direction == 'right':

        for i,line in enumerate(board):

            line.reverse()

            fusion(line)

            line.reverse()

    elif direction == 'up':

        board = transpose(move(transpose(board),'left'))

    elif direction == 'down':

        board = transpose(move(transpose(board),'right'))

    else:
        print('error')

    return board





def fusion(line):

    fusion = 0

    #A modifier je pense
    for j,tile in enumerate(line):

        for n in range(j):

            if tile == None:
                pass

            else: 

                if  line[j-n-1] == None:
                    line[j-n-1] = line[j-n]
                    line[j-n] = None

                if line[j-n-1] != None:

                    if line[j-n-1] == line[j-n] and fusion == 0:
                        line[j-n-1] = 2*line[j-n]
                        line[j-n] = None
                        fusion = 1

                    else: # board[i][j-1] != tile
                        pass

def transpose(board):

    lineR = []
    rotated = []

    for j in range(len(board[0])):

        for i,line in enumerate(board):

            lineR.append(line.pop(0))

        rotated.append(lineR)
        lineR = []

    return rotated

def addTile(board):

    i = int(random.random()*4)
    j = int(random.random()*4)

    while board[i][j] != None:
         i = int(random.random()*4)
         j = int(random.random()*4)

    board[i][j] = 2

    return board

def defeat(board):

    compteur = 0

    for j in range(len(board[0])):

        for i,line in enumerate(board):

            if board[i][j] != None:

                compteur += compteur

    if compteur == (len(board[0]) * len(board)):
        return 1
    else:
        return 0





if __name__ == "__main__":
    main()





