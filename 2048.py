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
    board = add_tile(board)
    board = add_tile(board)


    while jeu:

        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus

            if event.type == QUIT:   

                jeu = 0

            if event.type == KEYDOWN:

                if event.key == K_DOWN:

                    board = move(board,'down')
                    board = add_tile(board)

                elif event.key == K_UP:

                    board = move(board,'up')
                    board = add_tile(board)

                elif event.key == K_RIGHT:

                    board = move(board,'right')
                    board = add_tile(board)

                elif event.key == K_LEFT:

                    board = move(board,'left')
                    board = add_tile(board)

                elif board_full(board) == 1:

                    jeu = 0

        window.blit(fond, (0,0))

        for i,line in enumerate(board):

            for j,val in enumerate(line):

                if val != None:

                    window.blit(font.render(str(val), 1, (255,0,0)), (j*100,i*100))

        pygame.display.flip()

def move(board,direction): #Fonction principale pour faire bouger les pieces.

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

def fusion(line): #Fonction qui permet de fusionner les pieces.

    fusion = 0 #Permet de ne pas tout fusionner d'un coup.

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

def transpose(board): #Transpose la matrice "board" pour simplifier les mouvements.

    line_invert = []
    rotated = []

    for j in range(len(board[0])):

        for i,line in enumerate(board):

            line_invert.append(line.pop(0))

        rotated.append(line_invert)
        line_invert = []

    return rotated

def add_tile(board): #Ajoute une pieces de façon random.

    i = int(random.random()*4)
    j = int(random.random()*4)

    while board[i][j] != None: # Plutot while board_full == 0 non ?

         i = int(random.random()*4)
         j = int(random.random()*4)

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

if __name__ == "__main__":
    main()